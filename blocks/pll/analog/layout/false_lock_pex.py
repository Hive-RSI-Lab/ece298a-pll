#!/usr/bin/env python
"""false_lock_pex.py - can the extracted cell's TSPC /2 drop VCO edges with
vctrl at the rail (the false lock of verify.html claim 1.7)?

    eda python layout/false_lock_pex.py [--extracted FILE] [--corners NAME ...]
                                        [--bench rail|div|burst] [--jobs N] [--out FILE]

--bench rail (layout_ref/pll_analog_pex_rail_tb.cir): the extracted
pll_analog with vctrl forced to vdd and vdd-0.1 V, the ring started from
pll_en. Scores the bench's own bounds (f(vco_out)/f(vco_div2) = 2) and then
reads the bench's traces cycle by cycle over 200..500 ns: between every two
rising crossings of vco_div2 there must be exactly two rising crossings of
vco_out. Reports the VCO frequency, its shortest single period and the
count of /2 cycles that did not hold exactly two VCO edges.

--bench div (layout_ref/pll_analog_pex_div_tb.cir): the extracted cell's
TSPC /2 alone, its ring held, vco_out driven by an ideal clock stepped up
in frequency; reports the highest frequency it still divides exactly
(the real /2 limit, for the model in tb/prescaler_margin.py).

--bench burst (layout_ref/pll_analog_pex_burst_tb.cir): checks for burst
mode (fast cycles, then 20-30 ns stalls; seen only with bias_ref bare) below
the rail: vctrl at vdd-0.2 .. vdd-0.9 V from enable, and vdd-0.3 V ramped to vdd
while running. Reports the same cycle check over 400..600 ns plus "stalls",
the count of VCO periods over twice the median one.

Corners are the spec's sweep (sim_run.spec_sweep), run through the engine's
sim_run.run_bench_at_corner, each in its own directory under
log/false_lock_pex/<bench>/<corner>/ (the traces have fixed names). The
netlist is --extracted, else log/pex_pvt/pll_analog.pex.ordered.spice when
it is newer than the layout generator's inputs, else a fresh extraction
(pex_pvt.extract). Writes JSON to --out, else stdout. Run it with
chip-flow's environment (CHIP_FLOW_HOME, EDA_TOOLCHAIN).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pex_pvt  # noqa: E402  (sets up chip-flow's engine path)
from pex_pvt import sim_run, simlib, speclib, check_pex_sim  # noqa: E402

WS = Path(__file__).resolve().parent.parent
BENCHES = {"rail": "pll_analog_pex_rail_tb", "div": "pll_analog_pex_div_tb",
           "burst": "pll_analog_pex_burst_tb"}
BURST_RUNS = ["vdd-0.2", "vdd-0.3", "vdd-0.5", "vdd-0.7", "vdd-0.9", "ramp vdd-0.3 -> vdd"]  # burst_<k>.txt
T_FROM = 200e-9
DIV_FREQS_MHZ = [300, 400, 500, 600, 700, 800, 1000, 1200, 1500, 2000, 2500, 3000]  # the div bench's fl
GATE_RE = re.compile(r"^(X\S+ +\S+ +)nb\.t\d+( +\S+ +\S+ +[pn]fet_03v3 )")


def div_netlist(extracted: Path, out: Path) -> Path:
    """The extracted cell as pll_analog_div: vco_out and nb_drv added as
    pins, nb_drv on the gates of the output inverter's fingers (the devices
    with an nb gate and a vco_out drain or source) in place of nb."""
    lines, n = [], 0
    for ln in extracted.read_text().splitlines():
        if ln.startswith(".subckt pll_analog "):
            ln = ln.replace(".subckt pll_analog ", ".subckt pll_analog_div ", 1) + " vco_out nb_drv"
        elif GATE_RE.match(ln) and "vco_out" in ln.split()[1] + " " + ln.split()[3]:
            ln = GATE_RE.sub(r"\1nb_drv\2", ln)
            n += 1
        lines.append(ln)
    if n != 6:
        raise SystemExit(f"{extracted}: {n} output-inverter fingers found, want 6")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n")
    return out


def read_trace(path: Path) -> tuple[list[float], list[float], list[float]]:
    """wrdata's columns: time v1 time v2 -> (t, v1, v2)."""
    t, a, b = [], [], []
    for line in path.read_text().splitlines():
        p = line.split()
        if len(p) < 4:
            continue
        try:
            t.append(float(p[0]))
            a.append(float(p[1]))
            b.append(float(p[3]))
        except ValueError:
            continue
    return t, a, b


