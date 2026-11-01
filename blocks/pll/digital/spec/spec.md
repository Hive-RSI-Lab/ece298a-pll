# PLL digital side - spec (tt_um_ihsan_sa_pll, TT GF180 analog tile)

Core module `ihsan_sa_pll` (harden generates the `tt_um_ihsan_sa_pll` wrapper
from `tt_pins`), library `gf180mcu_fd_sc_mcu7t5v0` at 3.3 V.
The digital side is the whole tile except the charge pump, loop filter, VCO
and bias, which are the analog hard macro `pll_analog`. The signals crossing
to that macro are fixed in `../../interface.yaml` (names, directions, widths,
standalone TT pins); nothing here renames, widens or adds one.

## Behaviour

1. **Phase-frequency detector (PFD).** Two D flops, one clocked by the
   reference `clk`, one by the feedback divider output `clk_fb`, with an AND
   reset and a short kept delay chain (keep attributes, `must_keep`) to
   remove the dead zone. Outputs are active-high pulses `pfd_up` and
   `pfd_dn`. `pfd_up` high: the reference leads, the pump sources current
   (raise Vctrl, speed up the VCO). `pfd_dn` high: the feedback leads, the
   pump sinks. Pulse widths track the phase offset in both directions;
   frequency detection works in both directions (reference faster gives net
   UP, slower gives net DN). The reset fires whenever both are high; UP and
   DN never both stay high beyond the reset delay. The reset pulse has no
   width in zero-delay RTL: the bench checks it happens, ngspice (analog
   side / msde cosim) measures its width. Outside a recovery (item 4b)
   the PFD's flops are the outputs as they are. (REQ-PFD-*)
2. **/8 prescaler (/2 in the macro, /4 here).** The analog macro divides the
   VCO by 2 in a TSPC stage and hands the digital side `vco_div2` = VCO/2
   (full swing, about 50% duty, held at a fixed level while `pll_en` is low,
   no reset input; issue #48). Here two ripple toggle flops (an async-reset
   flop with an `inv_1` from Q to D) divide `vco_div2` by 4, the only logic
   above 50 MHz; the first stage sees up to 185 MHz (5.4 ns), half the VCO's
   370 MHz ceiling. The first library stage used to run at the VCO itself,
   where at ss no library flop toggles fast enough with margin; at VCO/2
   its toggle loop (about 3.65 ns routed at ss_125C_3v00) has 7.5 ns at the
   ss ceiling. Recovery (item 4b) still covers a VCO above what the
   dividers take. (REQ-TIM-VCO) Output `clk_pre` = `vco_div2`/4 = VCO/8
   exactly (at most 46 MHz) clocks everything after it. (REQ-PRE-DIV8)
3. **Programmable /N divider.** N = 1..5 from `n_sel` = `ui_in[2:0]`.
   Codes 0, 6, 7 are unsupported and **decode as N = 1** (chosen here: no
   hidden state, the divider never stalls). N = 1 passes `clk_pre` through.
   `clk_fb` = VCO/(8*N) = `vco_div2`/(4*N) goes to the PFD feedback flop and
   `uo_out[1]`. The prescaler and divider come out of reset cleanly with
   `vco_div2` already running. (REQ-DIV-*)
4. **Lock detector.** Clocked by `clk`. A pulse is *wide* when `pfd_up` or
   `pfd_dn` is still high at the falling edge of `clk` following the
   reference rising edge (threshold = half a reference period). Lock asserts
   after **K = 16** consecutive reference cycles without a wide pulse and
   drops on the next reference edge after any wide pulse; it is never
   asserted while pulses are wide. Output on `uo_out[2]`. (REQ-LOCK-*)
4b. **Runaway recovery.** Clocked by `clk`, next to the lock detector. With
   `pll_en` high and `lock` low at W = 1024 consecutive reference rising
   edges, a recovery starts on the 1024th: for exactly M = 128 reference
   periods `pfd_up` is held 0 and `pfd_dn` 1, which pulls Vctrl to ground,
   then the count restarts from 0. `pll_en` low or `lock` high at a
   reference edge clears the count and ends a recovery. Why: a VCO driven
   past what the first prescaler stage can divide (Vctrl near the rail at
   ss_pff reaches 310 MHz) drops edges, so `clk_fb` looks slow and the PFD
   alone would hold Vctrl at the rail for good. W x T_ref (82 us at
   12.5 MHz) is past the 50 us lock-time bound, so a loop that is still
   acquiring is never cut short. (REQ-RECOVER, REQ-RECOVER-OUT)
