# VCO and PLL jitter on the extracted cell

Script: `jitter/jitter_pex.py`. Recorded: `reports/recorded/jitter_pex.json` (full runs), `reports/recorded/jitter_pex_screen.json` (corner screen). Replaces the one-off `log/scratch/jitter/RESULT.md` (1.2 ps tt, 2.5 ps ss_125c: schematic, 260 MHz, 30-36 periods, ring-device white noise only).

## Headline

- **Period jitter of the free-running VCO at 100 MHz, simulated on the extracted cell:** 9.7 ps rms at tt_27c, 10.2 ps at ss_125c_vm10, 13.5 ps at ff_125c_vm10. ff_125c_vm10 is the highest of the 9 corners run, but 22 corners were not run, so it is not proven worst of all 31.
- **Locked PLL output, linear model only:** 44 to 61 ps rms integrated 10 kHz to 50 MHz, and 35 to 43 ps if VCO 1/f is dropped. Treat this as "about 35 to 60 ps". It excludes reference, PFD, charge-pump and supply noise, so it is not an upper bound on real silicon.
- **Deterministic:** the extracted ring also alternates long and short periods by up to +-6.8 ps on vco_out. This is separate from the rms figures.
- The old 1.2 and 2.5 ps figures should not be used. They were at 260 MHz with less noise included.

## Period jitter, simulated

Extracted netlist, vctrl held by an ideal source at the 100 MHz point. Each run settles 300 ns, then 520 periods. Crossings of ring node r5 at vdd/2. `sigma_T` is the rms period deviation with the mean, a linear drift and the period-2 pattern removed.

| corner | vdd, T | vctrl (V) | runs | sigma_T r5 (ps) | seeds (ps) | lag 2 (ps) | alternation r5 / vco_out (ps, noiseless) |
|---|---|---|---|---|---|---|---|
| tt_27c | 3.3, 27 | 1.819 | 3 x 520 | 9.7 | 9.3, 10.1, 9.8 | 14.6 | 3.3 / 6.1 |
| ss_125c_vm10 | 2.97, 125 | 1.842 | 3 x 520 | 10.2 | 10.3, 10.1, 10.4 | 16.5 | 3.4 / 6.8 |
| ff_125c_vm10 | 2.97, 125 | 1.458 | 2 x 520 | 13.5 | 14.2, 12.8 | 21.9 | 2.1 / 5.1 |

Corner screen, 1 seed x 200 periods, so about +-5 % and only good for ranking (`jitter_pex_screen.json`; its closed-loop and fit fields are not meaningful at this length, ignore them):

| corner | vdd, T | vctrl (V) | sigma_T r5 (ps) | lag 2 (ps) |
|---|---|---|---|---|
| ff_125c | 3.3, 125 | 1.616 | 12.2 | 19.6 |
| ff_pss | 3.63, -40 | 2.207 | 11.4 | 16.8 |
| ff_27c_vm10 | 2.97, 27 | 1.444 | 10.9 | 15.2 |
| ss_pff | 2.97, 125 | 1.514 | 10.3 | 15.9 |
| tt_pff | 3.3, 27 | 1.626 | 9.9 | 13.6 |
| ff_m40c_vm10 | 2.97, -40 | 1.448 | 9.7 | 12.6 |

The corners were picked by judgement. Hot ff corners read highest, which fits lower capacitance meaning less charge per edge at the same frequency, but that explanation was not tested. ss_125c_vm10 was the first pick for worst and was wrong.

**STA budget.** The STA's 0.20 ns at 7 sigma allows 28.6 ps rms. The largest lag-2 value here is 21.9 ps, so it still fits at 100 MHz, with less room than the old estimate implied. The STA clock is constrained at twice the VCO's ceiling period, not at 100 MHz, and jitter at that faster point was not measured.

- Statistical error on a pooled sigma is about 2 % (from `1/sqrt(2N)`, which assumes independent periods). Seeds at ff_125c_vm10 differ by more (14.2 and 12.8 ps), so read that corner as 13.5 +- 1 ps.
- Numerical floor (noiseless 150-period run, same statistics): 0.07 to 0.24 ps on r5, 0.24 to 0.51 ps on vco_out. In the screen (30 periods) up to 0.74 ps.
- vco_out gives the same sigma_T as r5 to within 0.2 ps. No buffer noise is injected, see "Left out".
- 1/f barely moves period jitter: the 1/f-only runs give about 2 ps, and tt and ss read the same with and without it within error.

**Lag 2 (the vco_div2 period).** rms over two VCO periods is 14.6 ps tt, 16.5 ps ss_125c_vm10, 21.9 ps ff_125c_vm10. This is derived from r5 crossings. vco_div2 itself was not measured and the divider's own noise is not included.

**Period-2 pattern.** The noiseless extracted ring alternates long and short periods: +-3.3 ps on r5 and +-6.1 ps on vco_out at tt (+-6.8 ps at ss_125c_vm10). After removing it the residue is 0.05 ps on r5, so it is deterministic. It is left out of sigma_T and reported here instead. The earlier "noiseless floor" in the scratch result may be partly this. It repeats every two periods, so it cancels over a vco_div2 period. The cause is not established: kickback from the /2 is a guess that was not tested.

## Noise sources

