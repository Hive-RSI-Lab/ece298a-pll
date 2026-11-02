# Monte Carlo of pll_analog

`mc_mismatch.py` runs the existing benches' stimulus with the PDK's own statistics
switched on, one ngspice run per sample, on the schematic netlist. Per-sample values
and summaries are in `reports/recorded/mc_*.json`. Each report's `nominal` is the same
deck with the statistics off (it reproduces the recorded sim_pvt values).

## What the models carry

| Variation | In the models? | Where |
|---|---|---|
| MOS per-instance mismatch | yes, off by default | `.lib fets_mm`, in every MOS corner; `sw_stat_mismatch` (0 in design.spice). Pair sigma(dVth): 7.15 mV*um nfet_03v3, 6.66 mV*um pfet_03v3; beta 0.70 / 0.28 %*um |
| Global (die-to-die) MOS, R | yes, off by default | `.lib statistical`, `res_statistical`; `sw_stat_global` |
| Poly resistor per-instance mismatch | no | `mis_r=0` |

The wrapper draws one sample per instance and ignores `m=`, so the script simulates a
copy of the netlist with each m=N instance split into N devices.

## Results

Mismatch only. `Fails` is against the spec bound, with the 95 % Clopper-Pearson interval
of that corner's failure rate. It is a rate given that corner, not a product yield.

| Corner | Measure | Nominal | Mean | Sigma | Worst | Bound | Fails |
|---|---|---|---|---|---|---|---|
| ff_pss | `cp_updn_mismatch_pct` | 8.69 | 8.69 | 1.92 | 14.55 | <= 10 | **52/200** (20.1-32.7 %) |
| ff_m40c_vp10 | `cp_updn_mismatch_pct` | 7.38 | 7.38 | 1.63 | 12.38 | <= 10 | **12/200** (3.1-10.3 %) |
| ss_pff | `cp_updn_mismatch_pct` | 7.85 | 7.85 | 0.82 | 9.80 | <= 10 | 0/200 (< 1.8 %) |
| tt_27c | `cp_updn_mismatch_pct` | 4.98 | 5.06 | 1.30 | 9.27 | <= 10 | 0/200 (< 1.8 %) |
| tt_27c | `cp_overlap_net_charge_fc` | 2.38 | 2.40 | 0.33 | 3.41 | <= 10 | 0/200 |
| tt_27c | `icp_up_code00_ua` | 19.01 | 19.00 | 0.37 | 17.81, 19.87 | 12..30 | 0/200 |
| tt_27c | `icp_dn_code00_ua` | 18.66 | 18.65 | 0.33 | 17.50, 19.51 | 12..30 | 0/200 |
| tt_27c | `icp_code11_over_code00_ratio` | 1.977 | 1.977 | 0.008 | 1.959, 2.003 | 1.8..2.2 | 0/200 |
| tt_27c | `startup_time_us` | 0.676 | 0.678 | 0.032 | 0.738 | <= 5 | 0/200 |
| ss_m40c_vm10 | `startup_time_us` | 0.920 | 0.901 | 0.025 | 0.949 | <= 5 | 0/100 (< 3.6 %) |
| tt_27c | Ib, uA | 4.554 | 4.553 | 0.019 | 4.504, 4.597 | none | |
| tt_27c | VCO f at vctrl = vdd/2, MHz | 101.83 | 101.69 | 2.51 | 95.67, 108.77 | none | |
| tt_27c | static phase offset, ps | -127.7 | -127.8 | 19.5 | -189.8, -83.6 | none | |

Global + mismatch, tt_27c device models, 27 C, 3.3 V, 100 samples (`mc_glob_mm_tt_27c.json`);
no spec bound failed (< 3.6 % each):

| Measure | Mean | Sigma | Min, max | Bound |
|---|---|---|---|---|
| `cp_updn_mismatch_pct` | 4.91 | 1.16 | 3.08, 7.99 | <= 10 |
| `cp_overlap_net_charge_fc` | 2.40 | 0.30 | 1.91, 3.39 | <= 10 |
| `icp_up_code00_ua` | 19.08 | 1.34 | 16.11, 23.59 | 12..30 |
| `icp_dn_code00_ua` | 18.77 | 1.32 | 15.58, 23.01 | 12..30 |
| `startup_time_us` | 0.680 | 0.049 | 0.560, 0.798 | <= 5 |
| Ib, uA | 4.58 | 0.34 | 3.79, 5.71 | none |
| VCO f at vctrl = vdd/2, MHz | 102.09 | 6.42 | 86.58, 120.90 | none |
| static phase offset, ps | -124.9 | 19.3 | -167.4, -74.4 | none |

