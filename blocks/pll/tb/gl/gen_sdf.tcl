# gen_sdf.tcl - an SDF for the hardened netlist at a liberty corner LibreLane
# did not write (it writes nom_{ff_n40C_3v60,ss_125C_3v00,tt_025C_3v30}).
# Same inputs as LibreLane's own write: the final netlist, its SDC and the
# nom SPEF. Checked: run at ff_n40C_3v60 it reproduces LibreLane's
# nom_ff_n40C_3v60 SDF to the ps, bar 16 tie-cell interconnects (0.001 vs
# 0.000 ns) and one setup check (0.094 vs 0.093 ns), OpenSTA 3.1.0 vs 2.7.0.
#   LIB=<liberty> OUT=<sdf> chip-flow eda sta -no_init -exit gen_sdf.tcl  (run from tb/gl)
read_liberty $::env(LIB)
read_verilog tt_um_ihsan_sa_pll.nl.v
link_design tt_um_ihsan_sa_pll
read_spef tt_um_ihsan_sa_pll.nom.spef
read_sdc tt_um_ihsan_sa_pll.sdc
write_sdf -include_typ -divider . $::env(OUT)
