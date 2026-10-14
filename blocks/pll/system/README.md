# Whole-loop verification

The proposal (`blocks/pll/brief/proposal-classic-pll.md`, section 5) tests the loop as a whole in three
layers. This folder holds them as they land.

| Layer | What | Where | Runs in |
|---|---|---|---|
| 1 | Linear model of the loop over every corner and lock-table point | `linear_loop.py` | `bash tests/check.sh` |
| 2 | The digital RTL in cocotb, closed with Python models of pump, filter and VCO | not yet | |
| 3 | Mixed-signal co-simulation of the digital RTL with the analog netlist | not yet | |

## Layer 1: the linear model

`linear_loop.py` takes R1, C1 and C2 from the netlist's `.param` defaults, and Icp (code 00) and Kvco at
each of the 29 corners from the recorded PVT run (`analog/reports/recorded/gate-sim_pvt.json`). It
models the type-2, third-order loop `H(s) = K (1 + s R1 C1) / (s^2 (1 + s R1 Cs))` with
`K = Icp Kvco / (P N (C1 + C2))`, then reports the crossover, the phase margin, Gardner's sampling limit
and the small-signal settling time (1 % of the slowest closed-loop pole) at every point of the lock
table.

The record does not give the resistor's value at the skewed passive corners, so the model fits one R1
scale per passive corner to ngspice's `ol_pm_pn16_nopad_pvt_deg`. Every corner then has to agree with
ngspice within 3°, and so do the tt_27c margins at P·N = 8 and 40. On the recorded run (2026-10-14) the
scales came out at ss 1.27 and ff 0.77, and the model lies within 0.6° of ngspice at every corner. That
is what makes the numbers below worth trusting at P·N values the PVT run does not score.

Results on the recorded run:

- P·N = 16 (N = 2): worst phase margin 37.3° (ff_125c_vp10), above the spec's 30° floor at every corner.
- Settling stays under 17 µs at every point, against the 50 µs lock-time bound. That figure is the small-signal
  part only; frequency acquisition (Vctrl slewing at Icp/(C1+C2)) adds a few µs.
- The Gardner limit holds at every point. The crossover is at most f_ref/5.5 (6.25 MHz, N = 1), so it
  breaks the f_ref/10 rule of thumb at N = 1 with f_ref of 6.25 and 10 MHz, as the proposal expected.
- **N = 4 and 5 (P·N = 32 and 40) fall under 30°** at the fast-passive, hot, high-supply corners: down to
  24.8° at ff_125c_vp10 (5 MHz, N = 5) and 27.6° at N = 4. The spec scores the 30° floor at P·N = 16
  only, so no gate catches this. The proposal's remedy is the Icp trim on `uio[1:0]` at P·N = 32 to 40.
  `linear_loop.py` prints these points as notes and does not fail on them.
