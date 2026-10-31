# PLL loop verification (top level, `blocks/pll/tb`)

The proposal's verification plan (section 5) and GOALS.md test the whole loop
in three layers. All three run from one command:

    . $HIVE_BOX/cf.env            # or set CHIP_FLOW_HOME
    $CHIP_FLOW_HOME/bin/eda python blocks/pll/tb/run_layers.py   # ~2.5 min

| Layer | What runs | Script | Output |
|---|---|---|---|
| 1 linear model | open-loop H(s) from the calibrated Icp, Kvco, R1/C1/C2 | `pll_loop_model.py` | `reports/loop_model.json` |
| 2 RTL + calibrated model | released RTL in cocotb/Icarus, pump/filter/VCO as a behavioural ngspice model calibrated from the real netlist | `test_pll_cosim.py` with `PLL_COSIM_KIND=ideal` | `reports/cosim_measures_ideal.json` |
| 3 RTL + transistor cell (the msde `cosim` gate) | released RTL + `analog/netlist/pll_analog.cir` (GF180 models, `sizing.yaml`) in ngspice through cocotbext-ams | `check_cosim.py` on `cosim_bench.json` | `reports/cosim_measures.json` |

Calibration (run it again whenever the analog netlist or sizing changes):

    $CHIP_FLOW_HOME/bin/eda python blocks/pll/tb/calibrate_analog.py

This script measures the real cell at tt_27c in batch ngspice. It writes `pll_analog_cal.json` and regenerates
`pll_analog_ideal.sp` from it.

## Operating point and bounds

Nominal point from the brief: f_ref = 6.25 MHz, n_sel = 2 (P*N = 16), so
f_vco = 100 MHz. Also cp_trim = 00, obs_sel = 0, tt_27c, 3.3 V. rst_n and pll_en_in
are released at 320 ns. The run lasts 30 us. Bounds (`pll_cosim.bounds.json`)
come from the specs, never from results:

| Measure | Bound | Source |
|---|---|---|
| `lock_time_us` (pll_en rise to first lock rise) | <= 50 | digital REQ-LOOP-LOCK; analog spec "Out of scope here"; brief |
| `lock_drops_after_lock` | 0 | lock must hold once asserted (REQ-LOCK-*) |
| `fb_period_rel_err` (mean clk_fb period vs T_ref, last 10 us) | <= 1e-3 | REQ-LOOP-FREQ: divided frequency equals the reference |
| `vco_period_rel_err` (mean vco_out period vs T_ref/16) | <= 1e-3 | REQ-LOOP-FREQ |
| `vctrl_pp_last_10us_mv` (every 5 ns sample of the filter node) | <= 20 | REQ-LOOP-VCTRL |

## Results (2026-10-28)

Calibration of the real cell at tt_27c: Icp up/down = 19.01 / 18.66 uA (the same values as the analog
gate). The fitted filter is R1 = 27.0 kOhm (the brief's 22 k is an estimate; ppolyf_u
150 um x 2 um gives about 26 k), C1 = 20.0 pF and C2 = 2.14 pF (V2I gate included). The VCO reaches
100 MHz at vctrl = 1.634 V, with a local Kvco of 116 MHz/V there.

| | Layer 1 | Layer 2 (ideal) | Layer 3 (transistor) |
|---|---|---|---|
| lock time | settle 4/(zeta wn) = 2.2 us | 4.80 us | **4.48 us** |
| f_fb / f_vco | - | 6.2499 / 99.999 MHz | **6.250000 / 100.000 MHz** |
| vctrl at lock | - | 1.634 V, 18.3 mV p-p | 1.6341 V, 0.003 mV p-p |
| PM / fc (P*N=16, no pad) | 52.4 deg / 585 kHz (f_ref/10.7), zeta 0.71 | - | - |
| wall time | <1 s | ~10 s | ~95 s |

Layer 1 sweep: the phase margin is 55 / 52 / 47 / 43 / 40 deg at P*N = 8 / 16 / 24 / 32 / 40, and
35 deg at P*N = 16 with 5 pF on vctrl. These line up with the analog gate's .ac
numbers (49.5 / 55.3 / 35.9 deg; that gate uses the mean Kvco over the range rather than the
local slope).

## Bench notes

- The digital side is the released RTL. `tb/*.v` symlinks point into `../digital/rtl`,
  and Icarus compiles the SIM path, which has a zero-delay PFD reset. `pll_cosim_top.v` carries the
  crossing nets under their `interface.yaml` names, so the bridge binds them by
  name.
