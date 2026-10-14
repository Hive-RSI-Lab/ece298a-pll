#!/usr/bin/env bash
# The fast check for this repo. GitHub runs it as the `check` job on every pull
# request and every push to main, and you can run the same thing locally:
#
#   bash tests/check.sh
#
# It needs python3 with PyYAML and Icarus Verilog (iverilog) on PATH. It runs:
#   1. tests/check_info.py: info.yaml has what the Tiny Tapeout flow reads, and
#      its source list matches src/, test/Makefile and test/tb.v.
#   2. tests/check_netlists.py: the analog netlist, testbenches, bounds and
#      spec files are well formed (no PDK or simulator needed).
#   3. blocks/pll/loop/linear_model.py: the s-domain model of the whole loop,
#      built from the sizing and the recorded PVT run, agrees with ngspice's
#      open-loop phase margin and meets the margin and settling targets.
#   4. A lint of the Verilog: the Tiny Tapeout wrapper in src/, and the PLL's
#      digital RTL with its hardening top, each compile under iverilog -Wall,
#      and any warning fails the check.
# Steps 1 to 3 need only python3, so they run (and report) before the check
# asks for iverilog; without it the run still stops with exit 2 at step 4.
# The SPICE corners, formal proof, hardening and the Tiny Tapeout workflows
# (gds, docs, test, fpga) still run on their own.
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd)
cd "$root"

need() {
  if ! command -v "$1" >/dev/null; then
    echo "check: $1 is not on PATH; see the top of tests/check.sh" >&2
    exit 2
  fi
}
need python3

echo "== 1/4 info.yaml"
python3 tests/check_info.py

echo "== 2/4 analog netlists and specs"
python3 tests/check_netlists.py

echo "== 3/4 linear loop model"
python3 blocks/pll/loop/linear_model.py

echo "== 4/4 lint (iverilog -Wall)"
need iverilog
lint() {
  local name=$1; shift
  local out
  out=$(iverilog -g2012 -Wall -t null "$@" 2>&1) || { echo "$out"; echo "lint: iverilog failed on $name"; exit 1; }
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
echo "check: ok"
