#!/usr/bin/env python
"""cosim_pump.py - the gate-level closed loop with a mismatched charge pump.

    $CHIP_FLOW_HOME/bin/eda python blocks/pll/tb/cosim_pump.py [--calibrate] [--jobs N]

analog/mc/README.md finds UP/DN mismatch over its 10 % bound in 26 % of samples
at ff_pss and 6 % at ff_m40c_vp10. That bound is a DC proxy. This bench asks what
the loop does with such a pump: cosim_gl.py's run (extracted cell, gate-level
digital + SDF, 0.25 ns sync) with one pump side's current source widened in a copy of the
extracted netlist. The skew is about +3 sigma of each corner's Monte Carlo, on
each side in turn. It is a deterministic stand-in for a bad sample, not a draw:
only the two output devices change, not the mirrors' or switches' own mismatch.

--calibrate runs the DC mismatch sweep of tb/pll_analog_cp_tb.cir on each cell
(no closed loop), so the skew actually applied is measured. Writes
reports/recorded/cosim_pump.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cosim_corners as CC  # noqa: E402
import cosim_gl as GL  # noqa: E402
import pll_tb_common as C  # noqa: E402

# case -> (corner, side widened, percent). Skew: 3 sigma of mc_mm_<corner>.json
# (1.92 and 1.63 % of Icp), rounded. ff_pss has its unskewed run on record in
# cosim_corners_gl.json; ff_m40c_vp10 does not, so it gets a baseline.
CASES = {
    "ff_pss_up6": ("ff_pss", "up", 6.0),
    "ff_pss_dn6": ("ff_pss", "dn", 6.0),
    "ff_m40c_vp10_base": ("ff_m40c_vp10", None, 0.0),
    "ff_m40c_vp10_up5": ("ff_m40c_vp10", "up", 5.0),
    "ff_m40c_vp10_dn5": ("ff_m40c_vp10", "dn", 5.0),
}
# The pump's output current sources in the extracted cell: drain on the side's
# source node, gate on its mirror (netlist XMP_UPS, XMN_DNS; two fingers each).
SOURCE = {"up": ("up_s", "vcp_p"), "dn": ("dn_s", "vcp_n")}


def with_pump_skew(extracted: Path, side: str, pct: float, work: Path) -> Path:
    """A copy of the extracted cell with this side's current source pct % wider."""
    d, g = SOURCE[side]
    k = 1 + pct / 100
    pat = re.compile(rf"^X\d+ {d}\.t\d+ {g}\.t\d+ .*$", re.M)

    def widen(m: re.Match) -> str:
        return re.sub(r"\b(w|ad|as)=([0-9.]+)([a-z]*)",
                      lambda p: f"{p[1]}={float(p[2]) * k:.6g}{p[3]}", m[0])
    text, n = pat.subn(widen, extracted.read_text())
    if n != 2:
        raise SystemExit(f"cosim_pump: {side} source: {n} fingers matched, expected 2")
    out = work / f"{extracted.stem}.{side}{pct:g}.spice"
    out.write_text(text)
    return out


def cell_for(name: str, root: Path) -> Path:
    _, side, pct = CASES[name]
    return with_pump_skew(CC.EXTRACTED, side, pct, root) if side else CC.EXTRACTED


def calibrate(name: str, root: Path) -> dict:
    """pll_analog_cp_tb's sweep at this case's corner on this case's cell."""
    corner = CASES[name][0]
    deck = (C.WS / "analog" / "log" / "sim" / f"pll_analog_cp_tb__{corner}.cir").read_text()
    deck, n = re.subn(r"^\.include '[^']*pll_analog[^']*'$", f".include '{cell_for(name, root)}'", deck, flags=re.M)
    if n != 1:
        raise SystemExit(f"cosim_pump: {n} netlist includes in the {corner} deck")
    work = root / name
    work.mkdir(parents=True, exist_ok=True)
    (work / "cp.cir").write_text(deck)
    out = subprocess.run([*C.ngspice_cmd(), "cp.cir"], cwd=work, capture_output=True, text=True, timeout=1800).stdout
    (work / "cp.log").write_text(out)
    return {m[0]: float(m[1]) for m in re.findall(r"^(icp_up_code00_ua|icp_dn_code00_ua|cp_updn_mismatch_pct) = (\S+)", out, re.M)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--jobs", type=int, default=5)
    ap.add_argument("--timeout-s", type=float, default=30000.0)
    ap.add_argument("--cases", nargs="*", default=list(CASES))
    ap.add_argument("--calibrate", action="store_true", help="only the DC sweep on each cell; print and exit")
    a = ap.parse_args()
    root = C.WS / "log" / "cosim_pump"
    root.mkdir(parents=True, exist_ok=True)
    if a.calibrate:
        for n in a.cases:
            print(n, calibrate(n, root), flush=True)
        return 0
    inputs = GL.input_hashes()
    inputs["tb/cosim_pump.py"] = "sha256:" + hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

    def one(name: str) -> dict:
        corner, side, pct = CASES[name]
        work = root / name
        work.mkdir(parents=True, exist_ok=True)
        res = work / "result.json"
        res.unlink(missing_ok=True)
        dc = calibrate(name, root)
        cmd = [sys.executable, str(HERE / "cosim_gl.py"), "--one", corner, "--work", str(work),
               "--extracted-cell", str(cell_for(name, root)), "--timeout-s", str(a.timeout_s), "--out", str(res)]
        with (work / "run.log").open("w") as f:
            subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
        try:
            r = json.loads(res.read_text())
        except (OSError, ValueError):
            r = {"corner": corner, "status": "fail", "why": ["no result"], "measures": None}
        r.update(case=name, side=side, width_pct=pct, dc=dc, sdf=GL.sdf_corner_for(corner))
        m = r.get("measures") or {}
        print(name, r["status"], dc, m.get("lock_time_us"), m.get("vctrl_pp_last_10us_mv"), r.get("why"), flush=True)
        return r

    with ThreadPoolExecutor(a.jobs) as pool:
        results = list(pool.map(one, a.cases))
    out = C.WS / "reports" / "recorded" / "cosim_pump.json"
    out.write_text(json.dumps({"script": "cosim_pump", "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                               "facts": {"results": results}, "inputs": inputs}, indent=1, default=str) + "\n")
    print("cosim_pump: done ->", out, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
