#!/usr/bin/env python
"""false_lock_cosim.py - the closed loop started from the rail on the extracted cell.

    $CHIP_FLOW_HOME/bin/eda python blocks/pll/tb/false_lock_cosim.py \
        [--points CORNER:N ...] [--vctrl0 V|vdd] [--jobs N] [--out FILE]

verify.html claim 1.7: if vctrl starts at (or is kicked to) VDD, the VCO
runs at its ceiling, and if the TSPC /2 or the prescaler dropped edges there
the divider would see a slow clock, the PFD would keep pumping up, and the
loop would sit at the rail (a false lock near 300 MHz). false_lock_pex.py
showed the /2 clean at the rail open loop; this closes the loop.

It runs cosim_corners.py's bench (test_pll_cosim.py, the released RTL, the
layout's extraction with bias_ref on its 5 pF pad cap, the PDK corner,
temperature and supply of each corner) with three changes, all through
PLL_COSIM_SETUP: N is set from reset (n_sel0), the N 2->3 step is off
(relock_ns 0), and vctrl and the loop filter's other plate start at VDD.
The preset is a switch from vctrl to VDD in a wrapper subckt of this
script's own (preset_lines, written to the run's work directory), closed while pll_en is low (the release moves
from 320 ns to 10 us so C1 charges through R1 too) and opened 20 ns before
pll_en rises. A .ic does not do it: the filter's MOS caps are charge-form
and drop to 0 V at t=0 under uic.

A point passes when lock rises within 50 us and never falls, and over the
last 10 us f_fb and f_vco are within 0.1 % of f_ref and P*N*f_ref - the
right frequency, not the rail. Writes reports/recorded/false_lock_cosim.json.
"""
from __future__ import annotations

import argparse
import importlib.util
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

# tb/cosim_corners.py under its own name: chip-flow's check_cosim imports
# a module called cosim_corners of its own, which this one must not shadow
_spec = importlib.util.spec_from_file_location("pll_cosim_corners", HERE / "cosim_corners.py")
CC = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CC)

OUT = HERE.parent / "reports" / "recorded" / "false_lock_cosim.json"
# ss_pff: the lowest ceiling with the 150 MHz point the closest to it (the
# brief's point); ff_m40c_vm10: the highest ceiling, the fastest the /2 sees.
POINTS = ["ss_pff:3", "ff_m40c_vm10:3", "ss_pff:2", "ff_m40c_vm10:2"]
SUBCKT = "pll_analog_cosim_preset"
# pll_en rises at RELEASE_NS: long enough for C1 to reach the preset through
# R1 (about 75 kOhm x 20 pF); the switch opens HOLD_GAP_NS before
RELEASE_NS = float(os.environ.get("PLL_FALSE_LOCK_RELEASE_NS", "10000"))  # override: smoke only
HOLD_GAP_NS = 20.0
RUN_NS = 30_000.0                  # after the release, as the gate's run


def preset_lines(v: float, hold_ns: float) -> list[str]:
    """pll_analog_cosim (pll_analog_tr.sp) plus a switch that ties vctrl to v
    until hold_ns, then opens. The loop filter's MOS caps are charge-form
    (pll_tb_common.MOSCAP_Q) and take no .ic under uic, so vctrl and C1
    (through R1, about 1.5 us) are charged for real while pll_en is low."""
    return [f".subckt {SUBCKT} pfd_up pfd_dn pll_en cp_trim0 cp_trim1 vco_div2 vdd vss",
            "xpll vco_div2 pfd_up pfd_dn pll_en cp_trim0 cp_trim1 vctrl bias_ref vdd vss pll_analog_ua",
            "cload vco_div2 vss 30f",
            "cpad_bias bias_ref vss 5p",
            f"vpre_src vpre vss dc {v:.4f}",
            f"vpre_ctl ctl vss pwl(0 1 {hold_ns:.1f}n 1 {hold_ns + 1:.1f}n 0)",
            "spre vctrl vpre ctl vss swpre",
            ".model swpre sw vt=0.5 vh=0.1 ron=100 roff=1e15",
            f".ends {SUBCKT}"]


def judge(m: dict | None) -> list[str]:
    if not m:
        return ["no measures"]
    why = []
    lt, drops = m.get("lock_time_us"), m.get("lock_drops_after_lock")
    if not isinstance(lt, (int, float)) or lt > 50:
        why.append(f"lock_time_us {lt}")
    if drops != 0:
        why.append(f"lock_drops_after_lock {drops}")
    if m.get("window_after_lock") is not True:
        why.append("window not after lock")
    for k in ("fb_period_rel_err", "vco_period_rel_err"):
        e = m.get(k)
        if not isinstance(e, (int, float)) or e > 1e-3:
            why.append(f"{k} {e}")
    if m.get("bridge_error"):
        why.append(f"bridge_error {m['bridge_error'][:150]}")
    return why


def worker(point: str, extracted: Path, work: Path, timeout_s: float, vctrl0: str) -> dict:
    corner, n = point.split(":")
    base = CC.setup_for

    def setup_for(c, ex, out):
        s = base(c, ex, out)
        v = s["vdd"] if vctrl0 == "vdd" else float(vctrl0)
        wrap = work / "pll_analog_preset.sp"
        wrap.write_text("\n".join([f"* {SUBCKT}: written by false_lock_cosim.py",
                                    f".include '{HERE / 'pll_analog_tr.sp'}'"]
                                   + preset_lines(v, RELEASE_NS - HOLD_GAP_NS)) + "\n")
        s.update(n_sel0=int(n), relock_ns=0, vctrl0=v, release_ns=RELEASE_NS, subckt=SUBCKT,
                 spice_file=str(wrap))
        return s

    CC.setup_for = setup_for
    os.environ.setdefault("PLL_COSIM_DURATION_NS", str(RELEASE_NS + RUN_NS))
    res = CC.run_one(corner, extracted, work, timeout_s)
    return summarize(point, work, res)


