// pll_analog_model.v - a behavioural model of the analog macro, for the
// RTL test only (never synthesised). The numbers are blocks/pll/tb's
// calibration of the real netlist at tt_27c (pll_analog_cal.json, written by
// calibrate_analog.py): the VCO's f(vctrl) in 0.1 V steps, the pump current
// per trim code at vctrl = vdd/2, and the loop filter fitted to the cell's own
// vctrl impedance, R1 + 1/(s C1) in parallel with 1/(s C2).
//
// The filter is stepped every STEP_NS (explicit Euler; R1*C2 is about
// 58 ns). The VCO toggles at exact real-valued times,
// so the divided clocks carry no step quantisation. pll_en low stops the
// VCO and the pump, as the cell's power-down does. The pin is vco_div2,
// the VCO divided by 2 in the macro (issue #48).
`timescale 1ns / 1ps
`default_nettype none
module pll_analog (
    inout  wire vdd,
    inout  wire vss,
    input  wire cp_trim0,
    input  wire cp_trim1,
    input  wire pfd_dn,
    input  wire pfd_up,
    input  wire pll_en,
    output reg  vco_div2,
    inout  wire bias_ref,
    inout  wire vctrl
);
  localparam real STEP_NS = 0.25;
  localparam real VDD = 3.3;
  localparam real R1 = 27013.7;          // ohm
  localparam real C1 = 2.0004e-11;      // F
  localparam real C2 = 2.1431e-12;      // F
  real f_tbl [0:33];                  // MHz at vctrl = 0.1 * index V
  real v1 = 0.0;                         // C1's voltage
  real v2 = 0.0;                         // vctrl
  real icp, i_in, f_mhz;
  reg vco_out;                           // the VCO, internal to the macro

  initial begin
    f_tbl[0] = 9.188;
    f_tbl[1] = 9.188;
    f_tbl[2] = 9.188;
    f_tbl[3] = 9.189;
    f_tbl[4] = 9.195;
    f_tbl[5] = 9.281;
    f_tbl[6] = 10.073;
    f_tbl[7] = 13.188;
    f_tbl[8] = 18.813;
    f_tbl[9] = 26.020;
    f_tbl[10] = 34.259;
    f_tbl[11] = 43.259;
    f_tbl[12] = 52.875;
    f_tbl[13] = 63.019;
    f_tbl[14] = 73.626;
    f_tbl[15] = 84.643;
    f_tbl[16] = 96.020;
    f_tbl[17] = 107.724;
    f_tbl[18] = 119.708;
    f_tbl[19] = 131.936;
    f_tbl[20] = 144.366;
    f_tbl[21] = 156.955;
    f_tbl[22] = 169.662;
    f_tbl[23] = 182.433;
    f_tbl[24] = 195.203;
    f_tbl[25] = 207.887;
    f_tbl[26] = 220.370;
    f_tbl[27] = 232.428;
    f_tbl[28] = 243.648;
    f_tbl[29] = 252.861;
    f_tbl[30] = 257.756;
    f_tbl[31] = 259.371;
    f_tbl[32] = 260.125;
    f_tbl[33] = 260.547;
    vco_out = 1'b0;
    vco_div2 = 1'b0;
  end

  function real f_of(input real v);
    integer k;
    real x;
    begin
      x = v / 0.1;
      if (x <= 0.0) f_of = f_tbl[0];
      else if (x >= 33.0) f_of = f_tbl[33];
      else begin
        k = $rtoi(x);
        f_of = f_tbl[k] + (x - k) * (f_tbl[k + 1] - f_tbl[k]);
      end
    end
  endfunction

  always @(*) case ({cp_trim1, cp_trim0})
    2'b00: icp = 1.9014e-05;
    2'b01: icp = 2.3675e-05;
    2'b10: icp = 2.8322e-05;
    default: icp = 3.7587e-05;
  endcase

  // the loop filter
  always begin
    #(STEP_NS);
    i_in = (pll_en && pfd_up ? icp : 0.0) - (pll_en && pfd_dn ? icp : 0.0);
    v1 = v1 + (v2 - v1) / R1 / C1 * STEP_NS * 1e-9;
    v2 = v2 + (i_in - (v2 - v1) / R1) / C2 * STEP_NS * 1e-9;
    if (v2 > VDD) v2 = VDD;
    if (v2 < 0.0) v2 = 0.0;
  end

  // the VCO: each half period from f at that moment
  always begin
    if (!pll_en) begin
      vco_out = 1'b0;
      @(posedge pll_en);
    end else begin
      f_mhz = f_of(v2);
      #(500.0 / f_mhz);
      vco_out = ~vco_out;
    end
  end

  // the TSPC /2 (issue #48): vco_div2 toggles on every rising vco_out and
  // holds while pll_en is low (the cell's MP_DR keeps its state node static)
  always @(posedge vco_out) vco_div2 <= ~vco_div2;

  // vctrl is the filter node; a test reads it as v2 (ua[0] carries no level
  // in a digital simulator)
  wire _unused = &{vdd, vss, bias_ref, vctrl, 1'b0};
endmodule
`default_nettype wire
