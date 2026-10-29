`ifndef VERILATOR
module testbench;
  reg [4095:0] vcdfile;
  reg clock;
`else
module testbench(input clock, output reg genclock);
  initial genclock = 1;
`endif
  reg genclock = 1;
  reg [31:0] cycle = 0;
  reg [2:0] PI_n_sel;
  reg [0:0] PI_rst_n;
  wire [0:0] PI_clk = clock;
  reg [0:0] PI_vco_out;
  reg [0:0] PI_pll_en_in;
  reg [0:0] PI_obs_sel;
  reg [1:0] PI_cp_trim_in;
  ihsan_sa_pll_formal UUT (
    .n_sel(PI_n_sel),
    .rst_n(PI_rst_n),
    .clk(PI_clk),
    .vco_out(PI_vco_out),
    .pll_en_in(PI_pll_en_in),
    .obs_sel(PI_obs_sel),
    .cp_trim_in(PI_cp_trim_in)
  );
`ifndef VERILATOR
  initial begin
    if ($value$plusargs("vcd=%s", vcdfile)) begin
      $dumpfile(vcdfile);
      $dumpvars(0, testbench);
    end
    #5 clock = 0;
    while (genclock) begin
      #5 clock = 0;
      #5 clock = 1;
    end
  end
`endif
  initial begin
`ifndef VERILATOR
    #1;
