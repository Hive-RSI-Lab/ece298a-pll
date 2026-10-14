# Whole-loop verification

The proposal (`../brief/proposal-classic-pll.md`, section 5) tests the loop as a whole in three layers. This folder holds them as they land.

| Layer | What | State |
|---|---|---|
| 1 | Linear (s-domain) model of the loop, `linear_model.py` | runs in `bash tests/check.sh` (step 3) |
| 2 | The digital RTL in cocotb, with Python models of the pump, filter and VCO calibrated from the analog benches | not started |
| 3 | Mixed-signal co-simulation of the digital RTL with the analog netlist | not started |

## Layer 1: the linear model

`linear_model.py` builds H(s) = Icp·Kvco·Z(s)/(s·P·N) for the type-II pump and R1 + C1 ∥ C2 filter. Nothing in it is hand-entered: R1, C1 and C2 come from `analog/sizing/sizing.yaml` (26.2 kΩ, 20.0 pF, 2.05 pF), and Icp and Kvco at each corner come from the recorded PVT run (`analog/reports/recorded/gate-sim_pvt.json`). It is the same gain `analog/tb/pll_analog_ol_tb.cir` measures, so the check compares the two.

Result on the recorded run (2026-10-14):

- **It agrees with ngspice.** At the nine corners with typical passives, the model's phase margin at P·N = 16 is within 0.6° of `ol_pm_pn16_nopad_pvt_deg` (49.4° against 49.5° at tt_27c, crossover 480 kHz). The check fails if they drift more than 3° apart. So the pump-filter-VCO loop behaves like the textbook model, with nothing missing that matters at the crossover. Layer 2 can use the same Icp, Kvco and filter values.
- **Margin across P·N.** The worst margin is at tt_125c_vp10, where Kvco is lowest: 52° at P·N = 8, 43° at 16, 36° at 24, 32° at 32 and 29° at 40 (ζ 0.29, crossover 193 kHz). The spec scores 30° at P·N = 16 only. At P·N = 40 the floor is missed at that corner, which is the case the proposal's risk table answers with Icp trim (`cp_trim` = 11).
- **Settling.** The estimate 4/(ζωn) stays under the 50 µs lock-time target at every modelled corner and every P·N.
- **Lock table.** At tt_125c_vp10 the VCO tops out at 194 MHz, so the 200 MHz points (5 MHz × 5, 6.25 MHz × 4, 12.5 MHz × 2) are out of range there. The 100 MHz nominal point is inside the range at every corner.

Not modelled yet: the 20 corners with ss or ff passives (every ss and ff process corner, plus tt_pss and tt_pff). Their R1 and C skew is not in the report, so the model would need the PDK's resistor and MIM corner values. The check prints ngspice's margin for those corners and does not score the model there.
