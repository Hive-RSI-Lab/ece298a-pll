/*
 * Copyright (c) 2026 Ihsan Salari
 * SPDX-License-Identifier: Apache-2.0
 *
 * tt_um_ihsan_sa_pll - the Tiny Tapeout top of the charge-pump PLL: the
 * digital core (ihsan_sa_pll: prescaler, divider, PFD, lock detector,
 * control registers) and the analog macro (pll_analog: charge pump, loop
 * filter, ring VCO, bias), wired as chip-flow's top_harden assembles them
 * (engine/lib/ttlib.py generate_tt_wrapper, from blocks/pll/interface.yaml).
 * The port list is Tiny Tapeout's GF180 analog template's.
 */

`default_nettype none

module tt_um_ihsan_sa_pll (
    input  wire       VGND,
    input  wire       VDPWR,    // 3.3 V supply
    input  wire [7:0] ui_in,    // ui[2:0] N_SEL, ui[6] PLL_EN, ui[7] OBS_SEL
    output wire [7:0] uo_out,   // uo[0] OBS_OUT, uo[1] CLK_FB, uo[2] LOCK
    input  wire [7:0] uio_in,   // uio[1:0] CP_TRIM
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    inout  wire [7:0] ua,       // ua[0] VCTRL, ua[1] BIAS_REF
    input  wire       ena,
    input  wire       clk,      // reference clock, 5 to 12.5 MHz
    input  wire       rst_n
);
  wire clk_fb, lock, obs_out;
  wire pfd_up, pfd_dn, pll_en, cp_trim0, cp_trim1, vco_out;

  ihsan_sa_pll u_ihsan_sa_pll (
      .clk(clk),
      .rst_n(rst_n),
      .n_sel(ui_in[2:0]),
      .vco_out(vco_out),
      .pll_en_in(ui_in[6]),
      .obs_sel(ui_in[7]),
      .cp_trim_in(uio_in[1:0]),
      .obs_out(obs_out),
      .clk_fb(clk_fb),
      .lock(lock),
      .pfd_up(pfd_up),
      .pfd_dn(pfd_dn),
      .pll_en(pll_en),
      .cp_trim0(cp_trim0),
      .cp_trim1(cp_trim1)
  );

  pll_analog u_pll_analog (
      .vdd(VDPWR),
      .vss(VGND),
      .cp_trim0(cp_trim0),
      .cp_trim1(cp_trim1),
      .pfd_dn(pfd_dn),
      .pfd_up(pfd_up),
      .pll_en(pll_en),
      .vco_out(vco_out),
      .bias_ref(ua[1]),
      .vctrl(ua[0])
  );

  assign uo_out  = {5'b0, lock, clk_fb, obs_out};
  assign uio_out = 8'b0;
  assign uio_oe  = 8'b0;

  wire _unused = &{ena, ui_in[5:3], uio_in[7:2], 1'b0};
endmodule

`default_nettype wire
