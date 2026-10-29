#!/usr/bin/env python
"""pex_pvt.py - the analog layout's post-layout benches at every corner the
spec scores.

    eda python layout/pex_pvt.py [--workspace DIR] [--extracted FILE]
                                 [--corners NAME ...] [--jobs N] [--out FILE]

chip-flow's pex_sim gate extracts the layout with parasitics and runs
layout_ref/pll_analog_pex_tb.cir at typical only (its docstring: the corner
sweep is out of its scope). This runs the same bench at every corner of the
spec's sweep (sim_run.spec_sweep: the 3x3x3 grid, ss_pff, ff_pss and the
engine's tt_pss/tt_pff), through the engine's own sim_run.run_bench_at_corner
- the materializing, the engine-error detection and the bounds scoring
sim_pvt uses - with layout_ref/pll_analog_pex_pvt_tb.cir, the corner-open
form of the pex bench, and its .bounds.json, the spec's post_layout_bounds.

The netlist is the extracted one: --extracted names one a pex_sim run just
wrote (log/pex_sim/pll_analog.pex.ordered.spice, its pins already in the
reference's order), else this script regenerates the GDS and extracts it
itself, the way check_pex_sim.py does, into log/pex_pvt/. A corner passes
when its run printed every bounded measure, ngspice reported no engine
error and no error-severity bound failed.

Writes a gate-shaped JSON (status pass only when every corner passes;
facts.corners lists the corners that passed) to --out, else stdout. Run it
with chip-flow's environment: CHIP_FLOW_HOME, and EDA_TOOLCHAIN for bin/eda.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

CFH = Path(os.environ.get("CHIP_FLOW_HOME") or "/opt/chip-flow")
sys.path[:0] = [str(CFH / "engine" / "scripts"), str(CFH / "engine" / "lib")]
import check_analog_lvs  # noqa: E402
import check_pex_sim  # noqa: E402
import layout_gen  # noqa: E402
import layoutlib  # noqa: E402
import sim_run  # noqa: E402
import simlib  # noqa: E402
import speclib  # noqa: E402

WS = Path(__file__).resolve().parent.parent
BENCH = "pll_analog_pex_pvt_tb"  # --bench pll_analog_pex_start_tb: the enable start


def extract(ws: Path) -> Path:
    """A fresh parasitic extraction of the generator's GDS, pins in the
    reference netlist's order: check_pex_sim.run's own steps, up to the
    bench."""
    block = layout_gen.block_of(ws, None)
    ref_path = check_analog_lvs.find_reference_netlist(ws, block)
    ref_text = ref_path.read_text(encoding="utf-8", errors="replace")
    ref_cell = check_analog_lvs.reference_cell(ws, block, ref_text)
    gds_path, topcell, _abs, _abstract = layout_gen.build(ws, block)
    work = ws / "log" / "pex_pvt"
    work.mkdir(parents=True, exist_ok=True)
    raw, _log = layoutlib.run_magic_extract(work, gds_path.resolve(), topcell,
                                            parasitics=True)
    raw_text = raw.read_text(encoding="utf-8", errors="replace")
    par = layoutlib.count_parasitics(raw_text)
    if not par["r"] and not par["c"]:
        raise SystemExit(f"{raw}: no R and no C line - not a parasitic extraction")
    ref_pins = check_pex_sim.pins_of(ref_text, ref_cell)
    if check_pex_sim.ground_finding(ref_text, ref_pins, raw_text, topcell,
                                    str(gds_path)) is not None:
        raise SystemExit("the extracted netlist has no ground node 0 (pex_sim's "
                         "ground_unlabelled): fix the layout first")
    out = work / f"{topcell}.pex.ordered.spice"
    out.write_text(check_pex_sim.reorder_pins(raw_text, topcell, ref_pins),
                   encoding="utf-8")
    return out


def rel(p: Path, ws: Path) -> str:
    try:
        return str(p.relative_to(ws))
    except ValueError:
        return str(p)


def run(ws: Path, extracted: Path, names: list[str] | None, jobs: int,
        deadline: float | None = None, bench: str = BENCH) -> dict:
    spec = speclib.load_spec(ws / "spec" / "spec.yaml")
    sweep, _scoped = sim_run.spec_sweep(ws)
    corners = [c for c in sweep if not names or c["name"] in names]
    unknown = sorted(set(names or []) - {c["name"] for c in sweep})
    cir = ws / "layout_ref" / f"{bench}.cir"
    bounds = simlib.load_bounds(ws / "layout_ref" / f"{bench}.bounds.json")
    template = cir.read_text(encoding="utf-8")
    timeout = speclib.sim_timeout(spec, "pex_sim", None, check_pex_sim.DEFAULT_TIMEOUT)
    t_root = sim_run.toolchain_root(sim_run.EDA_BIN)
    sizing = sim_run.load_sizing(ws)
    out_dir = ws / "log" / "pex_pvt" / bench

    def one(corner: dict) -> dict:
        if deadline is not None and time.monotonic() > deadline:
            return {"corner": corner["name"], "measures": {}, "engine_errors": [],
                    "violations": [{"severity": "error", "kind": "not_run",
                                    "msg": "out of time before it started"}]}
        subs = sim_run.build_subs(t_root, extracted, corner, spec["supply"]["vdd"], sizing)
        return sim_run.run_bench_at_corner(
            sim_run.EDA_BIN, cir.name, template, bounds, subs, corner,
            out_dir, timeout, check="pex_sim")

    with ThreadPoolExecutor(max(1, jobs)) as pool:
        results = list(pool.map(one, corners))
    passed, failing = [], []
    for r in results:
        errs = [v for v in r["violations"] if v.get("severity") == "error"]
        if r.get("engine_errors") or errs:
            failing.append({"corner": r["corner"], "msg": "; ".join(
                str(v.get("msg"))[:160] for v in errs[:2]) or str(r["engine_errors"])})
        else:
            passed.append(r["corner"])
    for n in unknown:
        failing.append({"corner": n, "msg": "not in the spec's sweep"})
    return {"script": "pex_pvt", "gate": "pex_pvt", "bench": cir.name,
            "status": "pass" if corners and not failing else "fail",
            "failing_count": len(failing), "failing": failing,
            "facts": {"extracted": rel(extracted, ws), "corners": passed,
                      "swept": [c["name"] for c in corners],
                      "measured": {r["corner"]: r.get("measures", {}) for r in results}}}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--workspace", default=str(WS))
    ap.add_argument("--extracted", help="an extracted netlist, pins in the reference's order")
    ap.add_argument("--corners", nargs="*", help="only these corners of the spec's sweep")
    ap.add_argument("--bench", default=BENCH, help="a layout_ref/ bench with a .bounds.json")
    ap.add_argument("--jobs", type=int, default=max(1, min(12, (os.cpu_count() or 2) // 2)))
    ap.add_argument("--budget-s", type=float, help="stop starting corners after this long")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    ws = Path(a.workspace).resolve()
    deadline = time.monotonic() + a.budget_s if a.budget_s else None
    extracted = Path(a.extracted).resolve() if a.extracted else extract(ws)
    res = run(ws, extracted, a.corners, a.jobs, deadline, a.bench)
    text = json.dumps(res, indent=1, default=str)
    if a.out:
        Path(a.out).write_text(text + "\n")
    else:
        print(text)
    for r in sorted(res["facts"]["measured"]):
        m = res["facts"]["measured"][r]
        print(f"{r:14} " + " ".join(f"{k}={v:.4g}" for k, v in sorted(m.items())), file=sys.stderr)
    for f in res["failing"]:
        print(f"FAIL {f['corner']}: {f['msg']}", file=sys.stderr)
    print(f"pex_pvt: {len(res['facts']['corners'])}/{len(res['facts']['swept'])} corners pass",
          file=sys.stderr)
    return 0 if res["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
