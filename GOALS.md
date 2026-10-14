# ece298a-pll goals

This repository is the term project of ECE 298A (Integrated Circuit Design and Tapeout) at the University of Waterloo: a charge-pump PLL for one Tiny Tapeout tile on GF180, with a divide-by-8 prescaler and a programmable feedback divider. Its analog half (the bias, the charge pump, the loop filter and the ring VCO) lives in `blocks/pll/analog`, its digital half (the phase-frequency detector, the dividers, the lock detector and the control registers) in `blocks/pll/digital`, and the two meet in `blocks/pll/interface.yaml`. `bash tests/check.sh` is the fast check every pull request has to pass. This is coursework, so runs never submit anything to a course system.

## Commands a run may use

Besides `bash tests/check.sh` and git, a run here may run the chip flow's own scripts. Type each one as its own command, with no `cd`, `&&`, pipe, redirect or variable in front, starting with exactly the words shown, because the engine allows these and nothing else:

- `/opt/chip-flow/bin/eda python /opt/chip-flow/engine/scripts/task_router.py` matches a task to its verb and plans the steps.
- `/opt/chip-flow/bin/eda python /opt/chip-flow/engine/scripts/state.py resume` says where a workspace stands.
- `/opt/chip-flow/bin/eda python /opt/chip-flow/engine/scripts/state.py edit` records a declared edit to a spec or interface file.
- `/opt/chip-flow/bin/eda python /opt/chip-flow/engine/scripts/state.py set-phase` moves a workspace to its next phase once that phase's gates pass, and never with `--force`.
- `/opt/chip-flow/bin/eda python /opt/chip-flow/engine/scripts/state.py issue` updates an open issue's status or attempts.
- `/opt/chip-flow/bin/eda python /opt/chip-flow/engine/scripts/state.py budget` reads or spends one of a workspace's fix-loop budgets.
- `/opt/chip-flow/bin/eda python /opt/chip-flow/engine/scripts/state.py snapshot` saves a workspace before a fix.
- `/opt/chip-flow/bin/eda python /opt/chip-flow/engine/scripts/state.py restore` puts a snapshot back after a fix made things worse.
- `/opt/chip-flow/bin/eda python /opt/chip-flow/engine/scripts/gate.py` runs and records a gate.
- `/opt/chip-flow/bin/eda python /opt/chip-flow/engine/scripts/jobs.py` runs a long gate, such as the harden, as a detached job.
- `/opt/chip-flow/bin/eda python /opt/chip-flow/engine/scripts/fix_dispatch.py` turns a failed gate into fix work orders.

`CHIP_FLOW_HOME` and `EDA_TOOLCHAIN` are already set for the run, and one command may run for up to 45 minutes. A run never records a sign-off. Recording one (`state.py human`) is a person's step, taken from the owner's own words in the thread.

## Proposed goals

Filed by runs. Each says what done looks like as something a run can check, and keeps its status (open, done, failed, dropped) with the pull requests that moved it. At most three are open at once.

### Sign off the PLL's analog half and close what it carries into layout

- **Status:** open; the owner approved H1-ada9eb, recorded in `blocks/pll/analog/log/H1-signoff.md` (#4), and the open items below remain
- **What:** The analog half has passed every pre-layout check over 29 simulation corners (spec lint, netlist lint, the typical and PVT simulations, and the bench-strength check), and its layout waits on the owner's sign-off. That sign-off decides whether the analog netlist, the spec it is checked against and those results are frozen as the reference layout has to match. It also accepts two changes made since the proposal: wider charge-pump current windows, and a phase-margin floor of 30 degrees scored at every corner. The [review](https://github.com/ihsan-sa/ece298a/blob/main/docs/pll-h1-review.md) sets out the results, the thin margins and the open items. The sign-off has been asked for, and the owner's answer arrives as an ask. A run records that answer as he gave it; it never approves the sign-off itself, and it changes nothing under `blocks/pll/analog` until the answer is recorded. If he approves, the run closes the open items: it puts the two resistor-skew corners (`ss_pff`, `ff_pss`) back into the spec, scores the VCO's 333 MHz ceiling at every corner (the VCO reaches about 363 MHz at fast, cold, low supply with its control voltage at the rail), corrects the frequency that the spec's sign-off note mislabels, reruns the analog checks, and reruns the digital timing with the VCO clock at about 2.7 ns. If he rejects it, the run reworks the design against his reason and asks again.
- **Done when:** the owner's answer is recorded as the analog sign-off in this repository. If he approved, the analog spec also scores both skew corners and the VCO ceiling at every corner, the analog spec lint, PVT simulation and bench-strength checks pass on that spec, and the digital timing check passes with the VCO clock at about 2.7 ns.

### Test the whole PLL loop in co-simulation

- **Status:** open
- **What:** The course grades a system verification of the term project. The proposal (`blocks/pll/brief/proposal-classic-pll.md`) tests the loop as a whole in three layers: a linear model of the loop, the real digital RTL in cocotb with Python models of the pump, filter and VCO calibrated from the analog benches, and a mixed-signal co-simulation of the digital RTL with the analog netlist. Build those benches under `blocks/pll` and run them. This reads the analog half but does not change it, so it can go ahead while the sign-off above is pending.
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

- No pull request has landed yet; the work so far was committed straight to the `track/pll` branch.
