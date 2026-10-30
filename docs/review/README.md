# Reviewing the PLL

One page for reviewing where the PLL stands, what it looks like, and which
decisions were taken without you, each marked as waiting for your review. You
said on 2026-10-29 (chat 261030-010852): "dont wait for me on anything. Just
build it all, i will retroactively review and tell you what to change or
redesign." So nothing below counts as approved by you. Each decision says what
was chosen, why, and what changing it would cost.

Regenerate the figures after any result changes:

    uv run --python 3.12 --no-project --with gdstk --with matplotlib python docs/review/make_figures.py

## Where it stands

| Stage | State | Evidence |
|---|---|---|
| Analog schematic, 31 PVT corners | done, signed off by you (H1-ada9eb) | `blocks/pll/analog/log/H1-signoff.md` |
| Digital RTL: PFD, /8 prescaler, /N divider, lock detector, registers | done; sim, formal, coverage, mutation, holdout, standalone harden, DRC, LVS, precheck and gate-level sim pass | `blocks/pll/digital/state.json` |
| Whole loop in co-simulation (RTL + transistor-level analog) | done: locks at 100.000 MHz in 4.48 us | `blocks/pll/tb/README.md`, figure below |
| Digital timing with the VCO clock at 2.7 ns | tt and ff meet; ss_125C waived (decision 2) | `blocks/pll/digital/state.json` issue 8 |
| Analog layout | DRC clean, LVS unique match | `blocks/pll/analog/layout/` |
| Post-layout benches on the extracted netlist | 28 of 31 corners pass; ff_pss, ss_m40c_vm10 and tt_pss do not (below) | `blocks/pll/analog/reports/recorded/pex_pvt.json` |
| Full tile (digital hardened around the analog macro) | blocked: chip-flow's top_harden shorts vctrl to VGND (fix in hive-chip-flow PR #28, testing) | GOALS.md, "Harden the tile" |
| Tile DRC, LVS, Tiny Tapeout precheck | not run yet (needs the tile) | |
| `src/`, `test/`, `info.yaml`, workflows in Tiny Tapeout's analog-project shape | staged and tested in `blocks/pll/tt`; goes in with the tile's GDS | `blocks/pll/tt/README.md` |

Nothing is ever submitted to Tiny Tapeout or the course for you. "Ready for
submission" stops at: precheck passes on the committed GDS, and the repository
has the analog template's shape.

## What it looks like

### The analog macro

Bottom to top, as `gen_pll_analog.py` draws it: the ring VCO (the small
block at the bottom right, under the vco_out pin); two rows of bias, buffer
and enable devices; the resistors' poly serpentines (R1, R_V2I and the bias
resistors, the tall red bars); the charge pump's NMOS row and its PMOS mirror
bank. The loop filter's MIM capacitors are the two large Metal4 plates over
the rows: C1 on top, C2 bottom left. Digital pins are on the right edge.
Supplies and the two analog pads (vctrl, bias_ref) are on the bottom edge.

![pll_analog layout](analog-layout.png)

To open it yourself: `klayout blocks/pll/analog/layout/pll_analog.gds`. The
generator that draws it is `blocks/pll/analog/layout/gen_pll_analog.py`.
GitHub Pages is on for the repository (warden request 261030-015628,
2026-10-30). The gds workflow's viewer job publishes a 3D GDS viewer of
what main builds at https://hive-rsi-lab.github.io/ece298a-pll/ on every
push to main. Until the tile replaces the template, that is still the
template's GDS.

### The loop locking

The loop locking on the transistor-level analog netlist, co-simulated with the
digital RTL. To watch it lock in a waveform viewer without any EDA tree, run
the RTL test of the real top (Icarus Verilog and cocotb). It uses a
behavioural model of the analog macro and takes about a second:

    python3 blocks/pll/tt/assemble.py   # before the tile is in, this is a local preview: do not commit it
    cd test && make && gtkwave tb.fst   # or surfer tb.fst

![co-simulation lock](cosim-lock.png)

### Post-layout, every corner

![post-layout corners](post-layout-corners.png)

What fails, and why:

- **ss_m40c_vm10**: the bias reference settles in its second DC operating
  point (pump current 168 uA, no oscillation). This is a real start-up risk,
  not a bench artefact: started from pll_en rising, the extracted netlist
  reaches the same state. Task 261030-001020 is working on it (a start-up
  path or a bias change).
