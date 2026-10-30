// pll_analog - port list of the analog hard macro (blocks/pll/analog):
// charge pump, loop filter, current-starved ring VCO and bias. Its layout is
// blocks/pll/analog/layout/pll_analog.gds. A blackbox for synthesis; the
// RTL test (test/) gives it a behavioural body, test/pll_analog_model.v.
`default_nettype none
`ifndef PLL_ANALOG_MODEL
(* blackbox *)
module pll_analog (
    inout  wire vdd,
    inout  wire vss,
    input  wire cp_trim0,
    input  wire cp_trim1,
    input  wire pfd_dn,
    input  wire pfd_up,
    input  wire pll_en,
    output wire vco_out,
    inout  wire bias_ref,
    inout  wire vctrl
);
endmodule
`endif
`default_nettype wire
