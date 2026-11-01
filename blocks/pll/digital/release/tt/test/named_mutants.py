#!/usr/bin/env python3
"""named_mutants.py - evidence for REQ-MUT-KILL.

    python3 blocks/pll/digital/tb/named_mutants.py

The mutate gate only scores mcy's sampled mutants, so this script applies the
four mutants the requirement names to a temporary copy of rtl/ and runs the
visible suite (test_pll.py) on each, through the calls chip-flow's sim gate
uses: check_sim.collect_sources, then cocotblib.run_cocotb and
parse_results_xml. The unmutated RTL runs first as a control and must pass.

Outcomes for a mutant:
  killed    at least one test failed with an AssertionError, every test of the
            control's suite ran, and the patched RTL built
  survived  every test passed
  error     build error, crash, timeout, a different set of tests than the
            control, or only non-assertion failures (an int() of an X signal
            raises ValueError). Not a kill.

Every patch must match exactly once or the script stops before any simulation,
so an RTL edit cannot leave it testing nothing. It writes only
reports/named_mutants.json in the workspace; RTL, the bench copy, build
directories and results go to a temp dir outside the repo. Exit 0 only when
the control passes and the kill rate is 1.0.

The name matters: chip-flow collects test_*.py as test modules (cocotblib.
test_modules), so this file is support code to every gate. It also must not
carry requirement tags or cocotb test decorators, since scan_requirement_tags
reads every *.py in tb/.

CHIP_FLOW_HOME and EDA_TOOLCHAIN override the defaults below. The script
re-executes itself through `bin/eda python`.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

TB = Path(__file__).resolve().parent
WS = TB.parent
REPORT = WS / "reports" / "named_mutants.json"
SUITE = "test_pll"
RUN_TIMEOUT_S = 1800  # per run: a hang is an error, never a pass
MSG_MAX = 300
REEXEC_MARK = "NAMED_MUTANTS_UNDER_EDA"
DEFAULT_CHIP_FLOW = "/home/hive2/projects/chip-flow-pll"
DEFAULT_TOOLCHAIN = "/opt/eda-toolchain/iic-osic-tools-2026.09"

# (name, description, [(rtl file, exact old text, new text), ...])
MUTANTS = [
    ("swapped_up_dn",
     "Swapped UP/DN: the PFD drives pfd_up from the feedback flop and pfd_dn "
     "from the reference flop.",
     [("pll_pfd.v", "assign pfd_up = pfd_ref_q;", "assign pfd_up = pfd_fb_q;"),
      ("pll_pfd.v", "assign pfd_dn = pfd_fb_q;", "assign pfd_dn = pfd_ref_q;")]),
    ("missing_pfd_reset",
     "Missing PFD reset: the delayed AND of up and dn (pfd_rst) no longer "
     "reaches the async clear, so pfd_clr is inactive whenever rst_n is high. "
     "The global rst_n term stays, so the flops still initialise and the "
     "fault is the missing PFD reset, not X propagation.",
     [("pll_pfd.v", "wire pfd_clr = ~rst_n | pfd_rst;", "wire pfd_clr = ~rst_n;")]),
    ("divider_off_by_one",
     "Divider off by one: legal codes 1..5 divide by N+1 (2..6). Illegal "
     "codes still give N = 1.",
     [("pll_divider.v",
       "n_m1    = n_legal ? (n_sel - 3'd1) : 3'd0;",
       "n_m1    = n_legal ? n_sel : 3'd0;")]),
    ("prescaler_one_stage_short",
     "Prescaler one stage short: clk_pre is taken from the first stage, "
     "vco_div2/2 = VCO/4 instead of vco_div2/4 = VCO/8. obs_q3 is untouched.",
     [("pll_prescaler.v", "assign clk_pre = pre_q1;", "assign clk_pre = pre_q0;")]),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def apply_patches(rtl: dict[str, str], patches) -> dict[str, str]:
    """A copy of rtl ({file name: text}) with patches applied. Raises when an
    old text does not match exactly once in the unpatched file."""
    out = dict(rtl)
    for fname, old, new in patches:
        if fname not in rtl:
            raise RuntimeError(f"patch target rtl/{fname} does not exist")
        n = rtl[fname].count(old)
        if n != 1:
            raise RuntimeError(
                f"patch for rtl/{fname} matched {n} times, expected exactly "
                f"once: {old!r}. The RTL changed: update this mutant.")
        out[fname] = out[fname].replace(old, new)
    return out


def run_variant(name: str, rtl: dict[str, str], tb_copy: Path, top: str,
                tmp: Path) -> dict:
    """Build and run the suite over rtl. Never raises for a failed run: the
    outcome is a dict with `results` (or None) and `error`."""
    import check_sim
    import cocotblib
    work = tmp / name
    (work / "rtl").mkdir(parents=True)
    for fname, text in rtl.items():
        (work / "rtl" / fname).write_text(text, encoding="utf-8")
    t0 = time.monotonic()
    results, error = None, None
    try:
        xml = cocotblib.run_cocotb(
            work / "sim_build", tb_copy, check_sim.collect_sources(work), top,
            [SUITE], work / "sim_results.xml", timeout_s=RUN_TIMEOUT_S)
        results = cocotblib.parse_results_xml(xml)
        if not results:
            error = "cocotb produced no test cases"
    except (Exception, SystemExit) as e:  # runner.build exits on an iverilog error
        error = f"{type(e).__name__}: {e} (log: {work / 'sim_build' / 'sim.log'})"
        results = None
    return {"results": results, "error": error,
            "wall_s": round(time.monotonic() - t0, 1)}


def short(msg) -> str | None:
    if msg is None:
        return None
    msg = str(msg).strip()
    return msg if len(msg) <= MSG_MAX else msg[:MSG_MAX] + "..."


def is_assertion(res: dict) -> bool:
    return (res.get("type") or "").rsplit(".", 1)[-1] == "AssertionError"


def classify(run: dict, control_tests: set[str]) -> dict:
    """The mutant's report entry fields from one run_variant result."""
    results = run["results"] or {}
    asserted = {t: short(r["message"]) for t, r in sorted(results.items())
                if not r["passed"] and not r.get("skipped") and is_assertion(r)}
    other = {t: f"{r.get('type') or 'skipped'}: {short(r['message'])}"
             for t, r in sorted(results.items())
             if not r["passed"] and t not in asserted}
    error = run["error"]
    if error is None and set(results) != control_tests:
        missing = sorted(control_tests - set(results))
        extra = sorted(set(results) - control_tests)
        error = f"test set differs from the control: missing {missing}, extra {extra}"
    if error is None and other and not asserted:
        error = "only non-assertion failures"
    if error is not None:
        status = "error"
    elif asserted:
        status = "killed"
    else:
        status = "survived"
    return {"killed": status == "killed", "status": status,
            "failing_tests": sorted(asserted), "failure_messages": asserted,
            "non_assertion_failures": other, "error": error,
            "tests_run": len(results), "wall_s": run["wall_s"]}


