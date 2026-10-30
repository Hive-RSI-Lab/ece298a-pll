#!/usr/bin/env python3
"""Put the PLL into Tiny Tapeout's analog-project shape, or check it is.

    python3 blocks/pll/tt/assemble.py            # write it
    python3 blocks/pll/tt/assemble.py --check    # exit 1 if anything differs

The tile is hardened by chip-flow's top_harden into
blocks/pll/top/harden/runs/run/final (out of git). Tiny Tapeout's analog flow
(ttgf-analog-template) takes a committed GDS and LEF instead of hardening
itself, so this copies:

- the tile's GDS and LEF to gds/ and lef/ (only when a harden has run);
- src/: project.v and pll_analog.v from blocks/pll/tt/src, and the digital
  core's RTL from blocks/pll/digital/rtl, so src/ never drifts from the
  RTL the harden used;
- test/: the RTL test of the top with the analog macro's behavioural model;
- info.yaml and .github/workflows/gds.yaml from blocks/pll/tt.

It also removes what only the digital template uses (src/config.json and the
fpga workflow, which can't build a design with an analog macro).
--check compares instead of writing, and leaves gds/ and lef/ out unless
--with-gds is given, since a check can't harden.
"""
from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TT = ROOT / "blocks" / "pll" / "tt"
RTL = ROOT / "blocks" / "pll" / "digital" / "rtl"
FINAL = ROOT / "blocks" / "pll" / "top" / "harden" / "runs" / "run" / "final"
TOP = "tt_um_ihsan_sa_pll"


def plan(with_gds: bool) -> tuple[list[tuple[Path, Path]], list[Path]]:
    copies = [(p, ROOT / "src" / p.name) for p in sorted((TT / "src").glob("*.v"))]
    copies += [(p, ROOT / "src" / p.name) for p in sorted(RTL.glob("*.v"))]
    copies += [(p, ROOT / "test" / p.name) for p in sorted((TT / "test").iterdir())
               if p.is_file()]
    copies += [(TT / "info.yaml", ROOT / "info.yaml"),
               (TT / "workflows" / "gds.yaml", ROOT / ".github" / "workflows" / "gds.yaml")]
    if with_gds:
        copies += [(FINAL / "gds" / f"{TOP}.gds", ROOT / "gds" / f"{TOP}.gds"),
                   (FINAL / "lef" / f"{TOP}.lef", ROOT / "lef" / f"{TOP}.lef")]
    gone = [ROOT / "src" / "config.json", ROOT / ".github" / "workflows" / "fpga.yaml"]
    return copies, gone


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="compare, don't write")
    ap.add_argument("--with-gds", action="store_true",
                    help="with --check: also compare gds/ and lef/ with the harden's")
    args = ap.parse_args()
    with_gds = args.with_gds or (not args.check and FINAL.is_dir())
    copies, gone = plan(with_gds)
    missing = [str(src.relative_to(ROOT)) for src, _ in copies if not src.is_file()]
    if missing:
        print("assemble: missing " + ", ".join(missing), file=sys.stderr)
        return 2
    if args.check:
        bad = [str(dst.relative_to(ROOT)) for src, dst in copies
               if not dst.is_file() or not filecmp.cmp(src, dst, shallow=False)]
        bad += [f"{p.relative_to(ROOT)} (should be gone)" for p in gone if p.exists()]
        if bad:
            print("assemble: differs from blocks/pll/tt/assemble.py's output: " + ", ".join(bad))
            print("assemble: run python3 blocks/pll/tt/assemble.py")
            return 1
        print(f"assemble: ok ({len(copies)} files in the analog-project shape)")
        return 0
    for src, dst in copies:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    for p in gone:
        p.unlink(missing_ok=True)
    print(f"assemble: wrote {len(copies)} files" + ("" if with_gds else
          " (no harden yet, so no gds/ or lef/)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