5. **Observation.** `obs_out` = `uo_out[0]` is `clk_pre` (VCO/8) when
   `obs_sel` = `ui_in[7]` = 0, or one more toggle flop (VCO/16) when 1.
   `uo_out[3]`/`uo_out[4]` carry `pfd_up`/`pfd_dn` for debug and stay in the
   final tile. (REQ-OBS-SEL)
6. **Control registers.** `pll_en` (from `ui_in[6]`), `cp_trim0`/`cp_trim1`
   (from `uio_in[1:0]`, inputs, `uio_oe` = 0) are registered on `clk` and
   driven to the analog macro; quasi-static. (REQ-CTRL-REG)
7. **Reset.** `rst_n` asynchronous, active low, resets everything on every
   clock domain. (REQ-RST-ASYNC)
8. **Tile tie-offs.** `uio_oe` = 0, `uio_out` = 0; `ui_in[5:4]`,
   `uio_in[7:2]` spare. No port, wire or logic named `vctrl` or `bias_ref`;
   `ua[0]`/`ua[1]` belong to the analog macro alone. (REQ-TT-TIEOFF,
   REQ-NO-UA)

### Closed loop under `ifdef SIM` (bench only)

A real-number Verilog model of pump, filter and VCO (Icp 20 uA, C1 20 pF,
R 22 kOhm, C2 2 pF, Kvco about 100 MHz/V, 50-200 MHz typical, up to 370 MHz
fast) closes the loop in CocoTB. At every (f_ref, N) point of the lock table
- (5 MHz: N 2,3,4,5), (6.25 MHz: N 1,2,3,4), (10 MHz: N 1,2), (12.5 MHz:
N 1,2) - lock rises within 50 us, the mean feedback period equals the
reference period, the VCO period equals the reference period/(8*N), the
modelled Vctrl settles, and the loop relocks after a change of N. Nothing of
the model is synthesised. (REQ-LOOP-*)

### Bench strength

The bench must kill: swapped UP/DN, missing PFD reset, divider off by one,
prescaler /4 (`clk_pre` = VCO/4). The gate-read number is the mutate gate's
sampled kill rate; the four named here are checked by `tb/named_mutants.py`
and recorded in `reports/named_mutants.json`, which no gate reads until
chip-flow #155. (REQ-MUT-KILL)

## Architecture

