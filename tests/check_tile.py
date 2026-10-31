#!/usr/bin/env python3
"""Fail when the tile's recorded harden has gone stale, or gds/ isn't what it built.

    python3 tests/check_tile.py

The tile is hardened by chip-flow's top_harden (10+ minutes), then checked by
top_drc, top_lvs and precheck; the passes are committed in
blocks/pll/state.json and blocks/pll/reports/recorded/. A change to anything
top_harden reads (the digital RTL, the analog layout, the SDCs) leaves those
passes, and the committed gds/ and lef/, describing a tile that no longer
matches the sources. This check catches that without any EDA tool:

1. top_harden, top_drc, top_lvs and precheck each last passed, in state.json
   and in their recorded report;
2. every input top_harden recorded hashes as it does now (the same hashes
   chip-flow's statelib takes: dir_text for a directory, text_eol for a file);
3. top_drc, top_lvs and precheck ran after that top_harden, so they judged what
   it built, and their own other inputs hash as they did;
4. gds/<top>.gds hashes as the GDS those three judged (top_gds), so the GDS
   Tiny Tapeout takes is the checked one.

It needs only python3 and PyYAML, as the rest of tests/check.sh does, so CI runs it.
When CHIP_FLOW_HOME points at chip-flow, it also compares its hashes with
statelib's own, so the two can't drift apart unnoticed.
Fix a failure by re-running the four gates (chip-flow gate --gate <g> --skill
msde --workspace blocks/pll), then python3 blocks/pll/tt/assemble.py, and
committing the result.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
WS = ROOT / "blocks" / "pll"
TOP = "tt_um_ihsan_sa_pll"
GATES = ("top_harden", "top_drc", "top_lvs", "precheck")
# chip-flow's invalidation.yaml artifact kinds the four gates read, workspace-relative
KINDS = {
    "digital_rtl": ("digital/rtl", "dir_text"),
    "analog_layout": ("analog/layout", "dir_text"),
    "top_sdc": ("top.sdc", "text_eol"),
    "digital_sdc": ("digital/harden/constraints.sdc", "text_eol"),
    "interface": ("interface.yaml", "json_canonical"),
}


def _text(data: bytes) -> str:
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1")


def _eol(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n")


def dir_text(files: list[tuple[str, Path]]) -> str:
    """statelib._norm_dir_text over (relative name, file) pairs."""
    parts = [rel.encode() + b"\0" + _eol(_text(f.read_bytes())).encode() + b"\0"
             for rel, f in sorted(files)]
    return "dir_text:" + hashlib.sha256(b"dir\0" + b"".join(parts)).hexdigest()


def hash_kind(kind: str) -> str | None:
    rel, norm = KINDS[kind]
    p = WS / rel
    if not p.exists():
        return None
    if norm == "dir_text":
        return dir_text([(f.relative_to(p).as_posix(), f) for f in p.rglob("*")
                         if f.is_file() and "__pycache__" not in f.parts
                         and f.suffix not in (".pyc", ".pyo")])
    if norm == "text_eol":
        return "text_eol:" + hashlib.sha256(_eol(_text(p.read_bytes())).encode()).hexdigest()
    doc = yaml.safe_load(_text(p.read_bytes()))  # json_canonical
    return "json_canonical:" + hashlib.sha256(json.dumps(
        doc, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode()).hexdigest()


def main() -> int:
    st = json.loads((WS / "state.json").read_text())
    gates = st.get("gates") or {}
    bad: list[str] = []
    harden_ts = ""
    gds_hash = dir_text([(f"{TOP}.gds", ROOT / "gds" / f"{TOP}.gds")]) \
        if (ROOT / "gds" / f"{TOP}.gds").is_file() else None
    for g in GATES:
        last = (gates.get(g) or {}).get("last") or {}
        try:
            rep = json.loads((WS / "reports" / "recorded" / f"gate-{g}.json").read_text())
        except (OSError, ValueError):
            rep = {}
        if (gates.get(g) or {}).get("status") != "pass" or rep.get("status") != "pass":
            bad.append(f"{g}: its last recorded run did not pass")
            continue
        if (gates.get(g) or {}).get("stale"):
            bad.append(f"{g}: state.json marks it stale")
        if g == "top_harden":
            harden_ts = str(last.get("ts") or "")
        elif str(last.get("ts") or "") < harden_ts:
            bad.append(f"{g}: recorded before top_harden's last run, so it judged an older GDS")
        for kind, want in (last.get("inputs") or {}).items():
            if kind == "top_gds":
                if want != gds_hash:
                    bad.append(f"{g}: gds/{TOP}.gds is not the GDS it checked "
                               "(run blocks/pll/tt/assemble.py after the harden)")
                continue
            if kind not in KINDS:
                bad.append(f"{g}: input {kind} is not one this check knows how to hash")
                continue
            if hash_kind(kind) != want:
                bad.append(f"{g}: {KINDS[kind][0]} changed since it passed")

    cfh = os.environ.get("CHIP_FLOW_HOME")
    if cfh and (Path(cfh) / "engine" / "lib" / "statelib.py").is_file():
        sys.path.insert(0, str(Path(cfh) / "engine" / "lib"))
        import statelib  # noqa: E402

        imap = statelib.load_map()
        for kind, (rel, norm) in KINDS.items():
            spec = imap["artifact_kinds"].get(kind) or {}
            if (spec.get("path"), spec.get("norm")) != (rel, norm):
                bad.append(f"chip-flow's {kind} is {spec}, this check's is {rel} {norm}: update KINDS")
            elif statelib.hash_artifact(WS / rel, norm) != hash_kind(kind):
                bad.append(f"{kind}: this check's hash differs from chip-flow statelib's")
        for g in GATES:
            cur = statelib.gate_input_hashes(WS, "msde", g, imap, st.get("artifacts"))
            rec = ((gates.get(g) or {}).get("last") or {}).get("inputs") or {}
            for kind in cur:
                if kind != "top_gds" and cur[kind] != rec.get(kind):
                    bad.append(f"{g}: {kind} changed since it passed (statelib)")

    if bad:
        print("tile: the recorded harden is stale or gds/ doesn't match it:")
        for b in dict.fromkeys(bad):
            print("  - " + b)
        print("re-run top_harden, top_drc, top_lvs and precheck (chip-flow gate --gate <g> "
              "--skill msde --workspace blocks/pll), then python3 blocks/pll/tt/assemble.py, "
              "and commit the result")
        return 1
    print(f"tile: ok (top_harden {harden_ts} is fresh; top_drc, top_lvs, precheck checked "
          f"the committed gds/{TOP}.gds)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
