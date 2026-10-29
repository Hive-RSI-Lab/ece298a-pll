# ece298a-pll goals

This repository is the term project of ECE 298A (Integrated Circuit Design and Tapeout) at the University of Waterloo: a charge-pump PLL for one Tiny Tapeout tile on GF180, with a divide-by-8 prescaler and a programmable feedback divider. Its analog half (the bias, the charge pump, the loop filter and the ring VCO) lives in `blocks/pll/analog`, its digital half (the phase-frequency detector, the dividers, the lock detector and the control registers) in `blocks/pll/digital`, and the two meet in `blocks/pll/interface.yaml`. `bash tests/check.sh` is the fast check every pull request has to pass. This is coursework, so runs never submit anything to a course system.

## Proposed goals

Filed by runs. Each says what done looks like as something a run can check, and keeps its status (open, done, failed, dropped) with the pull requests that moved it. At most three are open at once.

### Sign off the PLL's analog half and close what it carries into layout

- **Status:** done 2026-10-29. The owner approved H1-ada9eb, recorded in `blocks/pll/analog/log/H1-signoff.md` (4c90ceb). On 2026-10-28 every analog item closed (#6): the spec sweeps `ss_pff` and `ff_pss` (31 corners), scores `vco_fmax_ff_mhz` at every corner against 150..370 MHz, carries a written jitter estimate in place of the measure that never printed, and corrects the mislabelled 331.75 MHz. spec_lint, sim_pvt and bench_strength pass on it. The digital timing at about 2.7 ns, which this goal's done-line also asked for, is its own goal now (digital issue 8, below), so this one closes on its analog work.
- **What:** The analog half has passed every pre-layout check over 29 simulation corners (spec lint, netlist lint, the typical and PVT simulations, and the bench-strength check), and its layout waits on the owner's sign-off. That sign-off decides whether the analog netlist, the spec it is checked against and those results are frozen as the reference layout has to match. It also accepts two changes made since the proposal: wider charge-pump current windows, and a phase-margin floor of 30 degrees scored at every corner. The [review](https://github.com/ihsan-sa/ece298a/blob/main/docs/pll-h1-review.md) sets out the results, the thin margins and the open items. The sign-off has been asked for, and the owner's answer arrives as an ask. A run records that answer as they gave it; it never approves the sign-off itself, and it changes nothing under `blocks/pll/analog` until the answer is recorded. If they approve, the run closes the open items: it puts the two resistor-skew corners (`ss_pff`, `ff_pss`) back into the spec, scores the VCO's 333 MHz ceiling at every corner (the VCO reaches about 363 MHz at fast, cold, low supply with its control voltage at the rail), corrects the frequency that the spec's sign-off note mislabels, and reruns the analog checks. If they reject it, the run reworks the design against their reason and asks again.
- **Done when:** the owner's answer is recorded as the analog sign-off in this repository. If they approved, the analog spec also scores both skew corners and the VCO ceiling at every corner, and the analog spec lint, PVT simulation and bench-strength checks pass on that spec.

### Close digital issue 8: the digital half meets timing with the VCO clock at about 2.7 ns

- **Status:** open (split out of the analog sign-off 2026-10-29). Issue 8 is the -1.50 ns setup miss at ss_125C_3v00 on the /2 prescaler loop once the digital side is timed with the VCO clock at 2.7 ns. It was decided on 2026-10-29 (task 261029-082850, #15), digital-only. The /2 stage is now a hand-placed dffrnq_2 + inv_1, 274 MHz at ss after routing (it was 238 MHz). A recovery forces DN after 1024 unlocked reference cycles. The ss corner at 2.7 ns is waived with its numbers in `blocks/pll/digital/state.json` issue 8, because no library flop toggles at 2.7 ns at ss. Ss setup is still -1.2 ns, tt +0.65, ff +1.43. The loop model at `ss_pff` (`blocks/pll/tb/README.md`) shows the old stage locking every 200 MHz point at the rail, and the new one acquiring every point; 5 MHz x 5 has no margin pre-layout. The post-layout VCO (task 261029-062920, #14) tops out at 110-266 MHz over the corners, below the stage's 274 MHz at every one. The owner should review the waiver.
- **What:** The analog spec lets the VCO run up to 370 MHz (2.7 ns), and the first prescaler stage has to toggle at whatever the VCO reaches, or the feedback divider miscounts and the loop runs away to the rail. Make the digital half meet timing with `vco_out` constrained at about 2.7 ns at every STA corner. Until it does, the ss waiver stands with its numbers, and it is revisited if the post-layout VCO's ss ceiling passes about 270 MHz. This changes nothing under `blocks/pll/analog`.
- **Done when:** the digital timing check passes with the VCO clock at about 2.7 ns, setup and hold met at every STA corner.

### Test the whole PLL loop in co-simulation

- **Status:** done 2026-10-28. `python blocks/pll/tb/run_layers.py` runs the linear model, the RTL with a calibrated behavioural cell, and the RTL with the transistor-level analog netlist through cocotbext-ams. The last of these is the `cosim` gate, which passes: lock in 4.48 us at 6.25 MHz x 16, VCO at 100.000 MHz, with the lock detector held. `blocks/pll/tb/README.md` writes it up. Only the nominal point is gated.
- **What:** The course grades a system verification of the term project. The proposal (`blocks/pll/brief/proposal-classic-pll.md`) tests the loop as a whole in three layers: a linear model of the loop, the real digital RTL in cocotb with Python models of the pump, filter and VCO calibrated from the analog benches, and a mixed-signal co-simulation of the digital RTL with the analog netlist. Build those benches under `blocks/pll` and run them. This reads the analog half but does not change it, so it can go ahead while the sign-off above is pending.
- **Done when:** the three layers run from one command in this repository, the co-simulation shows the loop locking at the 100 MHz nominal point with the lock detector asserting, and the result is written up next to the benches.

### Lay out the analog half and match it after extraction

- **Status:** open (moved up 2026-10-28). `blocks/pll/analog/layout/gen_pll_analog.py` passes drc (0) and lvs (unique match). On 2026-10-29 the post-layout bench runs at every corner the spec scores: `layout/pex_pvt.py` runs `layout_ref/pll_analog_pex_pvt_tb.cir` (the pex bench with the corner left open, bounds = spec.yaml post_layout_bounds) through the engine's sim_run at all 31 corners on the extracted netlist. 29 of 31 pass. Two miss: at tt_27c the VCO reads 196 MHz at vctrl = vdd-0.3 V against the 200 MHz floor, and at ff_pss Kvco is 35 MHz/V against 40. The 226 MHz recorded at typical before was optimistic: magic's parasitic extraction dropped the coupling capacitance of every unlabelled net, about half the wire C on the ring nodes, so the generator now labels every routed internal net. Post-layout the VCO's ceiling (vctrl = vdd) is 110-266 MHz over the corners, below the pre-layout 150 MHz floor at ff_pss (110 MHz) and right at it at ss_125c_vp10 (150.0) and tt_125c_vp10 (151.0). Started from pll_en rising with no kick (`layout_ref/pll_analog_pex_start_tb.cir`), the extracted ring runs at all 31 corners with vctrl at vdd-0.3 V, but not with vctrl at 0.3 V at ff_125c (all three supplies) or ss_m40c_vm10. H2 is presented as challenge H2-a9fad5 and waits for the owner.
- **What:** Once the analog sign-off is recorded with the owner's approval, draw the layout of the analog half, pass DRC and LVS against the signed-off netlist, extract its parasitics, and rerun the analog benches on the extracted netlist against the spec's post-layout bounds. Matching, the charge pump's mirrors and the VCO ring's symmetry are the places where layout can eat the thin margins the review lists.
- **Done when:** DRC and LVS pass on the analog layout, and every analog bench passes its post-layout bounds on the extracted netlist at every corner the spec scores.

### Harden the tile and pass the Tiny Tapeout precheck

- **Status:** open (moved up from Later 2026-10-29; work on it had already started). The first top_harden attempt (2026-10-28) was refused by the engine: an msde top with two clock domains gets no constraints.sdc, and the engine rebuilds `top/` on every run. That fix landed in hive-chip-flow (task 261028-231313-dc59cc1ce9). Top LVS then found `vctrl` shorted to VGND at the analog macro's pin; the short is made by chip-flow's top_harden (its supply pins cross the MIM caps), so the PLL's task 261029-115210 is blocked on the chip-flow fix, carried by hive-chip-flow task 261029-152848-41539943b1.
- **What:** With the analog layout done, harden the digital half around the analog macro into one tile, run full-tile DRC and LVS, and pass the Tiny Tapeout precheck. Replace the template placeholder in `src/` and the template README with the real design, so the Tiny Tapeout gds, docs and test workflows build and test this design rather than the template.
- **Done when:** the tile hardens with no DRC or LVS errors, the Tiny Tapeout precheck passes, and the gds, docs and test workflows pass on main with the real design in `src/`.

## Later

Goals waiting for an open slot. When a proposed goal closes, the run that closed it moves the top one here up into Proposed goals as open.

- Nothing is waiting.

## Closed

What has landed, from the git history (a line per PR).

- #3 Set up the Hive files for pll: goals, test command, lessons; the gds viewer deploys to Pages only from main (2c1fa17).
- #6 Close the analog H1 open items: skew corners, the VCO ceiling at every corner, the jitter estimate; gates pass on 31 corners (ed2dbc0).
- #8 pll gets a score: `tests/score.sh`, the share of the goals' checkable done-lines that pass, re-run from scratch (c5c9acd).
- #14 The analog layout's post-layout benches run on the extracted netlist at all 31 corners the spec scores, with every routed internal net labelled so extraction keeps its coupling C; 29 of 31 pass (e4771cf).
- #15 Digital issue 8: a faster /2 prescaler stage, runaway recovery, the ss 2.7 ns corner waived with its numbers (f1aa1a9).
- Before this repository's pull requests, the work was committed to the `track/pll` branch. Four commits from that history carry pull-request numbers from the repository they were merged in, which are not this repository's: the check workflow (b1bf703, "#1"), the owner's analog sign-off H1-ada9eb (4c90ceb, "#6"), the Tiny Tapeout datasheet and pinout (665547c, "#10"), and iverilog through chip-flow's eda in `check.sh` (7f314a1, "#9").
