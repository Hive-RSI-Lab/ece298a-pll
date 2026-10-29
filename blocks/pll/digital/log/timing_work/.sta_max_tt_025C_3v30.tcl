read_liberty /opt/eda-toolchain/iic-osic-tools-2026.09/foss/pdks/gf180mcuD/libs.ref/gf180mcu_fd_sc_mcu7t5v0/lib/gf180mcu_fd_sc_mcu7t5v0__tt_025C_3v30.lib
read_verilog /work/blocks/pll/digital/harden/runs/run/final/nl/tt_um_ihsan_sa_pll.nl.v
link_design tt_um_ihsan_sa_pll
read_sdc /work/blocks/pll/digital/harden/runs/run/final/sdc/tt_um_ihsan_sa_pll.sdc
read_spef /work/blocks/pll/digital/harden/runs/run/final/spef/max/tt_um_ihsan_sa_pll.max.spef
report_worst_slack -max
report_worst_slack -min
report_check_types -max_slew -max_capacitance -max_fanout -violators
puts "chipflow_violation_counts slew [sta::max_slew_violation_count] cap [sta::max_capacitance_violation_count] fanout [sta::max_fanout_violation_count]"
exit
