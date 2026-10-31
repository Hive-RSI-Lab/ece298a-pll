// pll_prescaler - /4 ripple prescaler on vco_div2 plus the /8 observation flop.
// vco_div2 is VCO/2 from the TSPC divider inside the analog macro (issue
// #48), so clk_pre = vco_div2/4 = VCO/8 and obs_q3 = vco_div2/8 = VCO/16,
// the same ratios to the VCO as before the macro took the first /2.
// Domain: vco_div2 (pre_q0), rippled on rising edges of each stage's Q.
// Each stage's toggle loop is one async-reset flop and one inverter. With
// the first library stage at VCO/2 its toggle loop has twice the VCO period
// to close in, so it is plain RTL again (it used to be a hand-instantiated
// dffrnq_2 + inv_1 that closed at ss within 0.03 ns of the VCO ceiling).
`default_nettype none
module pll_prescaler (
    input  wire vco_div2,
    input  wire rst_n,
    output wire clk_pre,   // vco_div2 / 4 (VCO / 8)
    output wire obs_q3     // vco_div2 / 8 (VCO / 16, clk_pre / 2)
);
  reg pre_q0, pre_q1, q3;

  always @(posedge vco_div2 or negedge rst_n)
    if (!rst_n) pre_q0 <= 1'b0;
    else        pre_q0 <= ~pre_q0;

  always @(posedge pre_q0 or negedge rst_n)
    if (!rst_n) pre_q1 <= 1'b0;
    else        pre_q1 <= ~pre_q1;

  always @(posedge pre_q1 or negedge rst_n)
    if (!rst_n) q3 <= 1'b0;
    else        q3 <= ~q3;

  assign clk_pre = pre_q1;
  assign obs_q3  = q3;
endmodule
`default_nettype wire
