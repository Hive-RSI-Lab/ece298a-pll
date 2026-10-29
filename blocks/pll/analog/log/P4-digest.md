# P4 digest - pll_analog (2026-10-28, after H1-ada9eb)
- Corners: 27-point grid + ss_pff, ff_pss (extra) + tt_pss, tt_pff = 31. sim_pvt PASS at all 31.
- Icp code00 13.64 (DN, ff_pss) .. 27.06 uA (UP, ss_pff) vs 12..30; nominal 19.01 uA vs 18..22 (1.0 uA margin).
- UP/DN mismatch worst 8.69 % (ff_pss) vs 10; overlap charge 3.61 fC (ss_pff) vs 10.
- PM P*N=16: 49.5 deg tt vs 45; 37.2 deg (ff_125c_vp10) .. 54.0 vs 30 at every corner; ff_pss 43.3, ss_pff 50.0.
- VCO ceiling (vctrl = vdd) 158.95 (ff_pss) .. 362.9 MHz (ff_m40c_vm10) vs 150..370; Kvco 49.7 .. 141.9 MHz/V vs 40..250.
- bench_strength PASS, 34 survivors all covered by the owner-accepted below_spread rulings; mc not applicable.
- Jitter: written estimate in spec.md (~1.2 ps rms tt, ~2.5 ps ss hot), not gated.
- Netlist edit: MIM model m2m3 -> m4m5 (same model; gf180mcuD draws MIM-B only).
- Files: reports/gate-*.json, spec/spec.md "Revision 2026-10-28", log/H1-signoff.md.
