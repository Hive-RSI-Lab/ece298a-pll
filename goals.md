# H1 goals for pll

H1's copy of the open goals in `GOALS.md` (Hive-RSI-Lab/ece298a-pll, main at fc98a6c). H1 works only on `h1/*` branches; `h1/main` is the integration branch, cut from fc98a6c. Never push to main or H0's branches; never touch H0's issues or PRs. Nothing is submitted to a course system or Tiny Tapeout.

Setup: `export EDA_TOOLCHAIN=/opt/eda-toolchain/iic-osic-tools-2026.09 CHIP_FLOW_HOME=~/modules/hive-chip-flow`, then `bash tests/check.sh` (passes at fc98a6c). Tools that need the toolchain run as `$CHIP_FLOW_HOME/bin/eda <tool>` (eda python has cocotb 2.1 and cocotbext.ams; ngspice-47).

## 1. Digital issue 8: timing at the post-layout VCO ceiling plus margin
- **Status:** open. At ss the routed result is between -0.03 and +0.004 ns at max_ss with a 0.10 ns jitter uncertainty: it closes, but with no margin. tt +0.8 ns, ff +1.57 ns. GOALS.md says real margin at ss needs a TSPC /2 inside the analog macro, so the digital half would be clocked at vco/2. That means analog layout, DRC, LVS and pex_pvt 31/31 all run again.
- **Done when:** the digital timing gate passes with vco_out at each process's post-layout ceiling plus margin (`tests/score.py` checks it), with setup and hold met at every STA corner.

## 2. System verification on the extracted netlist at the bounding corners
- **Status:** open. In `blocks/pll/reports/recorded/cosim_corners.json` all 4 corners lock, but vctrl p-p is 20.9 mV at ff_pss and 27.4 mV at ff_m40c_vm10, against a 20 mV limit. The excess comes from isolated pump kicks. Next step: find out whether a finer sync grid or the gate-level PFD's reset pulse removes them (see `blocks/pll/tb/README.md`). Each corner takes about 25 minutes of wall time: `$CHIP_FLOW_HOME/bin/eda python blocks/pll/tb/cosim_corners.py`.
- **Done when:** the recorded cosim_corners.json shows lock at every corner `bounding_corners()` picks, vctrl within 20 mV p-p over the last 10 us, and inputs unchanged.

## 3. Harden the tile and pass the Tiny Tapeout precheck
- **Status:** the done-line looks met at fc98a6c (checked by H1 on 2026-10-30), but GOALS.md still says open. On main (run 41126114809) the gds workflow, including the TT precheck job, passes, and so do docs, test and check. The tile reports are recorded as passing: gate-top_harden, gate-top_drc, gate-top_lvs, and gate-precheck (2026-10-30T16:14). `src/` holds the real design, and `gds/` is newer than every RTL and layout change. One caveat: 91ec795 changed the digital SDC after the tile was hardened, but it didn't change the RTL. Proposed status: done, pending a `tests/score.py` run.
- **Done when:** the tile hardens with no DRC or LVS errors, the TT precheck passes, and the gds, docs and test workflows pass on main with the real design in `src/`.
