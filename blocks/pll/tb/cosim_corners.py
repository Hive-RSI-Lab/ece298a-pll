#!/usr/bin/env python
"""cosim_corners.py - the whole loop on the extracted analog netlist at the
corners that bound its range.

    $CHIP_FLOW_HOME/bin/eda python blocks/pll/tb/cosim_corners.py \
        [--corners NAME ...] [--extracted FILE] [--jobs N] [--timeout-s S] [--out FILE]

The cosim gate (layer 3 of run_layers.py) runs the released RTL against the
schematic netlist at tt_27c only. This runs the same bench, test_pll_cosim.py
at the same nominal point (6.25 MHz x 16 = 100 MHz) with the same bounds
(pll_cosim.bounds.json) and the same evidence checks as check_cosim.py, with
the cell swapped for the layout's parasitic extraction
(analog/log/pex_pvt/pll_analog.pex.ordered.spice, pins in the reference's
order; extracted here the way layout/pex_pvt.py does when it is missing) and
the PDK libs, temperature and supply moved to each corner (sim_run's own
build_subs over the spec's sweep, as pex_pvt runs its benches).

Which corners: the ones that bound the post-layout range, read from the
recorded post-layout sweep (analog/reports/recorded/pex_pvt.json): the
lowest and highest VCO ceiling (vco_f_vdd_mhz) and the lowest and highest
loop phase margin (ol_pm_pn16_nopad_pvt_deg), plus the lowest Kvco and pump
current where those are other corners. bounding_corners() says which.

Each corner is its own process (its own cocotb build, ngspice and SIGALRM),
--jobs side by side. Writes a gate-shaped json (default
reports/recorded/cosim_corners.json): status pass only when every corner
asked for meets every bound, facts.corners the ones that did, facts.locked
the ones that locked and held at 100 MHz (every bound but vctrl's p-p,
locks()), per-corner measures,
and inputs: a hash of every file the run read (the bench, the RTL, the
analog netlist, sizing, the layout generator and the spec). tests/score.py
counts the recorded pass while those hashes hold, as it does bench_strength's:
an extracted loop takes longer than the score's time budget.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pll_tb_common as C  # noqa: E402

CFH = Path(os.environ.get("CHIP_FLOW_HOME", "/opt/chip-flow"))
sys.path[:0] = [str(CFH / "engine" / "scripts"), str(CFH / "engine" / "lib")]
ANALOG = C.ANALOG
PEX_PVT = ANALOG / "reports" / "recorded" / "pex_pvt.json"
EXTRACTED = ANALOG / "log" / "pex_pvt" / "pll_analog.pex.ordered.spice"
OUT = C.WS / "reports" / "recorded" / "cosim_corners.json"
BOUNDS = HERE / "pll_cosim.bounds.json"
# What the run reads, relative to blocks/pll; tests/score.py hashes the same
# list (input_hashes) to tell whether a recorded pass still holds.
INPUTS = ["tb/test_pll_cosim.py", "tb/pll_tb_common.py", "tb/cosim_corners.py",
          "tb/pll_analog_tr.sp", "tb/pll_cosim_top.v", "tb/pll_cosim.bounds.json",
          "tb/cosim_bench.json", "digital/rtl", "analog/netlist/pll_analog.cir",
          "analog/sizing/sizing.yaml", "analog/layout/gen_pll_analog.py",
          "analog/spec/spec.yaml"]
# measures bounded the post-layout range on: (key, which end)
RANGE = [("vco_f_vdd_mhz", min), ("vco_f_vdd_mhz", max),
         ("ol_pm_pn16_nopad_pvt_deg", min), ("ol_pm_pn16_nopad_pvt_deg", max),
         ("vco_kvco_mhz_per_v", min), ("icp_dn_code00_ua", min)]
TIMEOUT_S = 7200.0
# The bench's fallback sync (PLL_COSIM_MAX_SYNC_NS) on the extracted netlist.
# At the bench's 1 ns, edges quantised to the grid fire isolated pump kicks of
# +-15-20 mV through R1 (27.4 mV p-p at ff_m40c_vm10); at 0.25 ns they go (0.6 mV).
MAX_SYNC_NS = 0.25


def input_hashes(ws: Path = C.WS) -> dict[str, str]:
    """sha256 of each INPUTS entry (a directory: of its files, sorted, and
    their names); a missing one hashes as 'missing'."""
    out = {}
    for rel in INPUTS:
        p = ws / rel
        h = hashlib.sha256()
        files = sorted(q for q in p.rglob("*") if q.is_file()) if p.is_dir() else [p]
        if not p.exists():
            out[rel] = "missing"
            continue
        for f in files:
            h.update(str(f.relative_to(ws)).encode() + b"\0")
            h.update(f.read_bytes())
        out[rel] = h.hexdigest()
    return out


def bounding_corners(pex: dict) -> dict[str, list[str]]:
    """corner -> why it bounds the range, from a pex_pvt report's measures."""
    meas = (pex.get("facts") or {}).get("measured") or {}
    got: dict[str, list[str]] = {}
    for key, end in RANGE:
        have = {c: m[key] for c, m in meas.items() if isinstance((m or {}).get(key), (int, float))}
        if not have:
            continue
        c = end(have, key=have.get)
        got.setdefault(c, []).append(f"{end.__name__} {key} {have[c]:.4g}")
    return got


