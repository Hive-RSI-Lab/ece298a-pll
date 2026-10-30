`default_nettype none
`timescale 1ns / 1ps

/* The testbench: the Tiny Tapeout top with named wires for the cocotb test
   (test.py). In the RTL test the analog macro is test/pll_analog_model.v. */
module tb ();

  // Dump the signals to a FST file. You can view it with gtkwave or surfer.
  initial begin
    $dumpfile("tb.fst");
    $dumpvars(0, tb);
    #1;
  end

  reg clk;
  reg rst_n;
  reg ena;
  reg [7:0] ui_in;
  reg [7:0] uio_in;
  wire [7:0] uo_out;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;
  wire [7:0] ua;
  wire VDPWR = 1'b1;
  wire VGND = 1'b0;

  tt_um_ihsan_sa_pll user_project (
      .VGND   (VGND),
      .VDPWR  (VDPWR),
      .ui_in  (ui_in),    // Dedicated inputs
      .uo_out (uo_out),   // Dedicated outputs
      .uio_in (uio_in),   // IOs: Input path
      .uio_out(uio_out),  // IOs: Output path
      .uio_oe (uio_oe),   // IOs: Enable path (active high: 0=input, 1=output)
      .ua     (ua),       // Analog pads: ua[0] VCTRL, ua[1] BIAS_REF
      .ena    (ena),      // enable - goes high when design is selected
      .clk    (clk),      // reference clock
      .rst_n  (rst_n)     // not reset
  );

  // the outputs by name, for the test
  wire obs_out = uo_out[0];
  wire clk_fb  = uo_out[1];
  wire lock    = uo_out[2];

endmodule