- `pll_analog_tr.sp` reorders the cell's pins into the bridge's order. It loads
  the cell, the PDK models and `sizing.yaml` (paths are resolved at run time). It leaves vctrl
  without a pad, which is the analog spec's nominal loop condition. It puts the **ua[1] pad
  capacitance (5 pF) on bias_ref**. Without any capacitance on bias_ref,
  the bias reference relaxes after pll_en rises (see OPEN in the integrator report).
  The decks that show this are in `log/scratch/bias/`.
- Two bench-side fixes to cocotbext-ams, both in `test_pll_cosim.py`. Neither changes what the bridge
  measures:
  1. *Sync rounding.* The stock sync callback clamps ngspice's step to
     `next_sync - t`. When `t` lands one float rounding short (about 1e-25 s), the clamp
     produces "Timestep too small" and the transient aborts. This is the open quirk in
     `docs/spikes/dcosim.md`. A remainder under 1 fs now counts as reached.
  2. *Write on change.* The stock bridge re-forces vco_out at every sync. Doing that
     at 1 ns syncs crashed vvp (SIGSEGV) after a few hundred forces. vco_out is now
     a reg that is written only when its digitized value changes.
  There is also one timing refinement: a sync is placed 2 ps after every clk rising edge, so
  a PFD edge launched by the reference reaches the pump at once rather than up
  to one sync interval (1 ns) late.
- Resolution: digital edge times sit on the bridge's sync grid (at most 1 ns). Over
  the 10 us window that limits the period measures to about 1e-4, which is ten times finer than
  their 1e-3 bound.
- With the zero-delay RTL PFD there is a dead zone. Once locked, the pump gets
  almost no charge, so vctrl sits flat. The reset-pulse width only exists in the
  gate-level netlist, which this bench does not simulate.
- Not covered yet: other (f_ref, N) points, relock after a change of N, and
  the vctrl pad cap. The bench takes them as parameters (`pll_tb_common.py`,
  `calibrate_analog.py --corner`), but only the nominal point is gated.
  The corners are run on the extracted netlist by `cosim_corners.py` (below).
- Debug knobs, which are not used by the gate: `PLL_COSIM_DURATION_NS`,
  `PLL_COSIM_ANALOG_VCD=<file>` with `PLL_COSIM_DEBUG_NODES=x1.xpll.vref,...`.

## The loop on the extracted netlist at the corners that bound its range (2026-10-30)

`cosim_corners.py` runs layer 3's bench (`test_pll_cosim.py`, same 100 MHz
point, same bounds and evidence checks as the cosim gate) with the cell
swapped for the layout's parasitic extraction
(`analog/log/pex_pvt/pll_analog.pex.ordered.spice`, extracted when missing)
and the PDK corner, temperature and supply moved to each corner. The bench
reads the move from `PLL_COSIM_SETUP` and the gate never sets it. The
corners are the ones that bound the post-layout sweep
(`analog/reports/recorded/pex_pvt.json`; `bounding_corners()`):

    $CHIP_FLOW_HOME/bin/eda python blocks/pll/tb/cosim_corners.py   # ~90 min, 4 corners side by side

A corner takes about 90 minutes of wall time with four side by side at the
0.25 ns sync (about 180 s per simulated us, against 3 s for the schematic cell). The result is
recorded in `../reports/recorded/cosim_corners.json` with a hash of every
input. `tests/score.py` counts it only while those hashes hold, as it does
bench_strength's. `--from-logs` rewrites that report from the last run's
`log/cosim_corners/<corner>/result.json` without running anything.

| Corner | Why it bounds the range | Lock | f_vco (MHz) | vctrl (V) | vctrl p-p, last 10 us, 5 ns samples (mV) |
|---|---|---|---|---|---|
| ff_pss | lowest ceiling 126.4 MHz, lowest Kvco 39.9 MHz/V, lowest Icp 13.6 uA | 6.72 us, held | 100.0000 | 2.207 | 15.5 (0.25 ns sync; 1 ns: **20.9**) |
| ff_m40c_vm10 | highest ceiling 299.5 MHz | 4.00 us, held | 100.0000 | 1.445 | 0.6 (0.25 ns sync; 1 ns: **27.4**) |
| ff_125c_vp10 | lowest phase margin 34.5 deg | 4.48 us, held | 100.0000 | 1.775 | 11.3 (0.25 ns sync; 1 ns: 16.2) |
| ss_m40c_vm10 | highest phase margin 52.9 deg | 4.96 us, held | 99.9999 | 1.804 | 0.2 (0.25 ns sync; 1 ns: 17.4) |