def rises(t: list[float], v: list[float], vmid: float, t_from: float) -> list[float]:
    """Rising vmid crossings after t_from, linearly interpolated."""
    out = []
    for i in range(1, len(t)):
        if v[i - 1] <= vmid < v[i] and t[i] > t_from:
            f = (vmid - v[i - 1]) / (v[i] - v[i - 1])
            out.append(t[i - 1] + f * (t[i] - t[i - 1]))
    return out


def cycle_check(path: Path, vdd: float, t_from: float = T_FROM) -> dict:
    """Every vco_div2 period holds exactly two vco_out rises."""
    if not path.exists():
        return {"trace": None}
    t, vo, vd = read_trace(path)
    ro = rises(t, vo, vdd / 2, t_from)
    rd = rises(t, vd, vdd / 2, t_from)
    counts = []
    j = 0
    for k in range(1, len(rd)):
        n = 0
        while j < len(ro) and ro[j] <= rd[k]:
            if ro[j] > rd[k - 1]:
                n += 1
            j += 1
        counts.append(n)
    per = [b - a for a, b in zip(ro, ro[1:])]
    med = sorted(per)[len(per) // 2] if per else 0.0
    res = {"stalls": sum(1 for x in per if x > 2 * med),  # periods over twice the median
           "vco_rises": len(ro), "div_rises": len(rd), "div_cycles": len(counts),
           "bad_cycles": sum(1 for c in counts if c != 2),
           "edges_per_div_cycle": sorted(set(counts)),
           "f_vco_mhz": (len(ro) - 1) / (ro[-1] - ro[0]) / 1e6 if len(ro) > 1 else 0.0,
           "f_vco_max_cycle_mhz": 1e-6 / min(per) if per else 0.0,
           "vco_out_swing_v": [round(min(vo[i] for i in range(len(t)) if t[i] > t_from), 3),
                               round(max(vo[i] for i in range(len(t)) if t[i] > t_from), 3)]
           if t else None}
    return res


def latest_extraction(ws: Path) -> Path | None:
    p = ws / "log" / "pex_pvt" / "pll_analog.pex.ordered.spice"
    if not p.exists():
        return None
    newest_src = max((f.stat().st_mtime for d in ("layout", "netlist")
                      for f in (ws / d).glob("*") if f.is_file()
                      and f.suffix in (".py", ".cir", ".spice", ".yaml", ".json")
                      and f.name != Path(__file__).name), default=0)
    return p if p.stat().st_mtime >= newest_src else None


def run(ws: Path, extracted: Path, names: list[str] | None, jobs: int, kind: str) -> dict:
    bench = BENCHES[kind]
    spec = speclib.load_spec(ws / "spec" / "spec.yaml")
    vdd_nom = spec["supply"]["vdd"]
    sweep, _ = sim_run.spec_sweep(ws)
    corners = [c for c in sweep if not names or c["name"] in names]
    cir = ws / "layout_ref" / f"{bench}.cir"
    bounds = simlib.load_bounds(ws / "layout_ref" / f"{bench}.bounds.json")
    template = cir.read_text(encoding="utf-8")
    timeout = speclib.sim_timeout(spec, "pex_sim", None, check_pex_sim.DEFAULT_TIMEOUT)
    t_root = sim_run.toolchain_root(sim_run.EDA_BIN)
    sizing = sim_run.load_sizing(ws)
    base = ws / "log" / "false_lock_pex" / bench
    netlist = extracted
    if kind == "div":
        netlist = div_netlist(extracted, base / "pll_analog_div.spice")

    def one(corner: dict) -> dict:
        out_dir = base / corner["name"]
        for old in out_dir.glob("*.txt"):
            old.unlink()
        subs = sim_run.build_subs(t_root, netlist, corner, vdd_nom, sizing)
        t0 = time.monotonic()
        r = sim_run.run_bench_at_corner(sim_run.EDA_BIN, cir.name, template, bounds,
                                        subs, corner, out_dir, timeout, check="pex_sim")
        if kind == "burst":
            for k, name in enumerate(BURST_RUNS):
                r.setdefault("cycles", {})[name] = cycle_check(
                    out_dir / f"burst_{k}.txt", float(subs.get("VDD", vdd_nom)), 400e-9)
        r["wall_s"] = round(time.monotonic() - t0)
        vdd = float(subs.get("VDD", vdd_nom))
        if kind == "burst":
            pass
        elif kind == "rail":
            r["cycles"] = {"vdd": cycle_check(out_dir / "rail_0.txt", vdd),
                           "vdd-0.1": cycle_check(out_dir / "rail_1.txt", vdd)}
        else:
            r["cycles"] = {f"{f}MHz": cycle_check(out_dir / f"div_{k}.txt", vdd,
                                                  1e-9 + 20 / (f * 1e6))
                           for k, f in enumerate(DIV_FREQS_MHZ)}
            ok = [f for f in DIV_FREQS_MHZ
                  if r["cycles"][f"{f}MHz"].get("div_cycles")
                  and not r["cycles"][f"{f}MHz"]["bad_cycles"]]
            r["div_exact_up_to_mhz"] = max(
                (f for i, f in enumerate(DIV_FREQS_MHZ) if all(
                    g in ok for g in DIV_FREQS_MHZ[:i + 1])), default=0)
        return r

    with ThreadPoolExecutor(max(1, jobs)) as pool:
        results = list(pool.map(one, corners))
    per, failing = {}, []
    for r in results:
        errs = [v for v in r["violations"] if v.get("severity") == "error"]
        scored = r.get("cycles", {})
        if kind == "div":  # the limit is the result; only 300 MHz must divide
            scored = {k: v for k, v in scored.items() if k == "300MHz"}
        bad = sum(c.get("bad_cycles") or 0 for c in scored.values())
        missing = [k for k, c in scored.items() if not c.get("div_cycles")]
        if r.get("engine_errors") or errs or bad or missing:
            failing.append({"corner": r["corner"], "msg": "; ".join(
                [str(v.get("msg"))[:160] for v in errs[:2]]
                + ([f"{bad} /2 cycles without exactly two VCO edges"] if bad else [])
                + ([f"no /2 cycles read at {missing}"] if missing else [])
                + ([str(r["engine_errors"])] if r.get("engine_errors") else []))})
        per[r["corner"]] = {"measures": r.get("measures", {}), "cycles": r.get("cycles"),
                            "wall_s": r.get("wall_s"),
                            **({"div_exact_up_to_mhz": r["div_exact_up_to_mhz"]}
                               if kind == "div" else {})}
    return {"script": "false_lock_pex", "bench": cir.name,
            "status": "pass" if corners and not failing else "fail",
            "failing_count": len(failing), "failing": failing,
            "extracted": pex_pvt.rel(extracted, ws),
            "swept": [c["name"] for c in corners], "corners": per}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--workspace", default=str(WS))
    ap.add_argument("--extracted")
    ap.add_argument("--corners", nargs="*")
    ap.add_argument("--bench", choices=sorted(BENCHES), default="rail")
    ap.add_argument("--jobs", type=int, default=max(1, min(8, (os.cpu_count() or 2) // 2)))
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    ws = Path(a.workspace).resolve()
    extracted = (Path(a.extracted).resolve() if a.extracted
                 else latest_extraction(ws) or pex_pvt.extract(ws))
    res = run(ws, extracted, a.corners, a.jobs, a.bench)
    text = json.dumps(res, indent=1, default=str)
    if a.out:
        Path(a.out).write_text(text + "\n")
    else:
        print(text)
    for n, r in res["corners"].items():
        m = " ".join(f"{k}={v:.4g}" for k, v in sorted(r["measures"].items()))
        c = " ".join(f"{k}:bad={v.get('bad_cycles')}/{v.get('div_cycles')} "
                     f"fmax_cyc={v.get('f_vco_max_cycle_mhz', 0):.1f}"
                     for k, v in (r["cycles"] or {}).items())
        print(f"{n:14} {m} {c}", file=sys.stderr)
    for f in res["failing"]:
        print(f"FAIL {f['corner']}: {f['msg']}", file=sys.stderr)
    print(f"false_lock_pex[{a.bench}]: {len(res['swept']) - res['failing_count']}"
          f"/{len(res['swept'])} corners pass", file=sys.stderr)
    return 0 if res["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
