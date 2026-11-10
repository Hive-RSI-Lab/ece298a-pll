# SPDX-FileCopyrightText: © 2026 Ihsan Salari
# SPDX-License-Identifier: Apache-2.0
"""The PLL's RTL test: the Tiny Tapeout top with the real digital core and a
behavioural model of the analog macro (pll_analog_model.v, calibrated from
the transistor-level netlist at tt_27c). It shows the loop working from the
pins a user has: lock rises, and the divided VCO clock on uo[0] and the
feedback clock on uo[1] run at the frequencies 8 x N x f_ref predicts,
and the PFD's UP and DN pulses reach uo[3] and uo[4] for a scope.
The transistor-level loop is blocks/pll/tb's co-simulation."""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Timer, with_timeout
from cocotb.utils import get_sim_time

PLL_EN = 1 << 6
OBS_SEL = 1 << 7
LOCK_TIMEOUT_US = 60  # the digital spec's lock time is 50 us


async def start(dut, f_ref_mhz: float, n_sel: int, ui_extra: int = 0, trim: int = 0):
    period_ns = round(1e3 / f_ref_mhz, 3)
    cocotb.start_soon(Clock(dut.clk, period_ns, unit="ns").start())
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = trim
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 4)
    dut.rst_n.value = 1
    dut.ui_in.value = PLL_EN | ui_extra | n_sel
    t0 = get_sim_time("us")
    await with_timeout(RisingEdge(dut.lock), LOCK_TIMEOUT_US, "us")
    dut._log.info(f"{f_ref_mhz} MHz x 8 x {n_sel}: lock after {get_sim_time('us') - t0:.2f} us")


async def freq_mhz(signal, edges: int = 64) -> float:
    await RisingEdge(signal)
    t0 = get_sim_time("ns")
    for _ in range(edges):
        await RisingEdge(signal)
    return edges / (get_sim_time("ns") - t0) * 1e3


async def check_locked(dut, f_ref_mhz: float, n: int, obs_div: int = 8):
    # settle a little past the lock rise, then measure over many cycles
    await ClockCycles(dut.clk, 64)
    f_fb = await freq_mhz(dut.clk_fb, 32)
    f_obs = await freq_mhz(dut.obs_out, 32 * n)
    assert dut.lock.value == 1, "lock dropped after it rose"
    assert abs(f_fb - f_ref_mhz) / f_ref_mhz < 1e-3, f"clk_fb at {f_fb:.4f} MHz"
    want = 8 * n * f_ref_mhz / obs_div
    assert abs(f_obs - want) / want < 1e-3, f"uo[0] at {f_obs:.4f} MHz, want {want:.4f}"
    dut._log.info(f"VCO at {f_obs * obs_div:.3f} MHz (uo[0] {f_obs:.4f}, clk_fb {f_fb:.4f})")


@cocotb.test()
async def test_lock_100mhz(dut):
    """The nominal point: 6.25 MHz x 16 locks the VCO at 100 MHz."""
    await start(dut, 6.25, 2)
    await check_locked(dut, 6.25, 2)


@cocotb.test()
async def test_lock_150mhz_obs16(dut):
    """6.25 MHz x 24 (N = 3), with OBS_SEL showing the VCO / 16."""
    await start(dut, 6.25, 3, OBS_SEL)
    await check_locked(dut, 6.25, 3, obs_div=16)


@cocotb.test()
async def test_lock_100mhz_n1_trim11(dut):
    """12.5 MHz x 8 (N = 1) with the pump at its highest trim."""
    await start(dut, 12.5, 1, trim=0b11)
    await check_locked(dut, 12.5, 1)


async def count_rises(signal, window_ns: float) -> int:
    """Rising edges of a pin within a time window."""
    rises = 0

    async def count():
        nonlocal rises
        while True:
            await RisingEdge(signal)
            rises += 1

    counter = cocotb.start_soon(count())
    await Timer(window_ns, "ns")
    counter.cancel()
    return rises


@cocotb.test()
async def test_pfd_pins(dut):
    """Locked at 100 MHz, UP (uo[3]) and DN (uo[4]) each pulse once a reference
    period: the PFD's two flops set on their own edges and reset together."""
    await start(dut, 6.25, 2)
    await ClockCycles(dut.clk, 64)
    periods = 32
    window = periods * 160.0  # 6.25 MHz reference
    up = cocotb.start_soon(count_rises(dut.pfd_up, window))
    n_dn = await count_rises(dut.pfd_dn, window)
    n_up = await up
    assert abs(n_up - periods) <= 1 and abs(n_dn - periods) <= 1, \
        f"{n_up} UP and {n_dn} DN pulses in {periods} reference periods"
    assert dut.lock.value == 1, "lock dropped while the PFD pins were watched"


@cocotb.test()
async def test_disabled(dut):
    """PLL_EN low: the VCO is off, so nothing divides and lock stays low."""
    cocotb.start_soon(Clock(dut.clk, 160, unit="ns").start())
    dut.ena.value = 1
    dut.uio_in.value = 0
    dut.ui_in.value = 2
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 4)
    dut.rst_n.value = 1
    await Timer(20, "us")
    assert dut.lock.value == 0
    assert dut.clk_fb.value == 0 and dut.obs_out.value == 0, "a divided clock moved with the VCO off"
