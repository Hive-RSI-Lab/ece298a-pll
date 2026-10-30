set circuit1 [readnet spice /work/blocks/pll/log/top_lvs/tt_um_ihsan_sa_pll.extracted.spice]
set circuit2 [readnet verilog /dev/null]
readnet spice /opt/eda-toolchain/iic-osic-tools-2026.09/foss/pdks/gf180mcuD/libs.ref/gf180mcu_fd_sc_mcu7t5v0/spice/gf180mcu_fd_sc_mcu7t5v0.spice $circuit2
readnet spice /opt/eda-toolchain/iic-osic-tools-2026.09/foss/pdks/gf180mcuD/libs.ref/gf180mcu_fd_io/spice/gf180mcu_fd_io.spice $circuit2
readnet spice /opt/eda-toolchain/iic-osic-tools-2026.09/foss/pdks/gf180mcuD/libs.ref/gf180mcu_fd_io/spice/gf180mcu_ef_io.spice $circuit2
readnet spice /work/blocks/pll/top/macros/pll_analog.spice $circuit2
readnet verilog /work/blocks/pll/top/harden/runs/run/final/pnl/tt_um_ihsan_sa_pll.pnl.v $circuit2
lvs "$circuit1 tt_um_ihsan_sa_pll" "$circuit2 tt_um_ihsan_sa_pll" /opt/eda-toolchain/iic-osic-tools-2026.09/foss/pdks/gf180mcuD/libs.tech/netgen/gf180mcuD_setup.tcl /work/blocks/pll/log/top_lvs/top_lvs.rpt -json
