#!/usr/bin/env python3
"""Lint the analog netlists, testbenches, bounds and spec files under blocks/.

Run from the repository root (tests/check.sh does). It needs only python3 and
PyYAML: no PDK and no simulator, so it catches what a hand edit most often
breaks before the full SPICE gates run.

For each block's analog/ folder it checks that:
  - every .subckt has a matching .ends;
  - every X instance names a subcircuit defined in that block's netlist, or a
    GF180 device or standard cell, and an instance of a block subcircuit has
    exactly as many nodes as the subcircuit has ports;
  - a testbench pairs .control with .endc and ends with .end;
  - every bound in tb/<bench>.bounds.json names a measure, has a min or a max
    with min <= max, and its measure is printed by tb/<bench>.cir.
It also checks that every .yaml and .json under blocks/ parses, outside the
logs, run directories and snapshots the flow writes.

Prints one line and exits 0 when all is sound; prints each problem and exits 1.
"""
import json
import re
import sys
from pathlib import Path

import yaml

# Names the GF180 PDK and its standard-cell library define, which a netlist
# may instantiate without defining them itself.
PDK_NAMES = re.compile(
    r"^(?:[np]fet_(?:03v3|06v0)(?:_\w+)?"
    r"|[np]polyf_[us](?:_\w+)?|[np]plus_[us](?:_\w+)?"
    r"|cap_mim_\w+|cap_[np]mos_\w+|diode_\w+|rm[123]|tm\w+"
    r"|gf180mcu_fd_sc_mcu[79]t5v0__\w+)$"
)
SKIP_DIRS = {"log", "runs", "state_snapshots", "__pycache__"}


def cards(path):
    """The netlist's cards as (line number, text), continuations joined."""
    out = []
    for no, raw in enumerate(path.read_text().splitlines(), 1):
        line = raw.split(";")[0].rstrip()
        if not line.strip() or line.lstrip().startswith("*"):
            continue
        if line.lstrip().startswith("+") and out:
            out[-1] = (out[-1][0], out[-1][1] + " " + line.lstrip()[1:])
        else:
            out.append((no, line.strip()))
    return out


def subckts(path, problems):
    """Port lists of the subcircuits a file defines, checking .subckt/.ends pairs."""
    defined, open_name, open_no = {}, None, 0
    for no, card in cards(path):
        words = card.split()
        head = words[0].lower()
        if head == ".subckt":
            if open_name:
                problems.append(f"{path}:{no}: .subckt {words[1]} opens inside {open_name}, whose .ends is missing")
            open_name, open_no = words[1], no
            defined[words[1]] = [w for w in words[2:] if "=" not in w and w.lower() != "params:"]
        elif head == ".ends":
            if not open_name:
                problems.append(f"{path}:{no}: .ends with no .subckt open")
            elif len(words) > 1 and words[1] != open_name:
                problems.append(f"{path}:{no}: .ends {words[1]} closes .subckt {open_name}")
            open_name = None
    if open_name:
        problems.append(f"{path}:{open_no}: .subckt {open_name} has no .ends")
    return defined


def instances(path, known, problems):
    """Check every X instance in a file against the subcircuits it can reach."""
    for no, card in cards(path):
        words = card.split()
        if not words[0][:1] in "xX":
            continue
        positional = [w for w in words[1:] if "=" not in w]
        if not positional:
            problems.append(f"{path}:{no}: {words[0]} names no subcircuit")
            continue
        name, nodes = positional[-1], positional[:-1]
        if name in known:
            if len(nodes) != len(known[name]):
                problems.append(
                    f"{path}:{no}: {words[0]} connects {len(nodes)} nodes to {name}, which has {len(known[name])} ports"
                )
        elif "{{" not in name and not PDK_NAMES.match(name):
            problems.append(f"{path}:{no}: {words[0]} instantiates {name}, which no netlist here defines and the PDK does not name")


def bounds(bench, problems):
    path = bench.with_suffix(".bounds.json")
    if not path.is_file():
        return 0
    try:
        rows = json.loads(path.read_text())
    except ValueError as err:
        problems.append(f"{path}: not valid JSON ({err})")
        return 0
    text = bench.read_text()
    if not isinstance(rows, list):
        problems.append(f"{path}: holds a {type(rows).__name__}, not a list of bounds")
        return 0
    for i, row in enumerate(rows):
        measure = row.get("measure") if isinstance(row, dict) else None
        if not measure:
            problems.append(f"{path}: bound {i} names no measure")
            continue
        lo, hi = row.get("min"), row.get("max")
        if lo is None and hi is None:
            problems.append(f"{path}: {measure} has neither a min nor a max")
        elif lo is not None and hi is not None and lo > hi:
            problems.append(f"{path}: {measure} has min {lo} above max {hi}")
        if not re.search(rf"\b{re.escape(measure)}\b", text):
            problems.append(f"{path}: {measure} is never printed by {bench.name}")
    return len(rows)


def main() -> int:
    problems = []
    nets = benches = nbounds = 0
    for analog in sorted(Path("blocks").glob("*/analog")):
        known = {}
        for net in sorted((analog / "netlist").glob("*.cir")):
            known.update(subckts(net, problems))
            nets += 1
        for net in sorted((analog / "netlist").glob("*.cir")):
            instances(net, known, problems)
        for bench in sorted((analog / "tb").glob("*.cir")):
            benches += 1
            subckts(bench, problems)
            instances(bench, known, problems)
            heads = [c.split()[0].lower() for _, c in cards(bench)]
            if heads.count(".control") != heads.count(".endc"):
                problems.append(f"{bench}: {heads.count('.control')} .control but {heads.count('.endc')} .endc")
            if not heads or heads[-1] != ".end":
                problems.append(f"{bench}: does not end with .end")
            nbounds += bounds(bench, problems)
    if not nets:
        problems.append("no analog netlist found under blocks/*/analog/netlist")

    parsed = 0
    for path in sorted(Path("blocks").rglob("*")):
        if path.suffix not in (".yaml", ".yml", ".json") or SKIP_DIRS & set(path.parts):
            continue
        try:
            (json.loads if path.suffix == ".json" else yaml.safe_load)(path.read_text())
            parsed += 1
        except (ValueError, yaml.YAMLError) as err:
            problems.append(f"{path}: does not parse ({str(err).splitlines()[0]})")

    if problems:
        for p in problems:
            print(f"netlists: {p}")
        return 1
    print(f"netlists: ok ({nets} netlist(s), {benches} testbench(es), {nbounds} bound(s), {parsed} spec file(s) parsed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
