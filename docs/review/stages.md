# The PLL, stage by stage

Every stage of the flow from spec to the Tiny Tapeout tile, each with what it
shows, its last recorded result, and how to see it work yourself. Written by
`python3 docs/review/stages.py` from each gate's report in `reports/recorded/`
and its workspace's `state.json`; don't edit it by hand. A result here is what
the last committed run of that gate found.

To re-run a gate you need chip-flow and the IIC-OSIC-TOOLS tree: in the Hive
the commands work as written. Elsewhere, put `$CHIP_FLOW_HOME/bin/eda python
$CHIP_FLOW_HOME/engine/scripts/gate.py` in place of `chip-flow gate`. The
commands without chip-flow (the RTL test, klayout, gtkwave) need only those
tools. Run them from the repository's root.

**30 of 31 gates pass on their last recorded run.** 1 fail.

## Spec and split

| gate | shows | result | what it found | run | see it yourself |
|---|---|---|---|---|---|
| spec_lint (digital) | the digital requirements are complete and each names its check | pass |  | 2026-10-31 | `blocks/pll/digital/spec/spec.md`<br>`chip-flow gate --gate spec_lint --skill vde --workspace blocks/pll/digital` |
| spec_lint (analog) | the analog spec's bounds, corners and benches are well formed | pass |  | 2026-10-30 | `blocks/pll/analog/spec/spec.md`<br>`chip-flow gate --gate spec_lint --skill ade --workspace blocks/pll/analog` |
| split (top) | the analog and digital halves agree on every crossing signal | pass | 6 signals cross the analog/digital line | 2026-10-28 | `blocks/pll/interface.yaml`<br>`chip-flow gate --gate split --skill msde --workspace blocks/pll` |

## Analog schematic (pre-layout)

| gate | shows | result | what it found | run | see it yourself |
|---|---|---|---|---|---|
| netlist_lint (analog) | the netlist parses and every device is a GF180 model | pass |  | 2026-10-31 | `blocks/pll/analog/netlist/pll_analog.cir`<br>`chip-flow gate --gate netlist_lint --skill ade --workspace blocks/pll/analog` |
| sim_tt (analog) | every bench passes at typical | pass | tt: Icp up 19.0 uA, Kvco 91.9 MHz/V | 2026-10-31 | ngspice decks in `blocks/pll/analog/tb/`<br>`chip-flow gate --gate sim_tt --skill ade --workspace blocks/pll/analog` |
| sim_pvt (analog) | every bench passes at all 31 PVT corners | pass | 187 bench runs over 31 corners, every bound met | 2026-10-31 | `blocks/pll/analog/reports/recorded/gate-sim_pvt.json` (every measure at every corner)<br>`chip-flow gate --gate sim_pvt --skill ade --workspace blocks/pll/analog` |
| bench_strength (analog) | the benches catch planted faults in the netlist | pass | 220 of 253 planted netlist faults caught; 33 too small to see, each ruled on | 2026-10-30 | `blocks/pll/analog/log/bench_strength/`<br>`chip-flow gate --gate bench_strength --skill ade --workspace blocks/pll/analog` |

## Digital RTL