- Every MOS outside the output buffer and divider: a `trnoise` current source drain to source. White level and 1/f coefficient come from a BSIM4 `.noise` of a copy of that instance at its own bias. So these are model values rather than an assumed gamma.
- Bias: ring devices at the moment their ring node crosses vdd/2, where the ring is most sensitive. Others: averaged over the last 100 ns of a noiseless run. Noise amplitude is stationary, so ring-device noise is held at that crossing value all period. This is an upper-side choice.
- Every poly resistor except the R1 segment touching vctrl: 4kT/R. R1 itself is shorted by the ideal vctrl source and enters the closed-loop model instead.
- `trnoise` scaling was checked by a periodogram of the source alone: one-sided white S = 2 NA^2 NT, and 1/f S = NAMP^2 / (2 f), at NT = 1 ns and 20 ps. The runs themselves use NT = 50 ps, which was not separately checked.
- K is taken from S at 1 kHz. In one test device (nfet, W/L 2/0.5 um) f*S rose about 40 % from 1 kHz to 1 MHz, so the 1/f level near the loop bandwidth may read somewhat low.

## Free-running phase noise

L(f) = a2/f^2 + b3/f^3 for the VCO, from averaged periodograms of the time error.

- **b3** comes from separate 1/f-only runs (3 seeds, no white source), fitted as f^3 L = b3 + c2 f. Slopes over the fitted bands are -23.5 to -27 dB/decade rather than -30, because 1/f noise folded around the carrier also gives a 1/f^2 term.
- **a2** comes from the full runs' bands between 1.5 and 12.5 MHz, after subtracting b3/f^3. It agrees with the slope of the accumulated-jitter variance over lags 4 to 32.
- a2 is well below `f0^3 sigma_T^2`: about 54 vs 95 Hz at tt, 86 vs 183 Hz at ff_125c_vm10. So part of the period jitter does not accumulate, and the simple conversion from sigma_T would overstate phase noise. The cause of that non-accumulating part was not identified.

| corner | a2 (Hz) | b3 (Hz^2) | 1/f^3 corner | L(1 MHz) dBc/Hz |
|---|---|---|---|---|
| tt_27c | 54 | 1.7e7 | 310 kHz | -101.5 |
| ss_125c_vm10 | 66 | 4.5e7 | 690 kHz | -99.6 |
| ff_125c_vm10 | 86 | 1.7e7 | 200 kHz | -99.9 |

b3 is the weakest number here. Band values of f^3 L scatter by a factor of 2 to 4 within a corner, and ss reads higher than tt although its device K is lower. Differences in b3 between corners are not significant.

## Closed-loop estimate: a linear model, not a simulation

Continuous-time model with the free-running L(f) above and R1's thermal noise, integrated 10 kHz to 50 MHz. Per-corner loop: Icp from `reports/recorded/pex_pvt.json`, R1 from the extracted segments, C1 and C2 at the corner's MOS-cap factor, Kvco from the +-100 mV points around the 100 MHz vctrl.

| corner | crossover | rms, with 1/f | rms, no VCO 1/f | R1 part | with Kvco = 116 MHz/V |
|---|---|---|---|---|---|
| tt_27c | 524 kHz | 43.6 ps | 34.7 ps | 6.0 ps | 40.7 ps (580 kHz) |
| ss_125c_vm10 | 493 kHz | 60.7 ps | 39.3 ps | 7.2 ps | 54.5 ps (574 kHz) |
| ff_125c_vm10 | 574 kHz | 49.0 ps | 42.7 ps | 7.6 ps | 51.3 ps (538 kHz) |

- The paper's 585 kHz assumes Kvco = 116 MHz/V. These runs measure 102 MHz/V at tt on the extracted ring, giving 524 kHz. Both are shown.
- Given the b3 scatter, quote the range, not a corner ranking.
- Period jitter is not reduced by the loop: 10 ns is far shorter than the loop's response, so the simulated sigma_T stands for the locked PLL too.
- The fit leaves out the non-accumulating part above about 10 MHz. Its size from the lag data is roughly 5 ps, small in quadrature but not counted.

## Left out

- Reference, PFD and charge-pump noise. The model has no in-band noise source except R1, so the low-offset closed-loop values are optimistic.
- Supply and substrate noise. vdd is ideal here. For a current-starved ring on a shared rail this may well dominate on silicon, and this bench cannot say by how much.
- Output buffer and divider noise. Their devices switch rail to rail, so an averaged bias means nothing. Hand estimate only: sqrt(kT/C) / slew with an assumed 30 fF and 3 V/ns gives a few tenths of a ps per edge.
- Sampling effects of the PFD, device mismatch, and R1 and resistor 1/f.
- 22 of the 31 corners, and white-only runs at ff_125c_vm10.

## Rerun

    python3 jitter/jitter_pex.py --corners tt_27c ss_125c_vm10 --seeds 3 --flicker-seeds 3 --periods 520 --jobs 3
    python3 jitter/jitter_pex.py --corners ff_125c_vm10 --seeds 2 --white-seeds 0 --flicker-seeds 3 --periods 520 --jobs 3
    python3 jitter/jitter_pex.py --recalc   # fits and model only

`--netlist` defaults to `log/pex_pvt/pll_analog.pex.ordered.spice`, which `layout/pex_pvt.py` makes (log/ is not committed). The json records the sha256 of the netlist used. Each 520-period run takes about 20 min on a quiet machine, 1 h under load. Crossing times are not recorded, only their statistics and spectra.

## Bookkeeping notes

- In the json's `by_group`, `ring_starve` counts 23 devices: the 20 starve devices plus 3 diode-connected mirrors. All of them get noise either way, so this affects only the labels.
- The `buffer_divider` values in `by_group` are listed but not injected.
- `bias_cp_other` may include some divider devices whose nets the grouping misses. They would get stationary sources at an averaged bias. They sit after the ring, so r5 should be little affected, but this was not checked device by device.
