/*
 * Copyright (c) 2026 Ihsan Salari
 * SPDX-License-Identifier: Apache-2.0
 *
 * tt_um_ihsan_sa_pll - the Tiny Tapeout top of the charge-pump PLL: the
 * digital core (ihsan_sa_pll) and the analog macro (pll_analog). The code is
 * chip-flow's ttlib.generate_tt_project of top/spec/spec.yaml: top_harden's
 * hardened wrapper (top/harden/tt_um_ihsan_sa_pll.v) plus the analog
 * template's VGND/VDPWR ports and the macro's power ties; release refuses it
 * if the logic differs. gds.yaml's verilog_path points here.
 */
`default_nettype none

module tt_um_ihsan_sa_pll (
    input  wire       VGND,
    input  wire       VDPWR,
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    inout  wire [7:0] ua,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);
  wire w_clk;
  assign w_clk = clk;
  wire w_clk_fb;
  wire w_cp_trim0;
  wire w_cp_trim1;
  wire [1:0] w_cp_trim_in;
  assign w_cp_trim_in = uio_in[1:0];
  wire w_lock;
  wire [2:0] w_n_sel;
  assign w_n_sel = ui_in[2:0];
  wire w_obs_out;
  wire w_obs_sel;
  assign w_obs_sel = ui_in[7];
  wire w_pfd_dn;
  wire w_pfd_up;
  wire w_pll_en;
  wire w_pll_en_in;
  assign w_pll_en_in = ui_in[6];
  wire w_rst_n;
  assign w_rst_n = rst_n;
  wire w_vco_div2;

  ihsan_sa_pll u_ihsan_sa_pll (
      .clk(w_clk),
      .clk_fb(w_clk_fb),
      .cp_trim0(w_cp_trim0),
      .cp_trim1(w_cp_trim1),
      .cp_trim_in(w_cp_trim_in),
      .lock(w_lock),
      .n_sel(w_n_sel),
      .obs_out(w_obs_out),
      .obs_sel(w_obs_sel),
      .pfd_dn(w_pfd_dn),
      .pfd_up(w_pfd_up),
      .pll_en(w_pll_en),
      .pll_en_in(w_pll_en_in),
      .rst_n(w_rst_n),
      .vco_div2(w_vco_div2)
  );

  pll_analog u_analog (
`ifdef USE_POWER_PINS
      .vdd(VDPWR),
      .vss(VGND),
`endif
      .cp_trim0(w_cp_trim0),
      .cp_trim1(w_cp_trim1),
      .pfd_dn(w_pfd_dn),
      .pfd_up(w_pfd_up),
      .pll_en(w_pll_en),
      .vco_div2(w_vco_div2),
      .bias_ref(ua[1]),
      .vctrl(ua[0])
  );

  assign uo_out = {1'b0, 1'b0, 1'b0, 1'b0, 1'b0, w_lock, w_clk_fb, w_obs_out};
  assign uio_out = {1'b0, 1'b0, 1'b0, 1'b0, 1'b0, 1'b0, 1'b0, 1'b0};
  assign uio_oe = 8'b00000000;
  wire _unused = &{ena, ui_in[3], ui_in[4], ui_in[5], uio_in[2], uio_in[3], uio_in[4], uio_in[5], uio_in[6], uio_in[7], 1'b0};
endmodule
`default_nettype wire
