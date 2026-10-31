# H1 goals for pll

H1's copy of the open goals in `GOALS.md` (Hive-RSI-Lab/ece298a-pll, main at fc98a6c). H1 works only on `h1/*` branches; `h1/main` is the integration branch, cut from fc98a6c. Never push to main or H0's branches; never touch H0's issues or PRs. Nothing is submitted to a course system or Tiny Tapeout.

Setup: `export EDA_TOOLCHAIN=/opt/eda-toolchain/iic-osic-tools-2026.09 CHIP_FLOW_HOME=~/modules/hive-chip-flow`, then `bash tests/check.sh` (passes at fc98a6c). Tools that need the toolchain run as `$CHIP_FLOW_HOME/bin/eda <tool>` (eda python has cocotb 2.1 and cocotbext.ams; ngspice-47).

## 1. Digital issue 8: timing at the post-layout VCO ceiling plus margin
- **Status:** open. At ss the routed result is between -0.03 and +0.004 ns at max_ss with a 0.10 ns jitter uncertainty: it closes, but with no margin. tt +0.8 ns, ff +1.57 ns. GOALS.md says real margin at ss needs a TSPC /2 inside the analog macro, so the digital half would be clocked at vco/2. That means analog layout, DRC, LVS and pex_pvt 31/31 all run again.
- **Done when:** the digital timing gate passes with vco_out at each process's post-layout ceiling plus margin (`tests/score.py` checks it), with setup and hold met at every STA corner.

## 2. System verification on the extracted netlist at the bounding corners
- **Status:** done on h1/main (2026-10-31). The 1 ns bridge sync grid caused the vctrl excess (20.9 mV at ff_pss, 27.4 mV at ff_m40c_vm10): PFD edges quantised to the grid fired isolated pump kicks. `cosim_corners.py` now runs the extracted netlist at a 0.25 ns sync; the layer-3 gate keeps 1 ns. All 4 bounding corners lock and hold, with vctrl p-p over the last 10 us of 15.5 / 0.6 / 11.3 / 0.2 mV (ff_pss, ff_m40c_vm10, ff_125c_vp10, ss_m40c_vm10). The recorded result is fresh (`score.cosim_corners_fresh()`). A run takes about 90 min of wall time with 4 corners side by side.
- **Done when:** the recorded cosim_corners.json shows lock at every corner `bounding_corners()` picks, vctrl within 20 mV p-p over the last 10 us, and inputs unchanged.

## 3. Harden the tile and pass the Tiny Tapeout precheck
- **Status:** done on h1/main (2026-10-31). `tests/score.sh` showed the tile's recorded passes as stale: 91ec795 changed the digital SDC after the tile was hardened. H1 re-ran top_harden, top_drc, top_lvs and precheck (12 checks, 0 failing); all four pass, and `score.tile()` counts them as fresh. On main, the gds workflow, its TT precheck job included, passes, and so do docs, test and check (run 41126114809).
- **Done when:** the tile hardens with no DRC or LVS errors, the TT precheck passes, and the gds, docs and test workflows pass on main with the real design in `src/`.