The loop locks and holds at all four corners: lock rises within 7 us, never
falls, f_fb and f_vco are within 5e-7 of their targets (bound 1e-3), and
vctrl stays within REQ-LOOP-VCTRL's 20 mV p-p at every corner (15.5 mV worst,
ff_pss). These runs use a 0.25 ns bridge fallback sync (`MAX_SYNC_NS` in
`cosim_corners.py`, passed to the bench as `PLL_COSIM_MAX_SYNC_NS`). The cosim
gate keeps 1 ns. At 1 ns two corners missed the limit (20.9 mV at ff_pss,
27.4 mV at ff_m40c_vm10). There vctrl was flat apart from isolated
+-15-20 mV kicks, one every 0.8-2.4 us: pump correction pulses seen through
R1, fired by PFD edges quantised to the 1 ns grid. At 0.25 ns those kicks go
(ff_m40c_vm10: 27.4 -> 0.6 mV), so they came from the bench, not the loop.
A corner now takes about 90 minutes of wall time with 4 side by side.
Still open: other (f_ref, N) points at these corners, and the gate-level PFD's
reset pulse.

## Prescaler margin at ss_pff (digital issue 8, 2026-10-29)

`prescaler_margin.py` is not a layer and not a gate. It asks how fast the
first /2 prescaler stage has to be at the corner where the VCO is fastest
against slow digital: ss_pff (ss transistors, fast passives, 125 C, 2.97 V).
It steps a behavioural loop built from `pll_analog_cal_ss_pff.json`, which
`calibrate_analog.py --corner ss_pff` measured on the real netlist. The
model's first stage drops a VCO edge whenever its toggle loop (t_lim) has
not finished since the last toggle. Output: `../reports/prescaler_margin.json`.

    $CHIP_FLOW_HOME/bin/eda python blocks/pll/tb/prescaler_margin.py [--t-lim-ns 3.5]   # ~40 s

Results:
- **Acquisition overshoots.** From vctrl = 0 the VCO peaks at 254 / 280 /
  243 MHz on the way to the 200 MHz points (6.25 MHz x 4, 5 MHz x 5,
  12.5 MHz x 2). The ideal model overshoots more than the transistor cell
  does at tt (145 vs 129 MHz peak for 100 MHz), so these peaks err high.
- **The old prescaler locked up.** The hardened dffrnq_4 loop handled about
  238 MHz at ss (t_lim 4.2 ns). At that speed all three 200 MHz points
  overshoot, the first stage drops edges, clk_fb looks slow, and vctrl runs
  to the rail (310 MHz) and stays there. A loop of 3.65 ns or faster locks at
  every point; at 3.68 ns the 5 MHz x 5 point (peak about 283 MHz) no
  longer does. The new hand-placed dffrnq_2 + inv_1 stage is 3.65 ns at ss
  after routing (STA, without the 0.25 ns uncertainty), so that point has no
  margin before layout. REQ-TIM-VCO holds stage 0 to 3.65 ns at ss.
- **A start at the rail never recovers by itself.** Only a stage that keeps
  up with 310 MHz (t_lim under 3.2 ns, which no library flop reaches at ss)
  would get out. Otherwise the 200 MHz points sit at 310 MHz for good, and
  nothing in the analog cell discharges vctrl when pll_en goes low. With the
  digital's recovery (REQ-RECOVER: 1024 unlocked reference cycles, then 128
  cycles of DN), 6.25 MHz x 4 and 12.5 MHz x 2 lock after one recovery (189
  and 95 us) with a 3.65 ns stage. 5 MHz x 5 overshoots past the stage again
  after the recovery and keeps cycling: it is the point with no margin.
- **False lock from the rail.** 6.25 MHz x 3 started at the rail locks at
  300 MHz, not 150. A stage that drops every other edge divides by 4, and
  that fits the loop exactly, so lock rises and recovery never fires. The
  model's stage drops edges cleanly; a real overclocked flop is messier.
  Either way the cure is a VCO that cannot outrun the stage.
- **Post-layout.** These numbers are the pre-layout netlist's. The
  post-layout corner sweep (task 261029-062920, not merged at the time of
  writing) puts the extracted VCO at ss_pff at 240 MHz with vctrl at the
  rail, and 266 MHz at its fastest corner. Both are below the stage's
  274 MHz, and if they hold, none of the cases above can happen on silicon.
  Rerun this script with a post-layout calibration once that lands.
