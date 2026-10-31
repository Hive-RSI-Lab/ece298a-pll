#!/usr/bin/env bash
# The fast check for this repo. GitHub runs it on every pull request and every
# push to main twice: as the `check` job with Ubuntu's iverilog, and as the
# `test (iic-osic-tools 2026.09)` job inside the IIC-OSIC-TOOLS image, with
# the same tools as the Hive's local run. You can run it locally too:
#
#   bash tests/check.sh
#
# It needs python3 with PyYAML, and Icarus Verilog: the iverilog on PATH when
# there is one (CI installs it), or else chip-flow's eda wrapper, which runs
# iverilog from the EDA toolchain ($CHIP_FLOW_HOME/bin/eda, then
# /opt/chip-flow/bin/eda), or else the toolchain's own iverilog under
# $EDA_TOOLCHAIN/foss/tools/iverilog/bin. It runs:
#   1. tests/check_info.py: info.yaml has what the Tiny Tapeout flow reads, and
#      its source list matches src/, test/Makefile and test/tb.v. In the
#      analog-project shape, blocks/pll/tt/assemble.py --check: src/ and test/
#      are its copies, src/ of the digital RTL.
#   2. A lint of the Verilog: the Tiny Tapeout wrapper in src/, and the PLL's
#      digital RTL with its hardening top, each compile under iverilog -Wall,
#      and any warning fails the check.
#   3. tests/check_netlists.py: the analog netlist, testbenches, bounds and
#      spec files are well formed (no PDK or simulator needed).
#   4. tests/check_tile.py: the tile's recorded harden (top_harden, top_drc,
#      top_lvs, precheck) still holds for the current RTL, analog layout and
#      SDCs, and gds/ is the GDS those gates checked. A change to what the
#      harden reads fails here until the tile is re-hardened and committed.
#   Then docs/review/stages.py --check says whether the review page's stage
#   table matches the recorded gate reports. A stale page is a note, not a
#   failure; a crash in the script fails the check.
# The SPICE corners, formal proof, hardening and the Tiny Tapeout workflows
# (gds, docs, test, fpga) still run on their own.
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd)
cd "$root"

if ! command -v python3 >/dev/null; then
  echo "check: python3 is not on PATH; see the top of tests/check.sh" >&2
  exit 2
fi
if command -v iverilog >/dev/null; then
  iverilog=(iverilog)
else
  iverilog=()
  for eda in ${CHIP_FLOW_HOME:+"$CHIP_FLOW_HOME/bin/eda"} /opt/chip-flow/bin/eda; do
    if [ -x "$eda" ]; then iverilog=("$eda" iverilog); break; fi
  done
  if [ ${#iverilog[@]} -eq 0 ] && [ -n "${EDA_TOOLCHAIN:-}" ] && [ -x "$EDA_TOOLCHAIN/foss/tools/iverilog/bin/iverilog" ]; then
    iverilog=("$EDA_TOOLCHAIN/foss/tools/iverilog/bin/iverilog")
  fi
  if [ ${#iverilog[@]} -eq 0 ]; then
    echo "check: iverilog is not on PATH, no chip-flow eda wrapper was found and \$EDA_TOOLCHAIN has none; see the top of tests/check.sh" >&2
    exit 2
  fi
  echo "check: no iverilog on PATH, so running it through ${iverilog[0]}"
fi

echo "== 1/4 info.yaml"
python3 tests/check_info.py
# in the analog-project shape, src/, test/, info.yaml and the gds workflow are
# blocks/pll/tt/assemble.py's copies, src/ of the digital RTL the harden used
if grep -q '^ *analog_pins:' info.yaml; then
  python3 blocks/pll/tt/assemble.py --check
fi

echo "== 2/4 lint (iverilog -Wall)"
lint() {
  local name=$1; shift
  local out
  out=$("${iverilog[@]}" -g2012 -Wall -t null "$@" 2>&1) || { echo "$out"; echo "lint: iverilog failed on $name"; exit 1; }
  if [ -n "$out" ]; then
    echo "$out"
    echo "lint: iverilog printed warnings on $name, and a warning fails the check"
    exit 1
  fi
  echo "lint: ok, $name"
}
mapfile -t sources < <(python3 -c 'import yaml; print("\n".join("src/" + f for f in yaml.safe_load(open("info.yaml"))["project"]["source_files"]))')
lint "src/" -I src "${sources[@]}"
shopt -s nullglob
rtl=(blocks/pll/digital/rtl/*.v)
if [ ${#rtl[@]} -eq 0 ]; then
  echo "lint: no RTL under blocks/pll/digital/rtl"
  exit 1
fi
lint "the PLL digital RTL" "${rtl[@]}" blocks/pll/digital/harden/tt_um_ihsan_sa_pll.v

echo "== 3/4 analog netlists and specs"
python3 tests/check_netlists.py

echo "== 4/4 the tile's recorded harden"
python3 tests/check_tile.py

rc=0
python3 docs/review/stages.py --check || rc=$?
if [ "$rc" -eq 3 ]; then
  echo "note: docs/review/stages.md is stale; run python3 docs/review/stages.py and commit it"
elif [ "$rc" -ne 0 ]; then
  echo "check: docs/review/stages.py failed (exit $rc)"
  exit 1
fi
echo "check: ok"
