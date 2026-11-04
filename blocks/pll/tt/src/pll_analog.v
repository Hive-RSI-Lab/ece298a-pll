// pll_analog - port list of the analog hard macro (blocks/pll/analog). The
// code is top_harden's blackbox (top/macros/pll_analog.v); release refuses it
// if they differ. The RTL test leaves this file out and uses
// test/pll_analog_model.v, a behavioural body.
(* blackbox *)
module pll_analog (
`ifdef USE_POWER_PINS
    inout  wire vdd,
    inout  wire vss,
`endif
    input  wire cp_trim0,
    input  wire cp_trim1,
    input  wire pfd_dn,
    input  wire pfd_up,
    input  wire pll_en,
    output wire vco_div2,
    inout  wire bias_ref,
    inout  wire vctrl
);
endmodule
