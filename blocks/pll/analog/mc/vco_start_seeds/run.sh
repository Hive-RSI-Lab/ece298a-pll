#!/bin/bash
. ~/modules/bin/eda-env; export PDK=gf180mcuD
cd /tmp/a06c8-mc
for f in mc1_base mc1_big mc1_en mc13_base mc13_big mc13_en mc2_base mc2_en; do
  heavy --first /usr/bin/timeout 1200 ngspice -b $f.cir > $f.log 2>&1
done
echo done > ALLDONE