def reexec_under_eda() -> None:
    home = os.environ.setdefault("CHIP_FLOW_HOME", DEFAULT_CHIP_FLOW)
    os.environ.setdefault("EDA_TOOLCHAIN", DEFAULT_TOOLCHAIN)
    os.environ[REEXEC_MARK] = "1"
    eda = str(Path(home) / "bin" / "eda")
    os.execv(eda, [eda, "python", str(Path(__file__).resolve()), *sys.argv[1:]])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.parse_args()
    if not os.environ.get(REEXEC_MARK):
        reexec_under_eda()

    t_start = time.monotonic()
    REPORT.unlink(missing_ok=True)  # a failed run must not leave an old pass behind

    home = Path(os.environ["CHIP_FLOW_HOME"])
    sys.path.insert(0, str(home / "engine" / "scripts"))
    import check_sim  # also puts engine/lib on sys.path
    import cocotblib
    import speclib

    top = speclib.load_spec(WS / "spec" / "spec.yaml")["top"]
    sources = check_sim.collect_sources(WS)
    rtl = {p.name: p.read_text(encoding="utf-8") for p in sources}

    # Stop on a stale patch before spending any simulation time.
    patched = {name: apply_patches(rtl, patches) for name, _, patches in MUTANTS}

    collected = cocotblib.test_modules(TB)
    if SUITE not in collected or Path(__file__).stem in collected:
        raise RuntimeError(f"unexpected test collection from tb/: {collected}")

    hashes = {f"rtl/{p.name}": sha256(p) for p in sources}
    hashes[f"tb/{SUITE}.py"] = sha256(TB / f"{SUITE}.py")

    repo_root = WS.parent.parent.parent
    with tempfile.TemporaryDirectory(prefix="named_mutants_") as d:
        tmp = Path(d).resolve()
        if tmp.is_relative_to(repo_root):
            raise RuntimeError(f"temp dir {tmp} is inside the repo")
        # A bench copy, so nothing is written to tb/ (a hashed gate input).
        tb_copy = tmp / "tb"
        tb_copy.mkdir()
        for p in sorted(TB.glob("*.py")):
            if p.name != Path(__file__).name:
                shutil.copy2(p, tb_copy / p.name)

        run = run_variant("control", rtl, tb_copy, top, tmp)
        results = run["results"] or {}
        bad = sorted(t for t, r in results.items() if not r["passed"])
        control_ok = run["error"] is None and bool(results) and not bad
        control = {
            "passed": control_ok, "tests_run": len(results),
            "tests_passed": sum(1 for r in results.values() if r["passed"]),
            "failing_tests": bad, "error": run["error"],
            "wall_s": run["wall_s"]}
        print(f"control: {'PASS' if control_ok else 'FAIL'} "
              f"{control['tests_passed']}/{control['tests_run']} "
              f"({run['wall_s']} s)", flush=True)

        control_tests = set(results)
        entries = []
        for name, desc, patches in MUTANTS:
            entry = {"name": name, "description": desc,
                     "patches": [{"file": f"rtl/{f}", "old": o, "new": n}
                                 for f, o, n in patches]}
            entry.update(classify(
                run_variant(name, patched[name], tb_copy, top, tmp),
                control_tests))
            entries.append(entry)
            print(f"{name}: {entry['status']} {entry['failing_tests']} "
                  f"({entry['wall_s']} s)"
                  + (f" error: {entry['error']}" if entry["error"] else ""),
                  flush=True)

    # The evidence is void if the inputs moved during the run.
    now = {f"rtl/{p.name}": sha256(p) for p in check_sim.collect_sources(WS)}
    now[f"tb/{SUITE}.py"] = sha256(TB / f"{SUITE}.py")
    if now != hashes:
        raise RuntimeError("rtl/ or the suite changed during the run; rerun")

    killed = sum(1 for e in entries if e["killed"])
    total = len(entries)
    rate = killed / total
    report = {
        "requirement": "REQ-MUT-KILL",
        "date": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "top": top,
        "suite": f"tb/{SUITE}.py",
        "control": control,
        "mutants": entries,
        "killed": killed,
        "total": total,
        "rate": rate,
        "sha256": hashes,
        "wall_s": round(time.monotonic() - t_start, 1),
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"killed {killed}/{total}, rate {rate}; control "
          f"{'pass' if control_ok else 'FAIL'}; wrote {REPORT}", flush=True)
    return 0 if control_ok and rate == 1.0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
