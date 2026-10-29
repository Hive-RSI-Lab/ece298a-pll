# P5 digest - pll_analog layout (2026-10-28)
- drc PASS: 0 klayout GF180 signoff findings (density/antenna/dummy decks are chip-level, skipped by the gate).
- lvs PASS: netgen unique match, 87 devices / 53 nets, sizing.yaml applied.
- pex_sim PASS at typical (magic R+C, 1065 R / 817 C): icp_up 18.99, icp_dn 18.64 uA (12..30);
  Kvco 80.9 MHz/V (40..250; 92 pre-layout); vco_fmax_tt 226.3 MHz (>= 200; 257.8 pre-layout).
- First extraction read vco_fmax_tt 154.8 MHz (ring wire C ~12 fF/node); wo-11 cut it to ~3 fF, fixed.
- Block 128.0 x 181.4 um; C1 100 x 100 um MIM-B (20 pF) over three device rows; caps metal4/metal5.
- Matching: CP NMOS mirror ABCCBA, PMOS ABBA, bias/trim bank common-centroid, ring stages identical.
- Pins: six digital pins on the right edge, vctrl/bias_ref/vdd/vss on the bottom, metal2 labels.
- Open: post-layout at typical only; slow corners after layout unscored (pre-layout ff_pss fmax 158 MHz
  less ~12 % layout slowdown ~ 139 MHz); bias_ref bare-node oscillation found in cosim (pad C fixes it).
- Files: reports/gate-drc.json, gate-lvs.json, gate-pex_sim.json, layout/gen_pll_analog.py.