def extract() -> Path:
    sys.path.insert(0, str(ANALOG / "layout"))
    import pex_pvt  # noqa: E402
    return pex_pvt.extract(ANALOG)


def setup_for(corner_name: str, extracted: Path, out: Path) -> dict:
    """The bench's PLL_COSIM_SETUP at one corner of the spec's sweep."""
    import sim_run  # noqa: E402
    import speclib  # noqa: E402
    sweep, _ = sim_run.spec_sweep(ANALOG)
    by = {c["name"]: c for c in sweep}
    if corner_name not in by:
        raise SystemExit(f"{corner_name}: not in the spec's sweep")
    spec = speclib.load_spec(ANALOG / "spec" / "spec.yaml")
    subs = sim_run.build_subs(sim_run.toolchain_root(sim_run.EDA_BIN), extracted,
                              by[corner_name], spec["supply"]["vdd"], sim_run.load_sizing(ANALOG))
    lines = C.model_lines(subs["CORNER"], subs["RES_CORNER"], subs["MIM_CORNER"],
                          netlist=extracted)
    lines.append(f".temp {subs['TEMP_C']}")
    return {"corner": corner_name, "vdd": float(subs["VDD"]), "netlist": str(extracted),
            "lines": lines, "out": str(out)}


def locks(res: dict) -> bool:
    """The loop locked and held at this corner: it ran clean (no bridge
    error, no ngspice non-convergence), lock rose within 50 us and never
    fell, and over the last 10 us after lock f_fb and f_vco are within
    0.1 % - every bound but vctrl's 20 mV p-p, which says whether vctrl has
    settled and is counted on its own (settled)."""
    m = res.get("measures") or {}
    other = [w for w in res.get("why") or [] if "vctrl_pp_last_10us_mv" not in w
             and not w.startswith("test failed")]
    lt, fb, vco = m.get("lock_time_us"), m.get("fb_period_rel_err"), m.get("vco_period_rel_err")
    return (not other and isinstance(lt, (int, float)) and lt <= 50
            and m.get("lock_drops_after_lock") == 0 and m.get("window_after_lock") is True
            and isinstance(fb, (int, float)) and fb <= 1e-3
            and isinstance(vco, (int, float)) and vco <= 1e-3)