Core `ihsan_sa_pll` is a flat top with five submodules, one clock domain
each (the domain is the module's `clk`-shaped port; no module has two).
Instance names are fixed here because `must_keep` and the timing reports
refer to them. Every register in every module is cleared asynchronously by
`rst_n` low (REQ-RST-ASYNC); no other reset exists except the PFD's own
pulse reset.

| Instance | Module | Domain | Responsibility |
|---|---|---|---|
| `u_pre` | `pll_prescaler` | `vco_div2` | two ripple toggle flops `pre_q0`, `pre_q1`; `pre_q1` is `clk_pre` = `vco_div2`/4 = VCO/8. Stage k+1 is clocked by the rising edge of stage k's Q. Flops carry an asynchronous active-low reset (a `dffrnq`-type cell, the reset requirement overrides the `dffq_1` cell hint in Behaviour 2) and each stage's toggle loop is one flop plus one inverter, nothing else (REQ-TIM-VCO). All plain RTL: the VCO's first /2 is the macro's TSPC stage, so no stage here needs a hand-picked cell. Also holds the third toggle flop `obs_q3` (`clk_pre`/2 = VCO/16, clocked by `clk_pre`). |
| `u_div` | `pll_divider` | `clk_pre` | mod-N counter `div_cnt[2:0]` on the rising edge of `clk_pre`, N decoded from `n_sel` (0,6,7 -> 1). A single enable flop `fb_en` is clocked on the FALLING edge of `clk_pre` and is 1 for exactly one `clk_pre` cycle out of N (constant 1 when N = 1). `clk_fb` = `clk_pre` AND `fb_en`: glitch-free because `fb_en` only changes while `clk_pre` is low, and N = 1 is a pure pass-through with no clock mux. `n_sel` is a raw pin, not synchronised, and may change while running (REQ-LOOP-RELOCK): a change can cost one extra or missing `clk_fb` edge per transition and bounce, and the loop then relocks; the `>=` wrap means no code or count state stalls the divider, so exact N returns within N `clk_pre` periods (spec/cdc.yaml). |
| `u_pfd` | `pll_pfd` | `clk` and `clk_fb` (one flop each) | reference flop `pfd_ref_q` (clocked by `clk`, D = 1) and feedback flop `pfd_fb_q` (clocked by `clk_fb`, D = 1), both with an asynchronous clear driven by `~rst_n OR pfd_rst`. `pfd_rst` = AND(`pfd_ref_q`, `pfd_fb_q`) passed through two hand-instantiated, `(* keep *)` delay cells `pfd_dly0`, `pfd_dly1` (`must_keep`). `pfd_up` = `pfd_ref_q`, `pfd_dn` = `pfd_fb_q`. |
| `u_lock` | `pll_lock_det` | `clk` | recovery: `wd_cnt[9:0]` counts reference edges with `pll_en` = 1 and `lock` = 0, and `recover` (registered) rises when it reaches W - 1 = 1023, then counts the M = 128 periods of the recovery; `pll_en` = 0 or `lock` = 1 clears both. `wide_q` samples (`pfd_up` OR `pfd_dn`) on the FALLING edge of `clk` (the half-period threshold); `lock_cnt[4:0]` counts reference edges with `wide_q` = 0, saturating at 16, cleared to 0 by `wide_q` = 1; `lock` = (`lock_cnt` == 16), registered. `pfd_dn` comes from the `clk_fb` domain and is sampled by one flop only (a lock indicator tolerates a rare metastable sample; no synchroniser). |
| `u_ctrl` | `pll_ctrl_regs` | `clk` | three D flops: `pll_en` <- `pll_en_in`, `cp_trim0` <- `cp_trim_in[0]`, `cp_trim1` <- `cp_trim_in[1]` on the rising edge of `clk`. |

Top-level glue (no module): `obs_out` = `obs_sel` ? `obs_q3` : `clk_pre`
(a plain mux on a quasi-static select; `obs_sel` changes are not
glitch-protected), the recovery override `pfd_up` = `pfd_ref_q` AND NOT
`recover`, `pfd_dn` = `pfd_fb_q` OR `recover` (the lock detector samples
these, so a recovery is never clean), and the port fan-out of `clk_fb`, `pfd_up`, `pfd_dn`,
`lock` and the control registers.

Signals crossing between instances:

| Signal | From | To | Domain |
|---|---|---|---|
| `clk_pre` | `u_pre` | `u_div`, `u_pre.obs_q3`, top mux | `vco_div2`/4 = VCO/8 (generated) |
| `obs_q3` | `u_pre` | top mux | `clk_pre` |
| `clk_fb` | `u_div` | `u_pfd.pfd_fb_q` clock, port | `clk_pre`/N (generated, gated) |
| `pfd_up`, `pfd_dn` | `u_pfd` (through the recovery override) | `u_lock`, ports | `clk` / `clk_fb` |
| `recover` | `u_lock` | the recovery override | `clk` |
| `pll_en` | `u_ctrl` | `u_lock`, port | `clk` |

Clock plan for synthesis and STA (also in `spec.yaml` `timing_notes`):
`clk` is the harden's CLOCK_PORT at 80 ns; `vco_div2` is a second port clock
at 5.4 ns (7.5 ns at ss) whose only paths are the prescaler toggle loops
(min period and min pulse width, no setup paths); `clk_pre` is a generated
clock (divide-by-4 of `vco_div2`) at 20 ns covering `u_div`, `obs_q3` and the
`fb_en` half-cycle path; `clk_fb` is a generated clock (divide-by-8N) for
`pfd_fb_q`. Paths between `clk` and `clk_pre`/`clk_fb` (the PFD reset AND,
`wide_q` sampling `pfd_dn`) are false paths. The custom SDC carrying these
goes through the harden override layer in P6, since CLOCK_PORT/CLOCK_PERIOD
alone constrain only `clk`.

The `ifdef SIM` real-number loop model lives in the bench (`tb/`), never
inside `ihsan_sa_pll` or its submodules, so the synthesised netlist is
standard cells only (REQ-LOOP-MODEL-BENCH-ONLY).

## Interface

| Port | Dir | Width | Standalone TT pin | Meaning |
|---|---|---|---|---|
| `clk` | input | 1 | `clk` | reference clock, 5-12.5 MHz (constrained 12.5 MHz) |
| `rst_n` | input | 1 | `rst_n` | asynchronous active-low reset |
| `n_sel` | input | 3 | `ui_in[2:0]` | divider ratio N = 1..5; 0, 6, 7 act as N = 1 |
| `vco_div2` | input | 1 | `ui_in[3]` | crossing (a2d): VCO/2 from the macro's TSPC stage, up to 185 MHz, clocks the prescaler only |
| `pll_en_in` | input | 1 | `ui_in[6]` | PLL enable request |
| `obs_sel` | input | 1 | `ui_in[7]` | 0 = VCO/8, 1 = VCO/16 on `obs_out` |
| `cp_trim_in` | input | 2 | `uio_in[1:0]` | charge pump trim request bits |
| `obs_out` | output | 1 | `uo_out[0]` | VCO/8 or VCO/16 |
| `clk_fb` | output | 1 | `uo_out[1]` | feedback divider output, VCO/(8*N) = `vco_div2`/(4*N) |
| `lock` | output | 1 | `uo_out[2]` | lock indicator |
| `pfd_up` | output | 1 | `uo_out[3]` | crossing (d2a): PFD UP pulse, active high, pump sources Icp |
| `pfd_dn` | output | 1 | `uo_out[4]` | crossing (d2a): PFD DN pulse, active high, pump sinks Icp |
| `pll_en` | output | 1 | `uo_out[5]` | crossing (d2a): registered `ui_in[6]`; 1 enables pump, bias, VCO |
| `cp_trim0` | output | 1 | `uo_out[6]` | crossing (d2a): registered `uio_in[0]`, pump current trim bit 0 |
| `cp_trim1` | output | 1 | `uo_out[7]` | crossing (d2a): registered `uio_in[1]`, pump current trim bit 1 |

`ui_in[5:4]`, `uio_in[7:2]` spare; `uio_oe` = `uio_out` = 0; `ena` unused.
`uo_out[7:5]` carry the crossing outputs only in the standalone harden; the
msde integrator binds them to the `pll_analog` macro and may drive the pins
low in the final tile.

## Clocks and timing

| Domain | Period | Constraint |
|---|---|---|
| `clk` (clk_ref) | 80 ns | reference at 12.5 MHz: PFD reference flop, lock detector, control registers |
| `vco_div2` | 5.4 ns (7.5 ns at ss) | 2x the VCO ceiling's period per process; prescaler flops only; Liberty min period 0.93 ns ff / 1.71 ns tt and min pulse width |
| `clk_pre` | 20 ns | generated clock `vco_div2`/4 (VCO/8) at 50 MHz: divider, PFD feedback flop, /16 flop |
| `clk_fb` | <= 46 MHz | `clk_pre`/N, PFD feedback flop clock |

Keep attributes on the PFD delay chain must survive synthesis (checked in
the synthesised netlist). (REQ-TIM-*, REQ-PFD-DELAY-KEEP)

## Harden

Hardens standalone as `tt_um_ihsan_sa_pll` on the TT GF180 analog-tile
footprint with the pins above; the analog macro's area is reserved by the
msde integrator later. The joined-loop measures (divided frequency against
the real VCO, lock with the real pump, PFD reset width, phase margin) are
msde cosim measures, not this run's. (REQ-HARDEN-STANDALONE)
