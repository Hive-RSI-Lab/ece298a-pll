"""Closed-loop coverage bench: other divider settings and re-lock after a
change of N, on the same cell, bridge and digital as test_pll_cosim.py
(cosim_cov.py runs it with the extracted cell and the gate-level digital).

PLL_COV_PLAN (json, set by cosim_cov.py) gives
  {"f_ref_hz": 5e6, "segments": [[t_ns, n_sel], ...], "duration_ns": ...}
n_sel starts at segments[0] and changes at each later t_ns while the loop
runs (n_sel is quasi-static in the RTL; it is changed on a clk falling edge,
away from the reference edge). PLL_COSIM_SETUP moves the cell to a corner,
as in test_pll_cosim.py.

Per segment (ending at the next change or the run's end), measured on its
last SETTLE_NS:
  lock_rise_after_change_us  first lock rise after the segment starts
  locked_at_end              lock high and no lock fall in the window
  fb_period_rel_err          |mean clk_fb period - T_ref| / T_ref
  vco_period_rel_err         |mean VCO period - T_ref/(8N)| / (T_ref/(8N))
  vctrl_pp_mv, vctrl_mean_v
A segment passes when it locks within the segment, holds lock over the
window, and both period errors are <= 0.1 % (test_pll_cosim.py's bounds).
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, Timer
from cocotbext.ams import AnalogBlock, DigitalPin

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import pll_tb_common as C  # noqa: E402
import test_pll_cosim as T  # noqa: E402  (a module object: cocotb does not collect its test)

SETTLE_NS = 4000.0


@cocotb.test()
async def test_pll_cov(dut):
    plan = json.loads(os.environ["PLL_COV_PLAN"])
    setup = json.loads(os.environ["PLL_COSIM_SETUP"])
    t_ref = 1e9 / float(plan["f_ref_hz"])
    segs = [(float(t), int(n)) for t, n in plan["segments"]]
    duration = float(plan["duration_ns"])
    extra = list(setup["lines"]) + [".save v(x1.vctrl)", ".options reltol=1e-3"]
    vdd = float(setup["vdd"])
    pin = dict(vdd=vdd, vss=0.0)
    block = AnalogBlock(
        name="pll_analog", spice_file=str(HERE.parent / "pll_analog_tr.sp"),
        subcircuit="pll_analog_cosim",
        digital_pins={"pfd_up": DigitalPin(direction="input", **pin),
                      "pfd_dn": DigitalPin(direction="input", **pin),
                      "pll_en": DigitalPin(direction="input", **pin),
                      "cp_trim0": DigitalPin(direction="input", **pin),
                      "cp_trim1": DigitalPin(direction="input", **pin),
                      "vco_div2": DigitalPin(direction="output", **pin)},
        vdd=vdd, vss=0.0, tran_step="50p", extra_lines=extra)
    dut.rst_n.value = 0
    dut.pll_en_in.value = 0
    dut.n_sel.value = segs[0][1]
    dut.obs_sel.value = 0
    dut.cp_trim_in.value = 0
    dut.clk.value = 0
    await Timer(1, unit="ns")
    bridge = T.Bridge(dut, [block], max_sync_interval_ns=T.MAX_SYNC_NS,
                      simulator_lib=T.LIBNGSPICE)
    t_clk0 = cocotb.utils.get_sim_time(unit="ns")
    cocotb.start_soon(Clock(dut.clk, t_ref, unit="ns").start())
    bridge.ref_grid = (t_clk0 * 1e-9, t_ref * 1e-9, T.REF_SYNC_LAG_NS * 1e-9)
    fb = T.Edges(dut.clk_fb)
    vco = T.Edges(dut.vco_div2, falls=True)
    en = T.Edges(dut.pll_en)
    lock = T.Edges(dut.lock, falls=True)
    vctrl: list[tuple[float, float]] = []
    changes: list[float] = []

    async def sample_vctrl():
        while True:
            await Timer(5, unit="ns")
            if bridge._sim is not None:
                v = bridge._sim._node_voltages.get("x1.vctrl")
                if v is not None:
                    vctrl.append((cocotb.utils.get_sim_time(unit="ns"), v))

    async def release():
        await Timer(T.RELEASE_NS - 1, unit="ns")
        dut.rst_n.value = 1
        dut.pll_en_in.value = 1

    async def step_n():
        for t, n in segs[1:]:
            now = cocotb.utils.get_sim_time(unit="ns")
            await Timer(max(1.0, t - now), unit="ns")
            await FallingEdge(dut.clk)
            dut.n_sel.value = n
            changes.append(cocotb.utils.get_sim_time(unit="ns"))
            dut._log.info("n_sel -> %d at %.0f ns", n, changes[-1])

    async def progress():
        t0 = time.monotonic()
        while True:
            await Timer(1000, unit="ns")
            v = vctrl[-1][1] if vctrl else float("nan")
            dut._log.info("progress: %.0f ns, %.0f s wall, vctrl %.4f V, lock %s",
                          cocotb.utils.get_sim_time(unit="ns"), time.monotonic() - t0, v,
                          dut.lock.value)

    for co in (sample_vctrl(), release(), step_n(), progress()):
        cocotb.start_soon(co)
    err = None
    try:
        await bridge.start(duration_ns=duration)
    except Exception as exc:  # noqa: BLE001
        err = exc
    finally:
        spice_ns = bridge._last_sync_spice_time * 1e9
        t_end = min(spice_ns, cocotb.utils.get_sim_time(unit="ns"))
        t_en = en.rises[0] if en.rises else None
        starts = [t_en if t_en is not None else 0.0] + changes
        ends = changes + [t_end]
        out = []
        for i, (s, e) in enumerate(zip(starts, ends)):
            n = segs[i][1]
            pn = C.P * n
            w0 = max(s, e - SETTLE_NS)
            rises = [t for t in lock.rises if s < t <= e]
            falls_w = [t for t in lock.falls if w0 <= t <= e]
            fb_t = T.mean_period([t for t in fb.rises if w0 <= t <= e])
            vco_t = T.mean_period([t for t in vco.rises if w0 <= t <= e])
            vco_t = vco_t / 2 if vco_t else None
            vc = [v for t, v in vctrl if w0 <= t <= e]
            last_rise = max([t for t in lock.rises if t <= e], default=None)
            last_fall = max([t for t in lock.falls if t <= e], default=None)
            locked_end = last_rise is not None and (last_fall is None or last_rise > last_fall) \
                and not falls_w and last_rise <= w0
            seg = {"n_sel": n, "p_times_n": pn, "f_vco_target_mhz": pn * 1e3 / t_ref,
                   "start_ns": s, "end_ns": e, "window_ns": [w0, e],
                   "lock_rise_after_change_us": (rises[0] - s) / 1000 if rises else None,
                   "lock_falls_in_segment": len([t for t in lock.falls if s < t <= e]),
                   "locked_at_end": locked_end,
                   "fb_period_rel_err": T.rel_err(fb_t, t_ref),
                   "vco_period_rel_err": T.rel_err(vco_t, t_ref / pn),
                   "vco_freq_mhz": 1e3 / vco_t if vco_t else None,
                   "vctrl_pp_mv": (max(vc) - min(vc)) * 1e3 if len(vc) > 1 else None,
                   "vctrl_mean_v": sum(vc) / len(vc) if vc else None}
            seg["pass"] = bool(locked_end and seg["fb_period_rel_err"] is not None
                               and seg["fb_period_rel_err"] <= 1e-3
                               and seg["vco_period_rel_err"] is not None
                               and seg["vco_period_rel_err"] <= 1e-3)
            out.append(seg)
        res = {"plan": plan, "corner": setup["corner"], "vdd": vdd, "segments": out,
               "bridge_error": repr(err) if err else None, "spice_time_reached_ns": spice_ns,
               "lock_rises_ns": lock.rises, "lock_falls_ns": lock.falls,
               "vctrl_trace_us_v": [[round(t / 1000, 4), round(v, 5)] for t, v in vctrl[::40]]}
        Path(setup["out"]).write_text(json.dumps(res, indent=1))
        await bridge.stop()
    if err is not None:
        raise err
    bad = [f"segment {i} (N={s['n_sel']})" for i, s in enumerate(out) if not s["pass"]]
    assert not bad, "not locked at the right frequency: " + ", ".join(bad)