def run_one(corner: str, extracted: Path, work: Path, timeout_s: float) -> dict:
    """The bench at one corner, in this process; the result dict."""
    import check_cosim  # noqa: E402
    import cocotblib  # noqa: E402
    check_cosim.ensure_ngspice_env(check_cosim.toolchain_root())
    work.mkdir(parents=True, exist_ok=True)
    meas_path = work / "measures.json"
    meas_path.unlink(missing_ok=True)
    os.environ["PLL_COSIM_SETUP"] = json.dumps(setup_for(corner, extracted, meas_path))
    os.environ["PLL_COSIM_MAX_SYNC_NS"] = str(MAX_SYNC_NS)
    meta = check_cosim.load_bench_meta(HERE)
    build = work / "build"
    t0 = time.monotonic()
    err = None
    results = {}
    try:
        xml = cocotblib.run_cocotb(build, HERE, check_cosim.collect_sources(HERE), meta["top"],
                                   cocotblib.test_modules(HERE), work / "results.xml",
                                   timeout_s=timeout_s)
        results = cocotblib.parse_results_xml(xml)
    except Exception as e:  # noqa: BLE001 - a timeout or a crash fails the corner
        err = f"{type(e).__name__}: {str(e).strip()[:200]}"
    log = build / "sim.log"
    log_text = log.read_text(errors="replace") if log.is_file() else ""
    meas = json.loads(meas_path.read_text()) if meas_path.is_file() else None
    bad = [f"{v['kind']}: {v['msg']}" for v in check_cosim.evaluate_measures(meas, meta["bounds"])]
    nonconv = check_cosim.scan_nonconvergence(log_text)
    failed = [n for n, r in results.items() if not r["passed"]]
    why = ([err] if err else []) + bad + [f"ngspice: {n}" for n in nonconv] + \
        [f"test failed: {n}" for n in failed] + ([] if results or err else ["no test ran"])
    keep = ["lock_time_us", "lock_drops_after_lock", "fb_period_rel_err", "vco_period_rel_err",
            "vctrl_pp_last_10us_mv", "vco_freq_hz", "fb_freq_hz", "vctrl_final_v",
            "vctrl_mean_window_v", "static_phase_offset_ns", "vco_min_period_ns_after_en",
            "lock_rises", "window_after_lock", "spice_time_reached_ns", "digital_toggles",
            "bridge_error", "operating_point", "vctrl_trace_us_v"]
    return {"corner": corner, "status": "fail" if why else "pass", "why": why,
            "wall_s": round(time.monotonic() - t0, 1),
            "measures": {k: meas.get(k) for k in keep} if meas else None}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--corners", nargs="*", help="default: bounding_corners() of the recorded pex_pvt")
    ap.add_argument("--extracted", help=f"default {EXTRACTED.relative_to(C.WS)}, extracted when missing")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--timeout-s", type=float, default=TIMEOUT_S, help="per corner")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--from-logs", action="store_true",
                    help="summarise the last run's log/cosim_corners/<corner>/result.json, run nothing")
    ap.add_argument("--one", help=argparse.SUPPRESS)       # a worker: this corner only
    ap.add_argument("--work", help=argparse.SUPPRESS)
    a = ap.parse_args(argv)

    if a.one:
        res = run_one(a.one, Path(a.extracted), Path(a.work), a.timeout_s)
        Path(a.out).write_text(json.dumps(res, indent=1, default=str))
        return 0 if res["status"] == "pass" else 1

    pex = json.loads(PEX_PVT.read_text())
    why = bounding_corners(pex)
    corners = a.corners or list(why)
    extracted = Path(a.extracted).resolve() if a.extracted else EXTRACTED
    if not extracted.is_file():
        print(f"cosim_corners: extracting the layout into {extracted.parent}", flush=True)
        extracted = extract()
    inputs = input_hashes()
    root = C.WS / "log" / "cosim_corners"

    def one(c: str) -> dict:
        work = root / c
        work.mkdir(parents=True, exist_ok=True)
        res_path = work / "result.json"
        res_path.unlink(missing_ok=True)
        cmd = [sys.executable, str(Path(__file__).resolve()), "--one", c, "--extracted",
               str(extracted), "--work", str(work), "--timeout-s", str(a.timeout_s),
               "--out", str(res_path)]
        with (work / "run.log").open("w") as f:
            try:
                subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                               timeout=a.timeout_s + 300)
            except subprocess.TimeoutExpired:
                pass
        try:
            res = json.loads(res_path.read_text())
        except (OSError, ValueError):
            tail = (work / "run.log").read_text(errors="replace").strip().splitlines()[-1:] or [""]
            res = {"corner": c, "status": "fail", "why": [f"no result: {tail[0][:200]}"],
                   "measures": None}
        res["bounds_the_range"] = why.get(c, [])
        m = res.get("measures") or {}
        print(f"{c:14} {res['status']:4} lock {m.get('lock_time_us')} us, "
              f"f_vco {(m.get('vco_freq_hz') or 0) / 1e6:.4f} MHz, vctrl "
              f"{m.get('vctrl_mean_window_v')} V, {res.get('wall_s')} s"
              + "".join(f"\n    {w}" for w in res.get("why") or []), flush=True)
        return res

    if a.from_logs:
        results = []
        for c in corners:
            try:
                r = json.loads((root / c / "result.json").read_text())
            except (OSError, ValueError):
                r = {"corner": c, "status": "fail", "why": ["no result in log/cosim_corners"],
                     "measures": None}
            r["bounds_the_range"] = why.get(c, [])
            results.append(r)
    else:
        with ThreadPoolExecutor(max(1, a.jobs)) as pool:
            results = list(pool.map(one, corners))
    passed = [r["corner"] for r in results if r["status"] == "pass"]
    locked = [r["corner"] for r in results if locks(r)]
    rep = {"script": "cosim_corners", "gate": "cosim_corners",
           "status": "pass" if corners and len(passed) == len(corners) else "fail",
           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "failing_count": len(corners) - len(passed),
           "failing": [{"corner": r["corner"], "msg": "; ".join(r.get("why") or [])[:300]}
                       for r in results if r["status"] != "pass"],
           "facts": {"corners": passed, "locked": locked, "swept": corners, "bounding": why,
                     "extracted": str(extracted.relative_to(C.WS)) if extracted.is_relative_to(C.WS)
                     else str(extracted),
                     "operating_point": {"f_ref_hz": C.F_REF_HZ, "n_sel": C.N_SEL,
                                         "p_times_n": C.P * C.N_SEL,
                                         "f_vco_target_hz": C.F_REF_HZ * C.P * C.N_SEL},
                     "results": results},
           "inputs": inputs}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(rep, indent=1, default=str) + "\n")
    print(f"cosim_corners: {len(locked)}/{len(corners)} corners lock, {len(passed)}/{len(corners)} "
          f"meet every bound (vctrl settled too) -> {a.out}")
    return 0 if rep["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
