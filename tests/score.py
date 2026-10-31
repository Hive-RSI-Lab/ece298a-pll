"""The project's score: the share of the goals' checkable done-lines that pass.

    bash tests/score.sh        (runs this with the tree's python, chip-flow set)

Each "Done when" in GOALS.md's proposed goals is cut into the lines below,
each worth one. A line over corners (the analog PVT sweep, the digital STA
corners, the post-layout benches) earns the share of its corners that pass,
so a change that fixes one corner moves the number. Every gate is re-run
here, from a scratch copy of blocks/pll, through chip-flow's gate.py
(sim_pvt through the engine's sweep, a corner per worker: pvt_sweep), with
one exception: bench_strength takes longer than the check may run, so its
recorded pass counts only while its inputs are unchanged
(bench_strength_fresh); nor do the Harden goal's top_harden, top_drc,
top_lvs and precheck, for the same reason (tile), nor the loop on the
extracted netlist at its bounding corners (cosim_corners_fresh). A gate that can't run (a tool missing, a
refusal, a timeout) fails its line; nothing is skipped.

Prints a line per done-line, then the score alone on the last line: 100 x
the mean over the lines, higher is better.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
BLOCK = ROOT / "blocks" / "pll"
CFH = Path(os.environ["CHIP_FLOW_HOME"])
EDA = str(CFH / "bin" / "eda")
GATE = str(CFH / "engine" / "scripts" / "gate.py")

# The check that runs this stops at 30 minutes; the chains run side by side
# and each stops here, so the score always prints.
DEADLINE = time.monotonic() + float(os.environ.get("PLL_SCORE_BUDGET_S", 24 * 60))
VCO_TARGET_HZ = 100e6
# The 31 corners the signed-off spec scores (H1-ada9eb plus its open items):
# the full grid, the two resistor-skew corners and the engine's tt_pss/tt_pff.
# A spec that drops one still has it counted, as failing: taking a corner out
# of the spec can't raise the score.
REQUIRED_CORNERS = [f"{p}_{t}{s}" for p in ("tt", "ss", "ff") for t in ("m40c", "27c", "125c")
                    for s in ("_vm10", "", "_vp10")] + ["ss_pff", "ff_pss", "tt_pss", "tt_pff"]


def copy_block(scratch: Path, name: str) -> Path:
    dst = scratch / name
    shutil.copytree(BLOCK, dst, symlinks=True, ignore=shutil.ignore_patterns(
        "state_snapshots", "__pycache__", "runs", "sim_build"))
    return dst


def gate(ws: Path, skill: str, name: str, logs: Path, tag: str) -> dict:
    """Run one gate in ws; its result json, with status "pass" only on a pass."""
    out, log = logs / f"{tag}-{name}.json", logs / f"{tag}-{name}.log"
    left = DEADLINE - time.monotonic()
    if left <= 0:
        return {"status": "timeout", "why": "the score's time ran out before it started"}
    try:
        with log.open("w") as f:
            rc = subprocess.run([EDA, "python", GATE, "--gate", name, "--skill", skill,
                                 "--workspace", str(ws), "--out", str(out)],
                                cwd=ws, stdout=f, stderr=subprocess.STDOUT,
                                stdin=subprocess.DEVNULL, timeout=left).returncode
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "why": "the score's time ran out"}
    try:
        res = json.loads(out.read_text())
    except (OSError, ValueError):
        tail = log.read_text(errors="replace").strip().splitlines()[-1:] or [""]
        return {"status": f"exit {rc}", "why": tail[0][:200]}
    if rc != 0 and res.get("status") == "pass":
        res["status"] = f"exit {rc}"
    return res


def chain(ws: Path, skill: str, names: list[str], logs: Path, tag: str) -> dict[str, dict]:
    """Gates in pipeline order; once one doesn't pass, the rest aren't run."""
    got: dict[str, dict] = {}
    for n in names:
        got[n] = gate(ws, skill, n, logs, tag)
        if got[n].get("status") != "pass" and n != names[-1]:
            for m in names[names.index(n) + 1:]:
                got[m] = {"status": "not run", "why": f"{n} did not pass"}
            break
    return got


def why(res: dict) -> str:
    if res.get("why"):
        return f"{res['status']}: {res['why']}"
    msgs = [str(v.get("msg") or v.get("kind")) for v in res.get("failing") or []]
    err = str(res.get("error") or "").strip().splitlines()[-1:] or []
    return f"{res.get('status')}" + "".join(f"; {m[:160]}" for m in (err + msgs)[:3])


def spec_corners(spec: dict) -> list[str]:
    """Every corner the analog spec scores: its grid, its extras, and the
    engine's tt_pss/tt_pff, as sim_pvt runs them."""
    g = (spec.get("corners") or {}).get("grid") or {}
    proc = {"typical": "tt", "ss": "ss", "ff": "ff"}
    temp = lambda t: f"m{-t}c" if t < 0 else f"{t}c"  # noqa: E731
    sup = lambda s: "" if s == 0 else (f"_vm{-s}" if s < 0 else f"_vp{s}")  # noqa: E731
    out = [f"{proc[p]}_{temp(t)}{sup(s)}" for p in g.get("process", [])
           for t in g.get("temp_c", []) for s in g.get("supply_pct", [])]
    for c in list((spec.get("corners") or {}).get("extra") or []) + ["tt_pss", "tt_pff"]:
        if c not in out:
            out.append(c)
    return out


