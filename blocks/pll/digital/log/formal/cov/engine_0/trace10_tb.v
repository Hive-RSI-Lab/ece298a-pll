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
  reg [0:0] PI_obs_sel;
  reg [0:0] PI_vco_div2;
  wire [0:0] PI_clk = clock;
  reg [2:0] PI_n_sel;
  reg [1:0] PI_cp_trim_in;
  reg [0:0] PI_rst_n;
  reg [0:0] PI_pll_en_in;
  ihsan_sa_pll_formal UUT (
    .obs_sel(PI_obs_sel),
    .vco_div2(PI_vco_div2),
    .clk(PI_clk),
    .n_sel(PI_n_sel),
    .cp_trim_in(PI_cp_trim_in),
    .rst_n(PI_rst_n),
    .pll_en_in(PI_pll_en_in)
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
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$$flatten/dut .\/u_div .\$0/div_cnt[2:0]#sampled$526  = 3'b000;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$$flatten/dut .\/u_lock .\$0/lock[0:0]#sampled$580  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$$flatten/dut .\/u_lock .\$0/recover[0:0]#sampled$544  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$$flatten/dut .\/u_lock .\$0/wd_cnt[9:0]#sampled$562  = 10'b0000000000;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$$flatten/dut .\/u_pre .\$0/pre_q0[0:0]#sampled$702  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$$flatten/dut .\/u_pre .\$0/pre_q1[0:0]#sampled$684  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$$flatten/dut .\/u_pre .\$0/q3[0:0]#sampled$666  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_ctrl.\cp_trim0#sampled$470  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_ctrl.\cp_trim1#sampled$488  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_ctrl.\cp_trim_in[0]#sampled$472  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_ctrl.\cp_trim_in[1]#sampled$490  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_ctrl.\pll_en#sampled$452  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_ctrl.\pll_en_in#sampled$454  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_div.\div_cnt#sampled$524  = 3'b000;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_div.\fb_en#sampled$506  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_div.\last#sampled$508  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_lock.\cnt_nxt#sampled$598  = 5'b00000;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_lock.\lock#sampled$578  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_lock.\lock_cnt#sampled$596  = 5'b00000;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_lock.\recover#sampled$542  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_lock.\wd_cnt#sampled$560  = 10'b0000000000;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_lock.\wide_q#sampled$614  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_pfd.\pfd_fb_q#sampled$632  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_pfd.\pfd_ref_q#sampled$648  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_pre.\pre_q0#sampled$700  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_pre.\pre_q1#sampled$682  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:101:sample_data$/dut .u_pre.\q3#sampled$664  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:75:sample_control$$auto$rtlil .\cc:3251:Not$625#sampled$626  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:75:sample_control$/dut .u_pfd.\pfd_clr$async_cut#sampled$658  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:87:sample_control_edge$/dut .u_div.\clk_pre#sampled$510  = 1'b0;
    // UUT.$auto$clk2fflogic.\cc:87:sample_control_edge$/dut .u_pfd.\clk#sampled$652  = 1'b1;
    // UUT.$auto$clk2fflogic.\cc:87:sample_control_edge$/dut .u_pfd.\clk_fb#sampled$636  = 1'b1;
    // UUT.$auto$clk2fflogic.\cc:87:sample_control_edge$/dut .u_pre.\pre_q0#sampled$686  = 1'b1;
    // UUT.$auto$clk2fflogic.\cc:87:sample_control_edge$/dut .u_pre.\pre_q1#sampled$668  = 1'b1;
    // UUT.$auto$clk2fflogic.\cc:87:sample_control_edge$/dut .u_pre.\vco_div2#sampled$704  = 1'b1;
    UUT._witness_.anyinit_procdff_418 = 1'b0;
    UUT._witness_.anyinit_procdff_419 = 1'b0;
    UUT._witness_.anyinit_procdff_420 = 1'b0;
    UUT._witness_.anyinit_procdff_421 = 1'b0;
    UUT._witness_.anyinit_procdff_422 = 1'b0;
    UUT._witness_.anyinit_procdff_423 = 1'b0;
    UUT._witness_.anyinit_procdff_424 = 1'b0;
    UUT._witness_.anyinit_procdff_425 = 1'b0;
    UUT._witness_.anyinit_procdff_426 = 1'b0;
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
    PI_obs_sel = 1'b0;
    PI_vco_div2 = 1'b0;
    PI_n_sel = 3'b000;
    PI_cp_trim_in = 2'b00;
    PI_rst_n = 1'b0;
    PI_pll_en_in = 1'b0;
  end
  always @(posedge clock) begin
    // state 1
    if (cycle == 0) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 2
    if (cycle == 1) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 3
    if (cycle == 2) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 4
    if (cycle == 3) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 5
    if (cycle == 4) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 6
    if (cycle == 5) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 7
    if (cycle == 6) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 8
    if (cycle == 7) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 9
    if (cycle == 8) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 10
    if (cycle == 9) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 11
    if (cycle == 10) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 12
    if (cycle == 11) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 13
    if (cycle == 12) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 14
    if (cycle == 13) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 15
    if (cycle == 14) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 16
    if (cycle == 15) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 17
    if (cycle == 16) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 18
    if (cycle == 17) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 19
    if (cycle == 18) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 20
    if (cycle == 19) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 21
    if (cycle == 20) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 22
    if (cycle == 21) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 23
    if (cycle == 22) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 24
    if (cycle == 23) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 25
    if (cycle == 24) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 26
    if (cycle == 25) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 27
    if (cycle == 26) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 28
    if (cycle == 27) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 29
    if (cycle == 28) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 30
    if (cycle == 29) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 31
    if (cycle == 30) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 32
    if (cycle == 31) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 33
    if (cycle == 32) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 34
    if (cycle == 33) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 35
    if (cycle == 34) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 36
    if (cycle == 35) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 37
    if (cycle == 36) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 38
    if (cycle == 37) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 39
    if (cycle == 38) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 40
    if (cycle == 39) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 41
    if (cycle == 40) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 42
    if (cycle == 41) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 43
    if (cycle == 42) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 44
    if (cycle == 43) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 45
    if (cycle == 44) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 46
    if (cycle == 45) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 47
    if (cycle == 46) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 48
    if (cycle == 47) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 49
    if (cycle == 48) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 50
    if (cycle == 49) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 51
    if (cycle == 50) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 52
    if (cycle == 51) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 53
    if (cycle == 52) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 54
    if (cycle == 53) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 55
    if (cycle == 54) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 56
    if (cycle == 55) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 57
    if (cycle == 56) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 58
    if (cycle == 57) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 59
    if (cycle == 58) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 60
    if (cycle == 59) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 61
    if (cycle == 60) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 62
    if (cycle == 61) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 63
    if (cycle == 62) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 64
    if (cycle == 63) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 65
    if (cycle == 64) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 66
    if (cycle == 65) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 67
    if (cycle == 66) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 68
    if (cycle == 67) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 69
    if (cycle == 68) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 70
    if (cycle == 69) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 71
    if (cycle == 70) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 72
    if (cycle == 71) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 73
    if (cycle == 72) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 74
    if (cycle == 73) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 75
    if (cycle == 74) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 76
    if (cycle == 75) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 77
    if (cycle == 76) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 78
    if (cycle == 77) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 79
    if (cycle == 78) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 80
    if (cycle == 79) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 81
    if (cycle == 80) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 82
    if (cycle == 81) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 83
    if (cycle == 82) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 84
    if (cycle == 83) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 85
    if (cycle == 84) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 86
    if (cycle == 85) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 87
    if (cycle == 86) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 88
    if (cycle == 87) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 89
    if (cycle == 88) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 90
    if (cycle == 89) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 91
    if (cycle == 90) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 92
    if (cycle == 91) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 93
    if (cycle == 92) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 94
    if (cycle == 93) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 95
    if (cycle == 94) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 96
    if (cycle == 95) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 97
    if (cycle == 96) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 98
    if (cycle == 97) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 99
    if (cycle == 98) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 100
    if (cycle == 99) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 101
    if (cycle == 100) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 102
    if (cycle == 101) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 103
    if (cycle == 102) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 104
    if (cycle == 103) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 105
    if (cycle == 104) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 106
    if (cycle == 105) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 107
    if (cycle == 106) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 108
    if (cycle == 107) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 109
    if (cycle == 108) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 110
    if (cycle == 109) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 111
    if (cycle == 110) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 112
    if (cycle == 111) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 113
    if (cycle == 112) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 114
    if (cycle == 113) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 115
    if (cycle == 114) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 116
    if (cycle == 115) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b1;
    end

    // state 117
    if (cycle == 116) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 118
    if (cycle == 117) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 119
    if (cycle == 118) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 120
    if (cycle == 119) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 121
    if (cycle == 120) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b110;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 122
    if (cycle == 121) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b1;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 123
    if (cycle == 122) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    // state 124
    if (cycle == 123) begin
      PI_obs_sel <= 1'b0;
      PI_vco_div2 <= 1'b0;
      PI_n_sel <= 3'b000;
      PI_cp_trim_in <= 2'b00;
      PI_rst_n <= 1'b1;
      PI_pll_en_in <= 1'b0;
    end

    genclock <= cycle < 124;
    cycle <= cycle + 1;
  end
endmodule
