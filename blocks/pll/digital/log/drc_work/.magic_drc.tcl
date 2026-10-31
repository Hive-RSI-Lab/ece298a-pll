gds maskhints yes
gds read /home/hive2/projects/ece298a-pll-digital/blocks/pll/digital/harden/runs/run/final/gds/tt_um_ihsan_sa_pll.gds
load tt_um_ihsan_sa_pll
select top cell
expand
drc euclidean on
drc style drc(full)
drc check
set drc_result [drc listall why]
set count 0
foreach {errtype coordlist} $drc_result {
  foreach coord $coordlist { incr count }
}
set fout [open /home/hive2/projects/ece298a-pll-digital/blocks/pll/digital/log/drc_work/.magic_drc.rpt w]
puts $fout "\[INFO\]: COUNT: $count"
close $fout
puts stdout "\[INFO\]: COUNT: $count"
flush stdout
quit -noprompt
