#!/usr/bin/env bash
# The project's score: the share of the goals' checkable done-lines that pass,
# re-run from a scratch copy of blocks/pll (tests/score.py says what each
# line is). One number on the last line, 0..100, higher is better.
#
#   bash tests/score.sh
#
# It runs the gates through chip-flow and the IIC-OSIC-TOOLS tree:
# CHIP_FLOW_HOME, else the Hive's hive-chip-flow module, else /opt/chip-flow;
# EDA_TOOLCHAIN, else /opt/eda-toolchain/iic-osic-tools-2026.09. A stage
# whose tool is missing inside the tree fails its line. With no tree or no
# chip-flow at all nothing can be measured, so it exits 127 with the shell's
# own "not found" line, which the Hive reads as "can't run", not a score of 0.
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd)
cd "$root"

cfh=
for d in ${CHIP_FLOW_HOME:+"$CHIP_FLOW_HOME"} ${HIVE_MODULES:+"$HIVE_MODULES/hive-chip-flow"} \
	/hive/modules/hive-chip-flow /opt/chip-flow; do
	if [ -x "$d/bin/eda" ] && [ -d "$d/engine/scripts" ]; then cfh=$d; break; fi
done
if [ -z "$cfh" ]; then
	echo "score: no chip-flow (CHIP_FLOW_HOME, the hive-chip-flow module or /opt/chip-flow)" >&2
	sh -c chip-flow
	exit 127
fi
EDA_TOOLCHAIN=${EDA_TOOLCHAIN:-/opt/eda-toolchain/iic-osic-tools-2026.09}
if [ ! -d "$EDA_TOOLCHAIN" ]; then
	echo "score: no IIC-OSIC-TOOLS tree at $EDA_TOOLCHAIN" >&2
	sh -c iic-osic-tools
	exit 127
fi
export CHIP_FLOW_HOME=$cfh EDA_TOOLCHAIN
exec "$cfh/bin/eda" python tests/score.py "$@"