## Reading them

- **`cp_updn_mismatch_pct` does not hold its 10 % bound under mismatch at every corner.**
  The bound is written for all corners, and sim_pvt passes it only because it runs with the
  statistics off. Nominal already sits at 8.69 % at ff_pss. The peak is at the edge of the
  vctrl range: at ff_pss nominal it is 1.21 uA at vctrl = 0.3 V against 0.60 uA at
  mid-range (8.7 % vs 4.3 % of Icp). Mid-range was not run through MC.
- The other measures with bounds hold where they were run; the closest is `icp_dn_code00_ua` at ff_pss
  (min 12.50 against 12). Their corner coverage is
  narrower than the spec's: overlap and VCO ran at tt_27c only, and startup at tt_27c and
  ss_m40c_vm10.
- **High-Ib bias state:** not reached in 200 samples at tt_27c or 100 at ss_m40c_vm10, the corner
  where it was found before MN_ST was lengthened (vref_end 1.048-1.066 V there, bias_ref 0.70-0.71 V,
  against 0.51 V in that state).
- Static phase offset: negative means DN leads. It is the overlap bench's charge at vdd/2,
  with its 1 ns overlap, divided by Icp. The mean is systematic; sigma is the mismatch part.

## mc gate: the two VCO misses at tt (seeds 2, 14) are the bench's kick, not a start failure

The chip-flow mc gate (30 seeds, mismatch on, tt) passes 178/180 overall but 28/30 (93 %) on
`pll_analog_vco_tb.cir`. Both misses (seed 2 = deck mc1, seed 14 = deck mc13) fail only at the
sweep's lowest point, vctrl = 0.3 V: `vco_fmin_tt_mhz` 0 and swing ~0, while the ring runs at
every other point (fmax 259.7 and 262.6 MHz). Re-run at that point only, 800 ns, f from rises
2..4 after 100 ns (decks and output in `vco_start_seeds/`, `run.sh`), 2026-11-02:

| deck | 1 fC kick (bench as is) | 200 fC kick (as the pex benches) | no kick, pll_en rising at 5 ns |
|---|---|---|---|
| mc1 (seed 2, miss) | stalled, swing 11 uV | runs, 9.94 MHz, rail to rail | runs, 14.6 MHz |
| mc13 (seed 14, miss) | stalled | runs, 9.82 MHz | runs, 15.0 MHz |
| mc2 (seed 3, passed, control) | runs, 9.22 MHz | - | runs, 17.6 MHz |

So under mismatch the ring at vctrl = 0.3 V still starts from pll_en alone, the way it starts on
silicon; the 1 fC kick is too small to move these two samples off the op's balance point, the same
failure as the extracted ring (layout_ref/pll_analog_pex_tb.cir START-UP KICK note). The higher f
from pll_en alone is the same in the control seed, so it is the bench's start-up transient in a
800 ns window, not the mismatch. Not done: the vco bench's kick is unchanged (raising it to 200 uA
re-stales sim_tt, sim_pvt, mc and bench_strength), so the mc gate's 93 % on that bench stays on
record with this note as its reason. Only the 0.3 V point was re-run.

## Not covered

- Schematic only: no extracted parasitics, and no layout gradients.
- No resistor mismatch and no capacitor variation, because the models and benches do not vary them.
- Corner runs hold the corner fixed and add mismatch, so they do not weight how likely the corner
  is. The only global run is at 27 C, 3.3 V. No figure here is a product yield.
- Kvco, phase margin and the rest of the spec were not run through MC.

## Reproduce

    python3 mc_mismatch.py --mode mm --n 200
    python3 mc_mismatch.py --mode mm --corner ff_pss --n 200 --benches cp     # also ss_pff, ff_m40c_vp10
    python3 mc_mismatch.py --mode mm --corner ss_m40c_vm10 --n 100 --benches startup
    python3 mc_mismatch.py --mode glob_mm --n 100 --seed0 1001

Seeds are fixed. Rerunning 200 cp samples and 3 VCO samples gave identical values. Corner runs need
the rendered decks in `log/sim`.
