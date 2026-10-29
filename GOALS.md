# ece298a-pll goals

This repository is the term project of ECE 298A (Integrated Circuit Design and Tapeout) at the University of Waterloo: a charge-pump PLL for one Tiny Tapeout tile on GF180, with a divide-by-8 prescaler and a programmable feedback divider. Its analog half (the bias, the charge pump, the loop filter and the ring VCO) lives in `blocks/pll/analog`, its digital half (the phase-frequency detector, the dividers, the lock detector and the control registers) in `blocks/pll/digital`, and the two meet in `blocks/pll/interface.yaml`. `bash tests/check.sh` is the fast check every pull request has to pass. This is coursework, so runs never submit anything to a course system.

## Proposed goals

Filed by runs. Each says what done looks like as something a run can check, and keeps its status (open, done, failed, dropped) with the pull requests that moved it. At most three are open at once.

### Sign off the PLL's analog half and close what it carries into layout

- **Status:** open; the owner approved H1-ada9eb, recorded in `blocks/pll/analog/log/H1-signoff.md` (#6); the items the approval carries into layout stay open
- **What:** The analog half passed every pre-layout check over 29 simulation corners (spec lint, netlist lint, the typical and PVT simulations, and the bench-strength check), and the owner signed it off: `approve H1-ada9eb`, recorded in `blocks/pll/analog/log/H1-signoff.md`. That freezes the analog netlist, the spec it is checked against and those results as the reference layout has to match, together with the two changes made since the proposal: wider charge-pump current windows, and a phase-margin floor of 30 degrees scored at every corner. The [review](https://github.com/ihsan-sa/ece298a/blob/main/docs/pll-h1-review.md) sets out the results, the thin margins and the open items. What stays open is what the approval carries into layout: put the two resistor-skew corners (`ss_pff`, `ff_pss`) back into the spec, score the VCO's 333 MHz ceiling at every corner (the VCO reaches about 363 MHz at fast, cold, low supply with its control voltage at the rail), correct the frequency that the spec's sign-off note mislabels, rerun the analog checks, and rerun the digital timing with the VCO clock at about 2.7 ns. A run never signs off on the owner's behalf: if these changes move the design away from what they approved, it asks them again.
- **Done when:** the owner's answer is recorded as the analog sign-off in this repository (done, #6), the analog spec scores both skew corners and the VCO ceiling at every corner, the analog spec lint, PVT simulation and bench-strength checks pass on that spec, and the digital timing check passes with the VCO clock at about 2.7 ns.

### Test the whole PLL loop in co-simulation

- **Status:** open
- **What:** The course grades a system verification of the term project. The proposal (`blocks/pll/brief/proposal-classic-pll.md`) tests the loop as a whole in three layers: a linear model of the loop, the real digital RTL in cocotb with Python models of the pump, filter and VCO calibrated from the analog benches, and a mixed-signal co-simulation of the digital RTL with the analog netlist. Build those benches under `blocks/pll` and run them. This reads the analog half but does not change it, so it can go ahead while the open items above are closed.
- **Done when:** the three layers run from one command in this repository, the co-simulation shows the loop locking at the 100 MHz nominal point with the lock detector asserting, and the result is written up next to the benches.

## Later

Goals waiting for an open slot. When a proposed goal closes, the run that closed it moves the top one here up into Proposed goals as open.

### Lay out the analog half and match it after extraction

- **Status:** proposed
- **What:** Once the analog sign-off is recorded with the owner's approval, draw the layout of the analog half, pass DRC and LVS against the signed-off netlist, extract its parasitics, and rerun the analog benches on the extracted netlist against the spec's post-layout bounds. Matching, the charge pump's mirrors and the VCO ring's symmetry are the places where layout can eat the thin margins the review lists.
- **Done when:** DRC and LVS pass on the analog layout, and every analog bench passes its post-layout bounds on the extracted netlist at every corner the spec scores.

### Harden the tile and pass the Tiny Tapeout precheck

- **Status:** proposed
- **What:** With the analog layout done, harden the digital half around the analog macro into one tile, run full-tile DRC and LVS, and pass the Tiny Tapeout precheck. Replace the template placeholder in `src/` and the template README with the real design, so the Tiny Tapeout gds, docs and test workflows build and test this design rather than the template.
- **Done when:** the tile hardens with no DRC or LVS errors, the Tiny Tapeout precheck passes, and the gds, docs and test workflows pass on main with the real design in `src/`.

## Closed

What has landed, from the git history (a line per PR).

- #1: Add a check workflow and GOALS.md for the dispatch engine.
- #6: Record the owner's analog sign-off H1-ada9eb.
- #10: Fill the Tiny Tapeout datasheet and pinout so the docs check passes.
- #9: check.sh runs iverilog through chip-flow's eda when it isn't on PATH.
- #3: Set up the Hive files for pll: goals, test command, lessons; deploy the gds viewer to Pages only from main.
- Before #1, the work was committed straight to the `track/pll` branch.