def summarize(point: str, work: Path, res: dict | None = None) -> dict:
    """One point's result from its work directory (measures.json)."""
    corner, n = point.split(":")
    res = res or {}
    meas = json.loads((work / "measures.json").read_text()) if (work / "measures.json").is_file() else None
    keep = ["lock_time_us", "lock_drops_after_lock", "lock_rises", "window_after_lock",
            "fb_period_rel_err", "vco_period_rel_err", "fb_freq_hz", "vco_freq_hz",
            "vctrl_final_v", "vctrl_mean_window_v", "vctrl_pp_last_10us_mv",
            "static_phase_offset_ns", "vco_min_period_ns_after_en", "vco_short_pulses_after_en",
            "spice_time_reached_ns", "bridge_error", "operating_point", "vctrl_trace_us_v"]
    m = {k: meas.get(k) for k in keep} if meas else None
    if m and m.get("vctrl_trace_us_v"):
        tr = m["vctrl_trace_us_v"]
        m["vctrl_at_start_v"] = tr[0][1]
        m["vctrl_at_release_v"] = min(tr, key=lambda p: abs(p[0] - RELEASE_NS / 1000))[1]
    why = judge(m)
    # the gate's own bounds, for context (relock is off here, so it is never met)
    return {"point": point, "corner": corner, "n_sel": int(n), "status": "fail" if why else "pass",
            "why": why, "gate_why": res.get("why"), "wall_s": res.get("wall_s"), "measures": m}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--points", nargs="*", default=POINTS, help="CORNER:N_SEL")
    ap.add_argument("--vctrl0", default="vdd", help="vctrl and vfilt at start: vdd or volts")
    ap.add_argument("--extracted", help="default: cosim_corners' extraction")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--timeout-s", type=float, default=CC.TIMEOUT_S)
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--collect", action="store_true",
                    help="no sims: rebuild the report from the points' work directories "
                         "(a run stopped by its time limit still leaves measures.json)")
    ap.add_argument("--one", help=argparse.SUPPRESS)
    ap.add_argument("--work", help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    extracted = Path(a.extracted).resolve() if a.extracted else CC.EXTRACTED

    if a.one:
        res = worker(a.one, extracted, Path(a.work), a.timeout_s, a.vctrl0)
        Path(a.out).write_text(json.dumps(res, indent=1, default=str))
        return 0 if res["status"] == "pass" else 1

    if not extracted.is_file():
        extracted = CC.extract()
    root = C.WS / "log" / "false_lock_cosim"

    def one(p: str) -> dict:
        work = root / p.replace(":", "_n")
        if a.collect:
            res = summarize(p, work) if (work / "measures.json").is_file() else \
                {"point": p, "status": "fail", "why": ["no measures.json"], "measures": None}
            m = res.get("measures") or {}
            print(f"{p:18} {res['status']:4} lock {m.get('lock_time_us')} us, f_vco "
                  f"{(m.get('vco_freq_hz') or 0) / 1e6:.4f} MHz, spice reached "
                  f"{m.get('spice_time_reached_ns')} ns" + "".join(f"\n    {w}" for w in res["why"]))
            return res
        work.mkdir(parents=True, exist_ok=True)
        res_path = work / "result.json"
        res_path.unlink(missing_ok=True)
        cmd = [sys.executable, str(Path(__file__).resolve()), "--one", p, "--extracted",
               str(extracted), "--work", str(work), "--timeout-s", str(a.timeout_s),
               "--vctrl0", a.vctrl0, "--out", str(res_path)]
        with (work / "run.log").open("w") as f:
            try:
                subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                               timeout=a.timeout_s + 300)
            except subprocess.TimeoutExpired:
                pass
        try:
            res = json.loads(res_path.read_text())
        except (OSError, ValueError):
            res = {"point": p, "status": "fail", "why": ["no result"], "measures": None}
        m = res.get("measures") or {}
        print(f"{p:18} {res['status']:4} lock {m.get('lock_time_us')} us, f_vco "
              f"{(m.get('vco_freq_hz') or 0) / 1e6:.4f} MHz, vctrl at release "
              f"{m.get('vctrl_at_release_v')} V, end {m.get('vctrl_final_v')} V"
              + "".join(f"\n    {w}" for w in res.get("why") or []), flush=True)
        return res

    with ThreadPoolExecutor(max(1, a.jobs)) as pool:
        results = list(pool.map(one, a.points))
    passed = [r["point"] for r in results if r["status"] == "pass"]
    rep = {"script": "false_lock_cosim",
           "status": "pass" if len(passed) == len(results) else "fail",
           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "facts": {"passed": passed, "points": a.points, "vctrl0": a.vctrl0,
                     "release_ns": RELEASE_NS, "run_ns_planned": RUN_NS, "collected": a.collect,
                     "extracted": str(extracted.relative_to(C.WS)) if extracted.is_relative_to(C.WS)
                     else str(extracted),
                     "results": results},
           "inputs": CC.input_hashes()}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(rep, indent=1, default=str) + "\n")
    print(f"false_lock_cosim: {len(passed)}/{len(results)} points lock at P*N*f_ref -> {a.out}")
    return 0 if rep["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
