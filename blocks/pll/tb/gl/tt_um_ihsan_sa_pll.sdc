###############################################################################
# Created by write_sdc
###############################################################################
current_design tt_um_ihsan_sa_pll
###############################################################################
# Timing Constraints
###############################################################################
create_clock -name clk -period 80.0000 [get_ports {clk}]
set_clock_transition 0.1500 [get_clocks {clk}]
set_clock_uncertainty 0.2500 clk
set_propagated_clock [get_clocks {clk}]
create_clock -name vco_div2 -period 5.4000 [get_ports {ui_in[3]}]
set_clock_transition 0.1500 [get_clocks {vco_div2}]
set_clock_uncertainty 0.2500 vco_div2
set_propagated_clock [get_clocks {vco_div2}]
create_generated_clock -name pre_q0 -source [get_ports {ui_in[3]}] -divide_by 2 [get_pins {_171_/Q}]
set_clock_transition 0.1500 [get_clocks {pre_q0}]
set_clock_uncertainty 0.2500 pre_q0
set_propagated_clock [get_clocks {pre_q0}]
create_generated_clock -name clk_pre -source [get_pins {_171_/Q}] -divide_by 2 [get_pins {_172_/Q}]
set_clock_transition 0.1500 [get_clocks {clk_pre}]
set_clock_uncertainty 0.2500 clk_pre
set_propagated_clock [get_clocks {clk_pre}]
set_clock_uncertainty -rise_from [get_clocks {vco_div2}] -rise_to [get_clocks {vco_div2}]  -setup 0.2000
set_clock_uncertainty -rise_from [get_clocks {vco_div2}] -fall_to [get_clocks {vco_div2}]  -setup 0.2000
set_clock_uncertainty -fall_from [get_clocks {vco_div2}] -rise_to [get_clocks {vco_div2}]  -setup 0.2000
set_clock_uncertainty -fall_from [get_clocks {vco_div2}] -fall_to [get_clocks {vco_div2}]  -setup 0.2000
set_clock_uncertainty -rise_from [get_clocks {pre_q0}] -rise_to [get_clocks {vco_div2}]  -setup 0.2000
set_clock_uncertainty -rise_from [get_clocks {pre_q0}] -fall_to [get_clocks {vco_div2}]  -setup 0.2000
set_clock_uncertainty -fall_from [get_clocks {pre_q0}] -rise_to [get_clocks {vco_div2}]  -setup 0.2000
set_clock_uncertainty -fall_from [get_clocks {pre_q0}] -fall_to [get_clocks {vco_div2}]  -setup 0.2000
set_clock_groups -name group1 -asynchronous \
 -group [get_clocks {clk}]\
 -group [list [get_clocks {clk_pre}]\
           [get_clocks {pre_q0}]\
           [get_clocks {vco_div2}]]
set_input_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {ena}]
set_input_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {rst_n}]
set_input_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {ui_in[0]}]
set_input_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {ui_in[1]}]
set_input_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {ui_in[2]}]
set_input_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {ui_in[3]}]
set_input_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {ui_in[4]}]
set_input_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {ui_in[5]}]
set_input_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {ui_in[6]}]
set_input_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {ui_in[7]}]
set_input_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_in[0]}]
set_input_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_in[1]}]
set_input_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_in[2]}]
set_input_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_in[3]}]
set_input_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_in[4]}]
set_input_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_in[5]}]
set_input_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_in[6]}]
set_input_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_in[7]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_oe[0]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_oe[1]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_oe[2]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_oe[3]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_oe[4]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_oe[5]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_oe[6]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_oe[7]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_out[0]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_out[1]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_out[2]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_out[3]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_out[4]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_out[5]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_out[6]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uio_out[7]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uo_out[0]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uo_out[1]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uo_out[2]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uo_out[3]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uo_out[4]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uo_out[5]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uo_out[6]}]
set_output_delay 16.0000 -clock [get_clocks {clk}] -add_delay [get_ports {uo_out[7]}]
###############################################################################
# Environment
###############################################################################
set_load -pin_load 0.0729 [get_ports {uio_oe[7]}]
set_load -pin_load 0.0729 [get_ports {uio_oe[6]}]
set_load -pin_load 0.0729 [get_ports {uio_oe[5]}]
set_load -pin_load 0.0729 [get_ports {uio_oe[4]}]
set_load -pin_load 0.0729 [get_ports {uio_oe[3]}]
set_load -pin_load 0.0729 [get_ports {uio_oe[2]}]
set_load -pin_load 0.0729 [get_ports {uio_oe[1]}]
set_load -pin_load 0.0729 [get_ports {uio_oe[0]}]
set_load -pin_load 0.0729 [get_ports {uio_out[7]}]
set_load -pin_load 0.0729 [get_ports {uio_out[6]}]
set_load -pin_load 0.0729 [get_ports {uio_out[5]}]
set_load -pin_load 0.0729 [get_ports {uio_out[4]}]
set_load -pin_load 0.0729 [get_ports {uio_out[3]}]
set_load -pin_load 0.0729 [get_ports {uio_out[2]}]
set_load -pin_load 0.0729 [get_ports {uio_out[1]}]
set_load -pin_load 0.0729 [get_ports {uio_out[0]}]
set_load -pin_load 0.0729 [get_ports {uo_out[7]}]
set_load -pin_load 0.0729 [get_ports {uo_out[6]}]
set_load -pin_load 0.0729 [get_ports {uo_out[5]}]
set_load -pin_load 0.0729 [get_ports {uo_out[4]}]
set_load -pin_load 0.0729 [get_ports {uo_out[3]}]
set_load -pin_load 0.0729 [get_ports {uo_out[2]}]
set_load -pin_load 0.0729 [get_ports {uo_out[1]}]
set_load -pin_load 0.0729 [get_ports {uo_out[0]}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_4 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {clk}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {ena}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {rst_n}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {ui_in[7]}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {ui_in[6]}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {ui_in[5]}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {ui_in[4]}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {ui_in[3]}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {ui_in[2]}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {ui_in[1]}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {ui_in[0]}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {uio_in[7]}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {uio_in[6]}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {uio_in[5]}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {uio_in[4]}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {uio_in[3]}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {uio_in[2]}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {uio_in[1]}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {uio_in[0]}]
set_timing_derate -early 0.9500
set_timing_derate -late 1.0500
###############################################################################
# Design Rules
###############################################################################
set_max_transition 3.0000 [current_design]
set_max_capacitance 0.2000 [current_design]
set_max_fanout 10.0000 [current_design]