`endif
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$$flatten/dut .\/u_div .\$0/div_cnt[2:0]#sampled$494  = 3'b000;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$$flatten/dut .\/u_lock .\$0/lock[0:0]#sampled$512  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$$flatten/dut .\/u_pre .\$0/pre_q0[0:0]#sampled$652  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$$flatten/dut .\/u_pre .\$0/pre_q1[0:0]#sampled$634  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$$flatten/dut .\/u_pre .\$0/pre_q2[0:0]#sampled$616  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$$flatten/dut .\/u_pre .\$0/q3[0:0]#sampled$598  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_ctrl.\cp_trim0#sampled$438  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_ctrl.\cp_trim1#sampled$456  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_ctrl.\cp_trim_in[0]#sampled$440  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_ctrl.\cp_trim_in[1]#sampled$458  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_ctrl.\pll_en#sampled$420  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_ctrl.\pll_en_in#sampled$422  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_div.\div_cnt#sampled$492  = 3'b000;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_div.\fb_en#sampled$474  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_div.\last#sampled$476  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_lock.\cnt_nxt#sampled$530  = 5'b00000;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_lock.\lock#sampled$510  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_lock.\lock_cnt#sampled$528  = 5'b00000;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_lock.\wide_q#sampled$546  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_pfd.\pfd_fb_q#sampled$564  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_pfd.\pfd_ref_q#sampled$580  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_pre.\pre_q0#sampled$650  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_pre.\pre_q1#sampled$632  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_pre.\pre_q2#sampled$614  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_pre.\q3#sampled$596  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:75:sample_control$$auto$rtlil .\cc:3251:Not$557#sampled$558  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:75:sample_control$/dut .u_pfd.\pfd_clr$async_cut#sampled$590  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:87:sample_control_edge$/dut .u_div.\clk_pre#sampled$478  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:87:sample_control_edge$/dut .u_pfd.\clk#sampled$584  = 1'b1;
    // UUT.$auto$clk2fflogic.\cc:87:sample_control_edge$/dut .u_pfd.\clk_fb#sampled$568  = 1'b1;
    // UUT.$auto$clk2fflogic.\cc:87:sample_control_edge$/dut .u_pre.\pre_q0#sampled$636  = 1'b1;
    // UUT.$auto$clk2fflogic.\cc:87:sample_control_edge$/dut .u_pre.\pre_q1#sampled$618  = 1'b1;
    // UUT.$auto$clk2fflogic.\cc:87:sample_control_edge$/dut .u_pre.\pre_q2#sampled$600  = 1'b1;
    // UUT.$auto$clk2fflogic.\cc:87:sample_control_edge$/dut .u_pre.\vco_out#sampled$654  = 1'b1;
    UUT._witness_.anyinit_procdff_387 = 1'b0;
    UUT._witness_.anyinit_procdff_388 = 1'b0;
    UUT._witness_.anyinit_procdff_389 = 1'b0;
    UUT._witness_.anyinit_procdff_390 = 1'b0;
    UUT._witness_.anyinit_procdff_391 = 1'b0;
    UUT._witness_.anyinit_procdff_392 = 1'b0;
    UUT._witness_.anyinit_procdff_393 = 1'b0;
    UUT._witness_.anyinit_procdff_394 = 1'b0;
    UUT.clk_q = 1'b0;
    UUT.dut.u_pfd.pfd_fb_q$async_arst_past = 1'b0;
    UUT.dut.u_pfd.pfd_fb_q$async_clk_past = 1'b0;
    UUT.dut.u_pfd.pfd_fb_q$async_d_past = 1'b0;
    UUT.dut.u_pfd.pfd_fb_q$async_q_past = 1'b0;
    UUT.dut.u_pfd.pfd_ref_q$async_arst_past = 1'b0;
    UUT.dut.u_pfd.pfd_ref_q$async_clk_past = 1'b0;
    UUT.dut.u_pfd.pfd_ref_q$async_d_past = 1'b0;
    UUT.dut.u_pfd.pfd_ref_q$async_q_past = 1'b0;
    UUT.fb_ok = 1'b0;
    UUT.fb_q = 1'b0;
    UUT.fb_seen = 1'b0;
    UUT.hist = 16'b1111111111111111;
    UUT.hist_q = 16'b1111111111111111;
    UUT.n_last = 3'b001;
    UUT.n_q = 3'b001;
    UUT.n_stab = 1'b1;
    UUT.obs_q = 1'b0;
    UUT.past_valid = 1'b0;
    UUT.pre_cnt = 4'b0000;
    UUT.pre_ok = 1'b0;
    UUT.pre_seen = 1'b0;
    UUT.prep_q = 1'b0;
    UUT.vco_cnt = 4'b0000;
    UUT.vco_q = 1'b0;
    UUT.wide_q = 1'b0;
    UUT.wide_s = 1'b1;

    // state 0
    PI_n_sel = 3'b000;
    PI_rst_n = 1'b0;
    PI_vco_out = 1'b0;
    PI_pll_en_in = 1'b0;
    PI_obs_sel = 1'b0;
    PI_cp_trim_in = 2'b00;
  end
  always @(posedge clock) begin
    // state 1
    if (cycle == 0) begin
      PI_n_sel <= 3'b110;
      PI_rst_n <= 1'b1;
      PI_vco_out <= 1'b0;
      PI_pll_en_in <= 1'b0;
      PI_obs_sel <= 1'b0;
      PI_cp_trim_in <= 2'b00;
    end

    // state 2
    if (cycle == 1) begin
      PI_n_sel <= 3'b111;
      PI_rst_n <= 1'b1;
      PI_vco_out <= 1'b1;
      PI_pll_en_in <= 1'b0;
      PI_obs_sel <= 1'b0;
      PI_cp_trim_in <= 2'b00;
    end

    // state 3
    if (cycle == 2) begin
      PI_n_sel <= 3'b110;
      PI_rst_n <= 1'b1;
      PI_vco_out <= 1'b0;
      PI_pll_en_in <= 1'b0;
      PI_obs_sel <= 1'b0;
      PI_cp_trim_in <= 2'b00;
    end

    // state 4
    if (cycle == 3) begin
      PI_n_sel <= 3'b000;
      PI_rst_n <= 1'b1;
      PI_vco_out <= 1'b1;
      PI_pll_en_in <= 1'b0;
      PI_obs_sel <= 1'b0;
      PI_cp_trim_in <= 2'b00;
    end

    // state 5
    if (cycle == 4) begin
      PI_n_sel <= 3'b000;
      PI_rst_n <= 1'b1;
      PI_vco_out <= 1'b0;
      PI_pll_en_in <= 1'b0;
      PI_obs_sel <= 1'b0;
      PI_cp_trim_in <= 2'b00;
    end

    // state 6
    if (cycle == 5) begin
      PI_n_sel <= 3'b000;
      PI_rst_n <= 1'b1;
      PI_vco_out <= 1'b1;
      PI_pll_en_in <= 1'b0;
      PI_obs_sel <= 1'b0;
      PI_cp_trim_in <= 2'b00;
    end

    // state 7
    if (cycle == 6) begin
      PI_n_sel <= 3'b000;
      PI_rst_n <= 1'b1;
      PI_vco_out <= 1'b0;
      PI_pll_en_in <= 1'b0;
      PI_obs_sel <= 1'b0;
      PI_cp_trim_in <= 2'b00;
    end

    // state 8
    if (cycle == 7) begin
      PI_n_sel <= 3'b000;
      PI_rst_n <= 1'b1;
      PI_vco_out <= 1'b1;
      PI_pll_en_in <= 1'b0;
      PI_obs_sel <= 1'b0;
      PI_cp_trim_in <= 2'b00;
    end

    // state 9
    if (cycle == 8) begin
      PI_n_sel <= 3'b110;
      PI_rst_n <= 1'b1;
      PI_vco_out <= 1'b0;
      PI_pll_en_in <= 1'b0;
      PI_obs_sel <= 1'b0;
      PI_cp_trim_in <= 2'b00;
    end

    // state 10
    if (cycle == 9) begin
      PI_n_sel <= 3'b110;
      PI_rst_n <= 1'b1;
      PI_vco_out <= 1'b1;
      PI_pll_en_in <= 1'b0;
      PI_obs_sel <= 1'b0;
      PI_cp_trim_in <= 2'b00;
    end

    // state 11
    if (cycle == 10) begin
      PI_n_sel <= 3'b111;
      PI_rst_n <= 1'b1;
      PI_vco_out <= 1'b0;
      PI_pll_en_in <= 1'b0;
      PI_obs_sel <= 1'b0;
      PI_cp_trim_in <= 2'b00;
    end

    // state 12
    if (cycle == 11) begin
      PI_n_sel <= 3'b000;
      PI_rst_n <= 1'b1;
      PI_vco_out <= 1'b1;
      PI_pll_en_in <= 1'b0;
      PI_obs_sel <= 1'b0;
      PI_cp_trim_in <= 2'b00;
    end

    // state 13
    if (cycle == 12) begin
      PI_n_sel <= 3'b000;
      PI_rst_n <= 1'b1;
      PI_vco_out <= 1'b0;
      PI_pll_en_in <= 1'b0;
      PI_obs_sel <= 1'b0;
      PI_cp_trim_in <= 2'b00;
    end

    // state 14
    if (cycle == 13) begin
      PI_n_sel <= 3'b000;
      PI_rst_n <= 1'b1;
      PI_vco_out <= 1'b1;
      PI_pll_en_in <= 1'b0;
      PI_obs_sel <= 1'b0;
      PI_cp_trim_in <= 2'b00;
    end

    // state 15
    if (cycle == 14) begin
      PI_n_sel <= 3'b110;
      PI_rst_n <= 1'b1;
      PI_vco_out <= 1'b0;
      PI_pll_en_in <= 1'b0;
      PI_obs_sel <= 1'b0;
      PI_cp_trim_in <= 2'b00;
    end

    // state 16
    if (cycle == 15) begin
      PI_n_sel <= 3'b110;
      PI_rst_n <= 1'b1;
      PI_vco_out <= 1'b1;
      PI_pll_en_in <= 1'b0;
      PI_obs_sel <= 1'b0;
      PI_cp_trim_in <= 2'b00;
    end

    // state 17
    if (cycle == 16) begin
      PI_n_sel <= 3'b000;
      PI_rst_n <= 1'b1;
      PI_vco_out <= 1'b0;
      PI_pll_en_in <= 1'b0;
      PI_obs_sel <= 1'b0;
      PI_cp_trim_in <= 2'b00;
    end

    // state 18
    if (cycle == 17) begin
      PI_n_sel <= 3'b000;
      PI_rst_n <= 1'b1;
      PI_vco_out <= 1'b1;
      PI_pll_en_in <= 1'b0;
      PI_obs_sel <= 1'b0;
      PI_cp_trim_in <= 2'b00;
    end

    genclock <= cycle < 18;
    cycle <= cycle + 1;
  end
endmodule
