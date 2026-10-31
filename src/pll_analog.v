// pll_analog - port list of the analog hard macro (blocks/pll/analog):
// charge pump, loop filter, current-starved ring VCO, bias and the TSPC /2
// whose output vco_div2 (the VCO divided by 2) clocks the digital half. Its layout is
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
    output wire vco_div2,
    inout  wire bias_ref,
    inout  wire vctrl
);
endmodule
`endif
`default_nettype wire
