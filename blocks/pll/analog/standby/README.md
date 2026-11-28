# Disable-phase sweep (c23)

pex_sim's stress decks drop `pll_en` at one fixed time (3.301 us). The c23
standby holds (MN_HN5 and the others) have to keep every device within the
gate's limits wherever in the cycle the disable lands. This sweep moves the
`pll_en` fall across the cycle and scores each run with the gate's own code
(`stresslib.score_run`, the same limits and windows as `pex_sim`).

- `phsweep.py WS EXTRACTED DECK CORNER T TAG OUTDIR` runs one point. It
  imports chip-flow from `$CHIP_FLOW_HOME`, built against chip-flow af0861b.
- `disable_phase_c23.jsonl` has all 110 points, run on the c23 extraction
  (pex_sim's `pll_analog.pex.ordered.spice` of commit 1f78365):
  - `up` deck at ff_pss: 20 points; at ff_125c_vp10: 30 points.
  - `dn` deck at ff_pss: 30 points; at ff_125c_vp10: 30 points.
  - The fall time T runs from 3.3005 to 3.3058 us: a coarse step of 0.6 ns
    plus a fine step of 0.1 ns around the worst edge.

Result: no point has a scored fail (`fails` is empty on all 110). Each line
also carries the raw worst |V| between two terminals of any device after the
disable. The largest is 3.83 V (X179 Vgb, `dn` deck at ff_pss); the gate's
scoring accepts it, since it does not fail. MN_HN5 peaks at 3.63 V, and every
one of its pairs scores `allowance`.