| gate | shows | result | what it found | run | see it yourself |
|---|---|---|---|---|---|
| lint (digital) | the RTL compiles clean | pass |  | 2026-10-31 | `blocks/pll/digital/rtl/`<br>`chip-flow gate --gate lint --skill vde --workspace blocks/pll/digital` |
| sim (digital) | the cocotb tests of every requirement pass | pass | 18 of 18 tests pass | 2026-10-31 | `cd test && make && gtkwave tb.fst` (the Tiny Tapeout test of the top, about a second)<br>`chip-flow gate --gate sim --skill vde --workspace blocks/pll/digital` |
| holdout (digital) | tests the RTL was not written against pass | pass | 7 of 7 tests pass | 2026-10-31 | `blocks/pll/digital/holdout/`<br>`chip-flow gate --gate holdout --skill vde --workspace blocks/pll/digital` |
| cover (digital) | the tests reach every line and toggle | pass | line 100%, toggle 100% | 2026-10-31 | `chip-flow gate --gate cover --skill vde --workspace blocks/pll/digital` |
| mutate (digital) | the tests catch planted RTL faults | pass | 16 of 16 RTL mutants killed (3 equivalent, ruled) | 2026-10-31 | `chip-flow gate --gate mutate --skill vde --workspace blocks/pll/digital` |
| formal (digital) | the requirements' properties hold in the formal model | pass | 6 properties hold to depth 20, 0 proven unbounded, 8 cover points; 0 fail | 2026-10-31 | `blocks/pll/digital/formal/`<br>`chip-flow gate --gate formal --skill vde --workspace blocks/pll/digital` |

## Digital standalone hardening

| gate | shows | result | what it found | run | see it yourself |
|---|---|---|---|---|---|
| synth (digital) | the RTL synthesises to GF180 standard cells | pass | 110 cells, gf180mcu_fd_sc_mcu7t5v0 | 2026-10-31 | `chip-flow gate --gate synth --skill vde --workspace blocks/pll/digital` |
| harden (digital) | the digital half places and routes on its own | pass | 1510 instances, setup WNS 2.34 ns, hold WNS 0.51 ns | 2026-10-31 | `chip-flow gate --gate harden --skill vde --workspace blocks/pll/digital` |
| timing (digital) | setup and hold meet with the VCO clock at 2.7 ns, every STA corner | pass | worst setup 2.34 ns at max_ss_125C_3v00; hold >= 0.51 ns everywhere | 2026-10-31 | issue 8 in `blocks/pll/digital/state.json`; GOALS.md's digital issue 8 goal<br>`chip-flow gate --gate timing --skill vde --workspace blocks/pll/digital` |
| drc (digital) | the digital layout is DRC clean | pass | magic 0, klayout 0 violations | 2026-10-31 | `chip-flow gate --gate drc --skill vde --workspace blocks/pll/digital` |
| lvs (digital) | the digital layout matches its netlist | pass | layout matches the netlist | 2026-10-31 | `chip-flow gate --gate lvs --skill vde --workspace blocks/pll/digital` |
| glsim (digital) | the tests pass on the gate-level netlist, with and without delays | pass | functional 18/18, sdf 18/18 | 2026-10-31 | `chip-flow gate --gate glsim --skill vde --workspace blocks/pll/digital` |
| precheck (digital) | the standalone digital tile passes Tiny Tapeout's precheck | pass | 12 Tiny Tapeout checks run | 2026-10-31 | `blocks/pll/digital/log/precheck_run/precheck/reports/results.md`<br>`chip-flow gate --gate precheck --skill vde --workspace blocks/pll/digital` |

## Whole loop (system verification)

| gate | shows | result | what it found | run | see it yourself |
|---|---|---|---|---|---|
| cosim (top) | the digital RTL and the transistor-level analog lock together | pass | locks in 4.48 us at 100.000 MHz (P*N=16), 0 lock drops, VCO period error 0.0000 | 2026-10-28 | `blocks/pll/tb/README.md`; all three layers: `chip-flow eda python blocks/pll/tb/run_layers.py` (about 2.5 min)<br>`chip-flow gate --gate cosim --skill msde --workspace blocks/pll` |
| cosim_corners (top) | the same loop locks on the extracted analog netlist at the corners that bound its post-layout range (lowest and highest VCO ceiling and phase margin) | **FAIL** | locks at 4 of 4 bounding corners on the extracted netlist (ff_pss 6.72 us, ff_m40c_vm10 4.00 us, ff_125c_vp10 4.48 us, ss_m40c_vm10 4.96 us); vctrl within 20 mV p-p at 2 of them; measure_out_of_bounds: 'vctrl_pp_last_10us_mv' = 26.96871833615111 is outside its bound [None, 20]; test failed: test_pll_lock_nominal | 2026-10-31 | `blocks/pll/tb/README.md`; every corner's measures and vctrl trace: `blocks/pll/reports/recorded/cosim_corners.json`<br>`chip-flow eda python blocks/pll/tb/cosim_corners.py` |
| cosim_corners_gl (top) | the same corners with the hardened gate-level digital and its SDF in place of the RTL, so the PFD's reset pulse is in the loop (issue #47) | pass | locks at 4 of 4 bounding corners on the extracted netlist (ff_pss 6.72 us, ff_m40c_vm10 4.00 us, ff_125c_vp10 4.48 us, ss_m40c_vm10 5.12 us); vctrl within 20 mV p-p at 4 of them | 2026-10-31 | `blocks/pll/tb/README.md`; `blocks/pll/reports/recorded/cosim_corners_gl.json`<br>`chip-flow eda python blocks/pll/tb/cosim_gl.py` (after the vde harden) |