def pvt_sweep(ws: Path, corners: list[str], logs: Path) -> tuple[int, list[str]]:
    """sim_pvt's sweep, one corner per worker: the engine's own
    sim_run.run_workspace_benches over the spec's sweep, with sim_pvt's
    timeout and refusals, which the gate runs one deck at a time (about 25
    minutes here, against the check's 30). A corner passes when every bench
    scored there ran and has no error-severity finding."""
    sys.path[:0] = [str(CFH / "engine" / "scripts"), str(CFH / "engine" / "lib")]
    import check_sim_pvt  # noqa: E402
    import sim_run  # noqa: E402
    import speclib  # noqa: E402

    try:
        sweep, _ = sim_run.spec_sweep(ws)
        timeout = speclib.sim_timeout(speclib.load_spec(ws / "spec" / "spec.yaml"), "sim_pvt",
                                      None, check_sim_pvt.DEFAULT_TIMEOUT)
    except Exception as e:  # noqa: BLE001  (a refusal fails every corner)
        return 0, [f"sim_pvt refused: {str(e).strip()[:200]}"]
    by_name = {c["name"]: c for c in sweep}

    def one(name: str) -> str:
        if name not in by_name:
            return "not in the spec's sweep"
        if time.monotonic() > DEADLINE:
            return "the score's time ran out"
        try:
            res = sim_run.run_workspace_benches(
                ws, corners=[by_name[name]], timeout=timeout, check="sim_pvt",
                out_subdir=f"log/score_pvt/{name}", scope_corners=sweep, refuse_unswept=True)
        except Exception as e:  # noqa: BLE001
            return f"did not run: {str(e).strip()[:160]}"
        (logs / f"pvt-{name}.json").write_text(json.dumps(res, default=str))
        if not res["results"]:
            return "no bench ran"
        for r in res["results"]:
            if r.get("returncode") or r.get("engine_errors"):
                return f"{r.get('bench')} did not run clean"
        errs = [v for v in res["violations"] if v.get("severity") == "error"]
        return str(errs[0].get("msg"))[:160] if errs else ""

    with ThreadPoolExecutor(max(1, min(12, (os.cpu_count() or 2) // 2))) as pool:
        bad = {c: m for c, m in zip(corners, pool.map(one, corners)) if m}
    return len(corners) - len(bad), [f"{c}: {m}" for c, m in bad.items()][:4]


def analog(ws: Path, corners: list[str], logs: Path) -> tuple[dict, tuple[int, list[str]]]:
    got = chain(ws, "ade", ["spec_lint", "netlist_lint", "sim_tt"], logs, "analog")
    if any(r.get("status") != "pass" for r in got.values()):
        first = next(n for n, r in got.items() if r.get("status") != "pass")
        return got | {"bench_strength": {"status": "not run", "why": f"{first} did not pass"}}, \
            (0, [f"not run: {first} did not pass"])
    pvt = pvt_sweep(ws, corners, logs)
    if pvt[0] < len(corners):
        got["bench_strength"] = {"status": "not run", "why": "sim_pvt did not pass"}
    else:
        got["bench_strength"] = bench_strength_fresh(ws)
    return got, pvt


def bench_strength_fresh(ws: Path) -> dict:
    """bench_strength's recorded pass, while it still holds. The gate runs
    253 mutants for 30 minutes and more, past the check's whole limit, so it
    isn't re-run here: its pass counts only while every input it read
    (netlist, tb, sizing, spec, mutant rulings; the engine's invalidation
    map) hashes as it did when it passed (recorded_fresh)."""
    return recorded_fresh(ws, "ade", "bench_strength")


def recorded_fresh(ws: Path, skill: str, name: str, built: tuple[str, str] | None = None) -> dict:
    """A gate's recorded pass, while it still holds: the last run in
    state.json and its report in reports/recorded/ both passed, and every
    input it read hashes as it did then, in both. Any change to those reads
    as failing until the gate is run again and its pass committed.

    built = (artifact kind, gate) names an input that is a build product
    git doesn't keep (top/'s hardened GDS): it can't be hashed here, so it
    counts as unchanged when that gate's own record is fresh and this one
    was recorded after it, i.e. it judged what that run built."""
    sys.path[:0] = [str(CFH / "engine" / "lib")]
    import statelib  # noqa: E402

    try:
        st = json.loads((ws / "state.json").read_text())
        rep = json.loads((ws / "reports" / "recorded" / f"gate-{name}.json").read_text())
        cur = statelib.gate_input_hashes(ws, skill, name, statelib.load_map(),
                                         st.get("artifacts"))
    except FileNotFoundError:
        return {"status": "fail", "why": f"no recorded run (run {name} and commit its result)"}
    except Exception as e:  # noqa: BLE001
        return {"status": "error", "why": f"can't read its record: {str(e).strip()[:160]}"}
    entry = (st.get("gates") or {}).get(name) or {}
    last = entry.get("last") or {}
    if entry.get("status") != "pass" or rep.get("status") != "pass":
        return {"status": "fail", "why": "its last recorded run did not pass: " + why(rep)}
    if built:
        kind, by = built
        src = (st.get("gates") or {}).get(by) or {}
        if recorded_fresh(ws, skill, by).get("status") != "pass":
            return {"status": "stale", "why": f"{by} has no fresh pass, so nothing it built counts"}
        if str(last.get("ts") or "") < str((src.get("last") or {}).get("ts") or "~"):
            return {"status": "stale", "why": f"recorded before {by}'s last run (re-run {name} on "
                    "what it built and commit its pass)"}
        cur[kind] = (last.get("inputs") or {}).get(kind)
    fresh = statelib.gate_freshness(entry, cur)
    if not fresh["fresh"] or (rep.get("inputs_at_start") or {}) | (
            {built[0]: cur[built[0]]} if built else {}) != cur:
        changed = fresh["changed_inputs"] or ["the recorded report's inputs"]
        return {"status": "stale", "why": "changed since it passed: " + ", ".join(changed)
                + f" (re-run {name} and commit its pass)"}
    return {"status": "pass"}


def tile(ws: Path) -> dict[str, dict]:
    """The Harden goal's gates, msde's on the whole block. top_harden
    (LibreLane around the analog macro, 8-11 minutes) and the precheck (7
    more) together run past what the check leaves the score, so their
    recorded results count, as bench_strength's do: top_harden while its
    inputs (digital/rtl, analog/layout, the SDCs) are unchanged, and
    top_drc, top_lvs and precheck, which read top/'s GDS that git doesn't
    keep, while top_harden's pass holds and they were recorded after it."""
    got = {"top_harden": recorded_fresh(ws, "msde", "top_harden")}
    for n in ("top_drc", "top_lvs", "precheck"):
        got[n] = recorded_fresh(ws, "msde", n, built=("top_gds", "top_harden"))
    return got


def cosim_corners_fresh() -> tuple[list[str], dict, str]:
    """tb/cosim_corners.py's recorded run (reports/recorded/cosim_corners.json)
    while every input it hashed is unchanged: the corners that bound the
    post-layout range (bounding_corners of the recorded pex_pvt), the
    recorded facts, and why it doesn't count (empty when it does). A loop on
    the extracted netlist takes longer than the score's budget, so it is
    recorded as bench_strength is; a corner the run didn't run, or any
    changed input, counts as failing."""
    sys.path.insert(0, str(BLOCK / "tb"))
    import cosim_corners  # noqa: E402

    try:
        pex = json.loads((BLOCK / "analog" / "reports" / "recorded" / "pex_pvt.json").read_text())
        want = list(cosim_corners.bounding_corners(pex))
    except (OSError, ValueError):
        return [], {}, "no recorded pex_pvt to bound the range"
    try:
        rep = json.loads(cosim_corners.OUT.read_text())
    except (OSError, ValueError):
        return want, {}, "no recorded run (run tb/cosim_corners.py and commit its report)"
    changed = [k for k, v in cosim_corners.input_hashes().items() if (rep.get("inputs") or {}).get(k) != v]
    if changed:
        return want, {}, "changed since it ran: " + ", ".join(changed) + " (re-run tb/cosim_corners.py)"
    return want, rep, ""


def pex_pvt(ws: Path, logs: Path) -> dict:
    """The layout chain (drc, lvs, pex_sim) and then, once drc and lvs pass,
    layout/pex_pvt.py: the post-layout bench at every corner of the spec's
    sweep, on the netlist pex_sim just extracted (or its own extraction when
    pex_sim stopped before it wrote one). pex_pvt's facts.corners are the
    corners that passed. pex_sim's own pass or fail at typical doesn't gate
    the sweep: a bound missed at one corner says nothing of the others."""
    got = chain(ws, "ade", ["drc", "lvs", "pex_sim"], logs, "layout")
    if any(got[g].get("status") != "pass" for g in ("drc", "lvs")):
        return got | {"pex_pvt": {"status": "not run", "why": "drc or lvs did not pass"}}
    out, log = logs / "layout-pex_pvt.json", logs / "layout-pex_pvt.log"
    left = DEADLINE - time.monotonic()
    cmd = [EDA, "python", str(ws / "layout" / "pex_pvt.py"), "--workspace", str(ws),
           "--budget-s", str(max(left - 60, 1)), "--out", str(out)]
    extracted = ws / ((got["pex_sim"].get("facts") or {}).get("extracted") or "-")
    if got["pex_sim"].get("status") in ("pass", "fail") and extracted.is_file():
        cmd += ["--extracted", str(extracted)]
    try:
        with log.open("w") as f:
            subprocess.run(cmd, cwd=ws, stdout=f, stderr=subprocess.STDOUT,
                           stdin=subprocess.DEVNULL, timeout=max(left, 1))
        got["pex_pvt"] = json.loads(out.read_text())
    except subprocess.TimeoutExpired:
        got["pex_pvt"] = {"status": "timeout", "why": "the score's time ran out"}
    except (OSError, ValueError):
        tail = log.read_text(errors="replace").strip().splitlines()[-1:] or [""]
        got["pex_pvt"] = {"status": "error", "why": tail[0][:200]}
    return got


def vco_periods_ns(sdc: Path) -> dict[str, float]:
    """vco_div2's period per process (ss, tt, ff) from the design SDC: its
    pll_vco_div2_period_ns table, or one literal create_clock period for
    all. vco_div2 is VCO/2 (the analog macro's TSPC stage, issue #48)."""
    text = sdc.read_text()
    m = re.search(r"set\s+pll_vco_div2_period_ns\s+\{([^}]*)\}", text)
    if m:
        tok = m.group(1).split()
        return {k: float(v) for k, v in zip(tok[::2], tok[1::2])}
    m = re.search(r"create_clock\s+-name\s+vco_div2\s+-period\s+([0-9.]+)", text)
    return {p: float(m.group(1)) for p in ("ss", "tt", "ff")} if m else {}


def vco_ceilings_mhz(pv: dict) -> dict[str, float]:
    """The extracted VCO's fastest (vctrl at the rail) per process over
    every corner pex_pvt swept: this run's, else the recorded run's."""
    meas = (pv.get("facts") or {}).get("measured") or {}
    if not meas:
        try:
            rec = json.loads((BLOCK / "analog" / "reports" / "recorded" / "pex_pvt.json").read_text())
            meas = (rec.get("facts") or {}).get("measured") or {}
        except (OSError, ValueError):
            meas = {}
    top: dict[str, float] = {}
    for corner, m in meas.items():
        f = (m or {}).get("vco_f_vdd_mhz")
        p = corner.split("_", 1)[0]
        if isinstance(f, (int, float)):
            top[p] = max(top.get(p, 0.0), float(f))
    return top


def layers(ws: Path, logs: Path) -> tuple[dict[str, bool], dict]:
    """run_layers.py in ws: which layers passed, and layer 3's measures."""
    log = logs / "layers.log"
    # the committed measures are the last run's: only this run's may count
    (ws / "reports" / "cosim_measures.json").unlink(missing_ok=True)
    left = DEADLINE - time.monotonic()
    try:
        with log.open("w") as f:
            subprocess.run([EDA, "python", str(ws / "tb" / "run_layers.py")], cwd=ws,
                           stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                           timeout=max(left, 1))
    except subprocess.TimeoutExpired:
        pass
    text = log.read_text(errors="replace")
    got = {k: f"== layer {k}: PASS" in text for k in "123"}
    try:
        meas = json.loads((ws / "reports" / "cosim_measures.json").read_text())
    except (OSError, ValueError):
        meas = {}
    return got, meas


def main() -> int:
    spec = yaml.safe_load((BLOCK / "analog" / "spec" / "spec.yaml").read_text()) or {}
    corners = REQUIRED_CORNERS + [c for c in spec_corners(spec) if c not in REQUIRED_CORNERS]
    scratch = Path(tempfile.mkdtemp(prefix="pll-score-"))
    logs = scratch / "logs"
    logs.mkdir()
    try:
        sim, lay, dig, top = (copy_block(scratch, n) for n in ("sim", "layout", "digital", "top"))
        # The co-simulation goes first, on its own: chip-flow's cosim gate
        # gives cocotb a fixed 240 s of wall clock, and the transistor-level
        # loop (about 100 s alone with the MOS caps' voltage-dependent C) ran
        # past it beside sim_pvt, pex_pvt and the harden on a loaded machine.
        lay3, meas = layers(top, logs)
        # sim_pvt, pex_pvt and the harden are the slow ones: side by side.
        with ThreadPoolExecutor(3) as pool:
            f_sim = pool.submit(analog, sim / "analog", corners, logs)
            f_lay = pool.submit(pex_pvt, lay / "analog", logs)
            f_dig = pool.submit(chain, dig / "digital", "vde",
                                ["spec_lint", "lint", "synth", "harden", "timing"], logs, "digital")
            (a, (n_pvt, bad_pvt)), l, d = f_sim.result(), f_lay.result(), f_dig.result()
        h = tile(BLOCK)

        lines: list[tuple[str, float, str]] = []

        def line(name: str, got: float, note: str = "") -> None:
            lines.append((name, max(0.0, min(1.0, got)), note))

        def passed(name: str, res: dict) -> None:
            ok = res.get("status") == "pass"
            line(name, 1.0 if ok else 0.0, "" if ok else why(res))

        # --- Sign off the PLL's analog half ------------------------------
        signoff = BLOCK / "analog" / "log" / "H1-signoff.md"
        ok = signoff.is_file() and re.search(r"\*\*Answer:\*\*\s*approved", signoff.read_text())
        line("analog sign-off recorded", 1.0 if ok else 0.0,
             "" if ok else "no approved answer in analog/log/H1-signoff.md")
        extra = (spec.get("corners") or {}).get("extra") or []
        fmax = [m for m in spec.get("measures") or [] if m.get("name") == "vco_fmax_ff_mhz"]
        miss = [c for c in ("ss_pff", "ff_pss") if c not in extra]
        if not (fmax and fmax[0].get("corners") == "all"):
            miss.append("vco_fmax_ff_mhz at every corner")
        line("spec scores ss_pff, ff_pss and the VCO ceiling at every corner",
             1.0 if not miss else 0.0, "missing: " + ", ".join(miss) if miss else "")
        passed("analog spec_lint", a["spec_lint"])
        line(f"analog sim_pvt corners passing ({n_pvt}/{len(corners)})", n_pvt / len(corners),
             "; ".join(bad_pvt))
        passed("analog bench_strength", a["bench_strength"])

        # --- Close digital issue 8: timing with vco_div2 (VCO/2, issue #48)
        # at twice the post-layout VCO ceiling's period on each process. The
        # SDC's vco_div2 period on a process must be at most 2x the period of
        # the extracted VCO's fastest on it; tt and ff never looser than 2x
        # the analog spec's 2.7 ns.
        t = d["timing"]
        periods = vco_periods_ns(BLOCK / "digital" / "harden" / "constraints.sdc")
        ceil = vco_ceilings_mhz(l["pex_pvt"])
        name = "digital timing with vco_div2 at 2x the post-layout VCO ceiling period"
        short = [f"{p} {periods.get(p)} ns vs 2 x 1/{ceil.get(p, 0):.1f} MHz"
                 for p in ("ss", "tt", "ff")
                 if p not in periods or p not in ceil or 2000 / periods[p] < ceil[p]
                 or (p != "ss" and periods[p] > 2 * 2.7)]
        if short:
            line(name, 0.0, "vco_div2 period misses 2x the ceiling period: " + "; ".join(short))
        elif t.get("status") not in ("pass", "fail"):
            line(name, 0.0, why(t))
        else:
            sta = (t.get("facts") or {}).get("corners") or {}
            good = [c for c, v in sta.items()
                    if (v.get("setup_ws") or -1) >= 0 and (v.get("hold_ws") or -1) >= 0]
            share = len(good) / len(sta) if sta else 0.0
            if t.get("status") != "pass" and share == 1.0:
                share = 0.0  # every corner met but the gate still failed: not a pass
            line(f"{name}, ss {periods['ss']} / tt {periods['tt']} / ff {periods['ff']} ns "
                 f"({len(good)}/{len(sta)} STA corners)",
                 share, "" if t.get("status") == "pass" else why(t))

        # --- Test the whole PLL loop in co-simulation --------------------
        n = sum(lay3.values())
        line(f"the three loop layers run from one command ({n}/3 pass)", n / 3,
             ", ".join(f"layer {k} failed" for k, v in lay3.items() if not v))
        op = meas.get("operating_point") or {}
        f = meas.get("vco_freq_hz") or 0.0
        lock = (lay3["3"] and meas.get("analog_kind") == "transistor"
                and op.get("f_vco_target_hz") == VCO_TARGET_HZ
                and abs(f - VCO_TARGET_HZ) <= 1e-3 * VCO_TARGET_HZ
                and (meas.get("lock_rises") or 0) >= 1 and meas.get("lock_drops_after_lock") == 0
                and meas.get("window_after_lock") is True)
        line("co-sim locks at 100 MHz with lock_detect held", 1.0 if lock else 0.0,
             "" if lock else f"vco {f / 1e6:.3f} MHz, lock_rises {meas.get('lock_rises')}, "
             f"drops {meas.get('lock_drops_after_lock')}, layer 3 {'pass' if lay3['3'] else 'fail'}")
        readme = BLOCK / "tb" / "README.md"
        ok = readme.is_file() and "run_layers" in readme.read_text()
        line("the co-simulation is written up next to the benches", 1.0 if ok else 0.0,
             "" if ok else "tb/README.md missing or doesn't name run_layers.py")

        # --- System verification: the loop on the extracted netlist at the
        # corners that bound its range ----------------------------------
        want, rep, note = cosim_corners_fresh()
        facts = rep.get("facts") or {}
        fails = {f.get("corner"): f.get("msg") for f in rep.get("failing") or []}
        for key, name in (("locked", "co-sim locks at 100 MHz on the extracted netlist at the bounding corners"),
                          ("corners", "and vctrl settles within 20 mV p-p there")):
            ok = [c for c in want if c in set(facts.get(key) or [])]
            bad = [f"{c}: {fails.get(c) or 'not run'}" for c in want if c not in ok]
            line(f"{name} ({len(ok)}/{len(want)})", len(ok) / len(want) if want else 0.0,
                 note or "; ".join(bad)[:300])

        # --- Lay out the analog half and match it after extraction -------
        passed("analog layout drc", l["drc"])
        passed("analog layout lvs", l["lvs"])
        pv = l["pex_pvt"]
        # pex_pvt runs the post-layout bench at every corner of the spec's
        # sweep (pex_sim, the engine's gate, at typical only)
        done = set((pv.get("facts") or {}).get("corners") or [])
        n = len([c for c in corners if c in done])
        line(f"post-layout benches pass at every scored corner ({n}/{len(corners)})",
             n / len(corners), why(pv))

        # --- Harden the tile and pass the Tiny Tapeout precheck ----------
        passed("tile top_harden (the digital half around the analog macro)", h["top_harden"])
        passed("tile top_drc", h["top_drc"])
        passed("tile top_lvs", h["top_lvs"])
        passed("tile Tiny Tapeout precheck", h["precheck"])
    finally:
        if os.environ.get("PLL_SCORE_KEEP"):
            print(f"score: scratch kept at {scratch}", file=sys.stderr)
        else:
            shutil.rmtree(scratch, ignore_errors=True)

    for name, got, note in lines:
        print(f"{got:5.3f}  {name}" + (f"  -- {note}" if note and got < 1 else ""))
    print(f"{100 * sum(g for _, g, _ in lines) / len(lines):.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
