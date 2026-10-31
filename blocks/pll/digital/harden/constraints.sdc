# Design SDC for tt_um_ihsan_sa_pll, sourced after LibreLane's base.sdc,
# which already defines the primary clock clk (spec clock.period_ns, 80 ns).
# Names are the flat (post-synth) netlist's: yosys flattening keeps one of
# a net's hierarchical aliases, so each clock net is looked up by every
# alias it can carry, and the clock goes on the driving flop's output pin.
# No leading wildcard: CTS adds clknet_*/clkbuf_* nets that end in the same
# names, and a pattern matching them gives a generated clock several masters.

proc pll_driver_pin {aliases} {
    foreach a $aliases {
        set nets [get_nets -quiet $a]
        if {[llength $nets] > 0} {
            set pins [get_pins -quiet -of_objects $nets -filter "direction == output"]
            if {[llength $pins] > 0} { return $pins }
        }
    }
    error "constraints.sdc: no net matches any of {$aliases}"
}

# vco_div2: VCO/2 from the TSPC divider inside the analog macro (issue #48),
# full swing, ~50% duty, on ui_in[3] in the standalone tile. It is timed per
# process at twice the period of the fastest the extracted VCO runs on that
# process (vctrl at the rail, any temperature, supply or resistor skew:
# analog/reports/recorded/pex_pvt.json vco_f_vdd_mhz), plus margin. The VCO
# and these flops share a die, so an ss STA corner meets an ss VCO.
# Post-layout ceilings: ss 263.3 MHz (ss_pff), tt 290.7 (tt_pff), ff 299.5
# (ff_m40c_vm10), read from the settled ring on the MOS-cap filter layout
# (2026-10-30).
#   ss 7.5 ns: 2 x 3.75 ns, VCO 267 MHz, just over the ss ceiling. ss_pff
#      (ss, 125 C, 3.0 V, fast resistor) is the corner ss_125C_3v00 times,
#      its slowest flops against its fastest VCO. The first library stage's
#      toggle loop is plain RTL now (dffrnq_1, CTS's clkbuf_8 on its Q, and
#      the inverter on that buffer's leaf): routed at max_ss_125C_3v00 (5%
#      derate) it arrives at 4.80 ns, so ss setup reads +2.34..+2.39 ns
#      (harden 2026-10-31, issue #48), against -0.03..+0.004 when the stage
#      ran at the VCO itself. The loop would keep up with a VCO near 388 MHz
#      at ss, 47% above the ss ceiling.
#   tt, ff 5.4 ns: 2 x 2.7 ns, VCO 370 MHz (the analog spec's vco_fmax
#      ceiling), 24-27% above their post-layout ceilings; setup +2.74 (tt),
#      +3.79 (ff) ns.
# Each STA corner links one process's liberty, so the period follows the
# liberty loaded; with several loaded (or none recognised) the tightest wins.
# tests/score.py reads this table (vco_div2 periods, ns) and checks each is
# within twice the VCO period at the post-layout ceiling it measures.
set pll_vco_div2_period_ns {ss 7.5 tt 5.4 ff 5.4}
proc pll_vco_div2_period {} {
    global pll_vco_div2_period_ns
    set per {}
    foreach lib [get_libs -quiet *] {
        set n [get_name $lib]
        dict for {proc_corner p} $pll_vco_div2_period_ns {
            if {[string match "*__${proc_corner}_*" $n]} { lappend per $p }
        }
    }
    if {[llength $per] == 0} {
        set per [dict values $pll_vco_div2_period_ns]
    }
    return [tcl::mathfunc::min {*}$per]
}
create_clock -name vco_div2 -period [pll_vco_div2_period] [get_ports {ui_in[3]}]

# The /4 ripple prescaler on vco_div2 plus the /8 observation flop: each
# stage clocks the next, so each stage's Q is a generated clock.
set pll_pre_q0 [pll_driver_pin {u_ihsan_sa_pll.u_pre.pre_q0}]
set pll_pre_q1 [pll_driver_pin {u_ihsan_sa_pll.clk_pre u_ihsan_sa_pll.u_pre.pre_q1}]
create_generated_clock -name pre_q0 -source [get_ports {ui_in[3]}] -divide_by 2 $pll_pre_q0
# clk_pre = vco_div2/4 = VCO/8 (21.6 ns at tt and ff, 30 ns at ss). It has
# to be a generated clock: a create_clock on the stage-1 Q pin gives that
# flop's own toggle loop zero launch latency against a propagated capture
# clock, a false hold violation. REQ-TIM-PRE's 20 ns is tighter; harden run
# 2 (clk_pre at 20 ns) met it with 3.3 ns of setup slack at ss.
# clk_fb = clk_pre & fb_en is the same clock passed through a gate, so
# STA propagates clk_pre through it to the divider's and PFD's flops.
create_generated_clock -name clk_pre -source $pll_pre_q0 -divide_by 2 $pll_pre_q1

# Setup uncertainty within vco_div2: 0.10 ns, derived here, in place of the
# flow's generic 0.25 ns (CLOCK_UNCERTAINTY_CONSTRAINT, which flow.sdc sets on
# [all_clocks] after this file; an inter-clock uncertainty takes precedence
# over it). The only path captured by vco_div2 is the first stage's own
# toggle loop: it launches and captures on the same CLK pin one vco_div2
# period apart. STA reports its launch as clock pre_q0 (the flop's Q is that
# generated clock's source pin, and its source latency runs through the same
# port and CLK pin), so the uncertainty is set from both. Then
#   skew: 0. One pin; CRPR removes the common path, and OCV on the data
#      path is the flow's 5% timing derate, kept.
#   loop-filter ripple, Kvco and supply: 0 here. The period is the ceiling's
#      own: vctrl held at the rail (it cannot rise above it) at ss_pff, the
#      -10% supply corner, the fastest the ring runs on ss.
#   random period jitter: the analog spec's written estimate ("Period
#      jitter", analog/log/scratch/jitter/RESULT.md) is 2.5 ps rms per VCO
#      period at ss, 125 C (worst seed 4.2 ps by plain std). x1.41 for the
#      starve devices' noise it leaves out, x2 for flicker and supply noise
#      it leaves out: about 12 ps rms per VCO period. A vco_div2 period is
#      two VCO periods, so x1.41 (uncorrelated) to x2 (fully correlated):
#      24 ps rms at worst; 7 sigma (one period in 1e12) is 0.17 ns. The TSPC
#      stage's own jitter is a few ps against that.
# Rounded up to 0.20 ns, still under the flow's 0.25. Hold and every other
# clock keep the flow's 0.25 ns.
set_clock_uncertainty -setup 0.20 \
    -from [get_clocks {vco_div2 pre_q0}] -to [get_clocks vco_div2]

# clk and the VCO-derived clocks are unrelated: the PFD reset AND, the lock
# detector's sample of pfd_dn and every rst_n recovery path cross them on
# purpose (REQ-PFD-*, REQ-LOCK-*).
set_clock_groups -asynchronous \
    -group [get_clocks clk] \
    -group [get_clocks {vco_div2 pre_q0 clk_pre}]
