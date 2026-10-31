#!/bin/bash
# Run the paper's post-layout VCO decks (make_decks.py first). ~10-20 min.
set -u
cd "$(dirname "$0")/run"
. ~/modules/bin/eda-env
export PDK=gf180mcuD
for f in *.cir; do
  ngspice -b "$f" > "${f%.cir}.log" 2>&1 &
done
wait
grep -h "^PT" vco_*.log | head -3
# collect "PT <vctrl> <f>" lines into ../data/vco_<corner>.txt
for f in vco_*.log; do grep "^PT" "$f" | awk '{print $2, $3}' > "../../data/${f%.log}.txt"; done
cp wave_tt_27c.txt ../../data/