## Analog layout

| gate | shows | result | what it found | run | see it yourself |
|---|---|---|---|---|---|
| drc (analog) | the analog layout is DRC clean | pass | klayout: 0 violations | 2026-10-31 | `klayout blocks/pll/analog/layout/pll_analog.gds`<br>`chip-flow gate --gate drc --skill ade --workspace blocks/pll/analog` |
| lvs (analog) | the analog layout matches the signed-off netlist | pass | layout matches the netlist | 2026-10-31 | `blocks/pll/analog/layout/gen_pll_analog.py` draws it<br>`chip-flow gate --gate lvs --skill ade --workspace blocks/pll/analog` |
| pex_sim (analog) | the benches run on the extracted netlist at typical | pass | tt extracted: Icp 18.8 uA, Kvco 76.7 MHz/V, fmax 214.6 MHz; 1496 parasitic C | 2026-10-31 | `chip-flow gate --gate pex_sim --skill ade --workspace blocks/pll/analog` |
| pex_pvt (analog) | the extracted netlist meets its post-layout bounds at every corner | pass | 31 of 31 corners pass their post-layout bounds | - | every measure at every corner: `blocks/pll/analog/reports/recorded/pex_pvt.json`<br>`chip-flow eda python blocks/pll/analog/layout/pex_pvt.py --workspace blocks/pll/analog --out blocks/pll/analog/reports/recorded/pex_pvt.json` |

## Full tile (Tiny Tapeout submission shape)

| gate | shows | result | what it found | run | see it yourself |
|---|---|---|---|---|---|
| top_harden (top) | the digital half hardens around the analog macro into one tile | pass | 2350 instances around the analog macro, setup WNS 6.97 ns | 2026-10-31 | `chip-flow gate --gate top_harden --skill msde --workspace blocks/pll` |
| top_drc (top) | the whole tile is DRC clean | pass | magic 0, klayout 0 violations | 2026-10-31 | `chip-flow gate --gate top_drc --skill msde --workspace blocks/pll` |
| top_lvs (top) | the whole tile matches its netlist, analog macro included | pass | layout matches the netlist | 2026-10-31 | `blocks/pll/log/top_lvs/top_lvs.rpt` after a run<br>`chip-flow gate --gate top_lvs --skill msde --workspace blocks/pll` |
| precheck (top) | the tile passes Tiny Tapeout's precheck | pass | 12 Tiny Tapeout checks run | 2026-10-31 | `chip-flow gate --gate precheck --skill msde --workspace blocks/pll` |

## Your sign-offs

The engine stops at each sign-off for you. A pending one is not taken as
approved: the work went ahead on it pending your review, as you asked on
2026-10-29. `GOALS.md` says where each goal stands.

- analog H1 (`H1-ada9eb`): **approved** 2026-10-14, `approve H1-ada9eb`
- analog H2 (`H2-a9fad5`): **presented** 2026-10-28, waiting for your answer
