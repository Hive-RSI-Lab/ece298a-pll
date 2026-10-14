# H1 sign-off: PLL analog half

- **Answer:** approved, as given: `approve H1-ada9eb`
- **Challenge:** H1-ada9eb, presented 2026-10-12T03:50:46 at phase P4
- **Digest:** sha256 57f44dea5b23943fa774009f57df5e4cf4bbb27fc64116f4e858a181d83d941d
- **Source:** Slack C0C984ULHL4/1791992318.072609, carried as ihsan-sa/ece298a-pll#4
- **Recorded:** 2026-10-14

This approval covers the netlist, spec and gate results that H1-ada9eb was
presented on (spec_yaml `de9c9841…`, netlist `1ef1fe40…`, tb `75f9cbb0…`,
sizing `42905241…`, mutant_rulings `35732ca1…`, as hashed in `state.json`),
together with the two changes made since the proposal: wider charge-pump
current windows and a phase-margin floor of 30 degrees scored at every corner.
The [review](https://github.com/ihsan-sa/ece298a/blob/main/docs/pll-h1-review.md)
sets out what was presented. `log/scratch/h1/digest.md` is the earlier digest
for challenge H1-101694, which this one supersedes.

## Open items this approval carries into layout

Not yet done; they need ngspice and the digital timing flow:

1. Put the resistor-skew corners `ss_pff` and `ff_pss` back into the spec.
2. Score the VCO's 333 MHz ceiling at every corner (it reaches about 363 MHz
   at fast, cold, low supply with its control voltage at the rail).
3. Correct the frequency the spec's sign-off note mislabels.
4. Rerun spec_lint, sim_pvt and bench_strength on that spec.
5. Rerun the digital timing with the VCO clock at about 2.7 ns.