- **ff_pss**: Kvco reads 36 MHz/V against a 40 MHz/V floor (decision 3).
- **tt_pss**: a simulator-log misread, not a circuit failure. ngspice prints
  "Dynamic gmin stepping failed" and then converges by true gmin stepping;
  chip-flow reads the first line as an engine error. The fix is hive-chip-flow
  PR #34 (testing). Every measure at tt_pss is in bounds.

One thing the figure shows that no bound catches: at ff_pss the VCO's ceiling
is 114 MHz after layout (158 MHz before). Every corner still reaches the
100 MHz nominal point, but the lock range promised in `docs/info.md` (up to
about 200 MHz) only holds at typical. Decision 4 covers it.

## Decisions taken without you, waiting for your review

1. **The analog layout goes ahead to the tile (H2-a9fad5).** The engine
   presented the layout sign-off as challenge H2-a9fad5 on 2026-10-28. It is
   not recorded as approved. The tile is built on this layout, and
   `blocks/pll/analog/log/H2-proceed.md` records that this was done pending
   your review. If you reject it, the layout is redone and the tile rebuilt.
2. **Digital issue 8, the ss_125C timing waiver.** With the VCO clock
   constrained at 2.7 ns (370 MHz), the /2 prescaler stage misses setup by
   1.2 ns at ss_125C. No flop in the GF180 library toggles that fast at ss.
   It is waived at that corner because the VCO can't go that fast at ss:
   after layout, the fastest corner with slow transistors (ss_pff)
   reaches 247 MHz at the rail, and the stage manages 274 MHz. A recovery circuit also pulls the loop back if it
   ever runs away. The approval on record is the lead's under your 10-28
   "i signoff" message, not your own ruling. Details are in issue 8 of
   `blocks/pll/digital/state.json`.
3. **ff_pss Kvco, 36 vs 40 MHz/V (open).** The 40 MHz/V floor protects loop
   gain, and through it the phase margin. The decision rests on the phase
   margin at ff_pss, not the Kvco number. The linear loop model (layer 1,
   `blocks/pll/tb/pll_loop_model.py`) with ff_pss's post-layout pump current
   (13.6 uA) and Kvco scaled to 36 MHz/V gives 31 deg at P*N = 16 with
   typical R1, and 27 to 35 deg over R1 +-15%. The spec's floor is 30 deg at
   every corner. That is too close to call on a scaled estimate, so it is
   settled on the extracted netlist, by one of:
   (a) keep the bound and raise Kvco at ff_pss (a smaller R_V2I, re-layout);
   (b) replace the bound by the post-layout phase margin at every corner,
   if that clears 30 deg.
   Until one of those runs, the bound stands and ff_pss counts as failing.
4. **The datasheet's lock range.** `docs/info.md` will promise only what every
   post-layout corner reaches: the VCO between about 12 and 114 MHz, so
   8 x N x f_ref between those, with 100 MHz as the nominal point. Typical
   silicon goes further (7 to 205 MHz).
5. **The tile is 1x2, not 1x1.** Tiny Tapeout's GF180 analog tiles start at
   1x2. `info.yaml` says 1x1 today and changes with the tile.
6. **PFD_UP and PFD_DN leave the debug pins in the full tile.** In the
   standalone digital harden, `uo[3]` and `uo[4]` show the PFD's UP and DN
   pulses. In the tile, chip-flow wires each crossing signal to the analog
   macro only, so `uo[3:7]` read 0. Keeping UP/DN visible needs a chip-flow
   change (a crossing signal that also goes to a pad). Say if you want it.

## What is left before "ready for submission"

In order:

1. hive-chip-flow PR #28 lands (top_harden's false vctrl/VGND short), then the
   tile hardens: `top_harden`, `top_drc`, `top_lvs`, `precheck`.
2. The repository takes the analog template's shape. This is staged and
   tested in `blocks/pll/tt`. `python3 blocks/pll/tt/assemble.py` puts in
   place `src/` (the real top and the digital RTL), `test/` (an RTL test of
   the top with a behavioural analog model, which locks at 100 and 150 MHz),
   an `info.yaml` for a 1x2 analog tile, the `custom_gds` gds workflow, and
   the tile's GDS and LEF.
3. ss_m40c_vm10's bias start-up (task 261030-001020) and the ff_pss decision
   (3 above). Each changes the analog layout, so the tile is rebuilt after.
4. The issue 8 waiver written where chip-flow's release gate reads it
   (`blocks/pll/digital/reports/waivers.json`, bound to the timing gate's
   inputs). That needs a fresh digital timing run.
