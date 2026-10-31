#!/usr/bin/env python
"""cosim_gl.py - cosim_corners.py's bench with the hardened gate-level digital
in the loop (issue #47).

    $CHIP_FLOW_HOME/bin/eda python blocks/pll/tb/cosim_gl.py \
        [--corners NAME ...] [--jobs N] [--timeout-s S] [--out FILE]

Same bench (test_pll_cosim.py), operating point, bounds, extracted analog
cell, PDK corner and 0.25 ns sync as cosim_corners.py, with one change: the
digital half is not the RTL but the vde harden's gate-level netlist
(digital/harden/runs/run/final/nl/tt_um_ihsan_sa_pll.nl.v) with the PDK's
timing cell models and the harden's own SDF back-annotated, the corner's
process picked from the SDF corners LibreLane writes (nom_ff_n40C_3v60 for
ff, nom_ss_125C_3v00 for ss, nom_tt_025C_3v30 for tt). The netlist is wrapped
by chip-flow's glsim harness (ttlib.generate_glsim_harness: a module named
ihsan_sa_pll with the RTL's own ports around the tt_um_ wrapper), so
pll_cosim_top.v instantiates it unchanged. So the PFD's reset pulse, the
dividers' clock-to-q and the prescaler's toggle all carry their routed
delays, which the RTL's zero-delay SIM path leaves out.

The harden's runs/ is not in git: run the vde harden gate first
(chip-flow gate --gate harden --skill vde --workspace blocks/pll/digital).
Writes reports/recorded/cosim_corners_gl.json, shaped as cosim_corners.json,
with the netlist and SDF hashes added to its inputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cosim_corners as CC  # noqa: E402
import pll_tb_common as C  # noqa: E402

FINAL = C.WS / "digital" / "harden" / "runs" / "run" / "final"
TOP = "tt_um_ihsan_sa_pll"
OUT = C.WS / "reports" / "recorded" / "cosim_corners_gl.json"
SDF_BY_PROCESS = {"ff": "nom_ff_n40C_3v60", "ss": "nom_ss_125C_3v00", "tt": "nom_tt_025C_3v30"}


def sdf_for(corner: str) -> Path:
    return FINAL / "sdf" / SDF_BY_PROCESS[corner.split("_")[0]] / \
        f"{TOP}__{SDF_BY_PROCESS[corner.split('_')[0]]}.sdf"


def gl_sources(corner: str, work: Path) -> tuple[list[Path], list[str]]:
    """The gate-level sources for this corner, built in work/gl."""
    import check_glsim  # noqa: E402
    import speclib  # noqa: E402
    import ttlib  # noqa: E402
    gl = work / "gl"
    gl.mkdir(parents=True, exist_ok=True)
    nl, sdf = FINAL / "nl" / f"{TOP}.nl.v", sdf_for(corner)
    for p in (nl, sdf):
        if not p.is_file():
            raise SystemExit(f"cosim_gl: no {p}; run the vde harden gate first")
    renames = check_glsim.escaped_dot_renames(sdf.read_text(errors="replace"),
                                              nl.read_text(errors="replace"))
    isdf, inl = gl / "icarus.sdf", gl / "icarus.nl.v"
    check_glsim.sdf_for_icarus(sdf, isdf, renames)
    check_glsim.netlist_for_icarus(nl, inl, renames)
    spec = speclib.load_spec(C.WS / "digital" / "spec" / "spec.yaml")
    harness = gl / "ihsan_sa_pll_gl.v"
    harness.write_text(ttlib.generate_glsim_harness(spec, sdf_path=isdf))
    cells = check_glsim._cell_sources(check_glsim._pdk_root())
    return [HERE / "pll_cosim_top.v", harness, inl, *cells], ["-gspecify", "-ginterconnect"]


def run_one_gl(corner: str, extracted: Path, work: Path, timeout_s: float) -> dict:
    """cosim_corners.run_one with the sources and Icarus flags swapped."""
    import check_cosim  # noqa: E402
    import cocotb_tools.runner as R  # noqa: E402
    sources, build_args = gl_sources(corner, work)
    check_cosim.collect_sources = lambda _d: sources
    real = R.get_runner

    def get_runner(name):
        r = real(name)
        build = r.build
        r.build = lambda *a, **kw: build(*a, **{**kw, "build_args": build_args})
        return r
    R.get_runner = get_runner
    return CC.run_one(corner, extracted, work, timeout_s)


def input_hashes() -> dict[str, str]:
    h = CC.input_hashes()
    h["tb/cosim_gl.py"] = "sha256:" + hashlib.sha256((HERE / "cosim_gl.py").read_bytes()).hexdigest()
    for p in sorted([FINAL / "nl" / f"{TOP}.nl.v"] + [sdf_for(c) for c in ("ff_", "ss_", "tt_")]):
        if p.is_file():
            h[str(p.relative_to(C.WS))] = "sha256:" + hashlib.sha256(p.read_bytes()).hexdigest()
    return h


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--corners", nargs="*")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--timeout-s", type=float, default=CC.TIMEOUT_S)
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--one", help=argparse.SUPPRESS)
    ap.add_argument("--work", help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    extracted = CC.EXTRACTED
    if a.one:
        res = run_one_gl(a.one, extracted, Path(a.work), a.timeout_s)
        Path(a.out).write_text(json.dumps(res, indent=1, default=str))
        return 0 if res["status"] == "pass" else 1
    why = CC.bounding_corners(json.loads(CC.PEX_PVT.read_text()))
    corners = a.corners or list(why)
    inputs = input_hashes()
    root = C.WS / "log" / "cosim_corners_gl"

    def one(c: str) -> dict:
        work = root / c
        work.mkdir(parents=True, exist_ok=True)
        res_path = work / "result.json"
        res_path.unlink(missing_ok=True)
        cmd = [sys.executable, str(Path(__file__).resolve()), "--one", c, "--work", str(work),
               "--timeout-s", str(a.timeout_s), "--out", str(res_path)]
        with (work / "run.log").open("w") as f:
            try:
                subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                               timeout=a.timeout_s + 300)
            except subprocess.TimeoutExpired:
                pass
        try:
            res = json.loads(res_path.read_text())
        except (OSError, ValueError):
            tail = (work / "run.log").read_text(errors="replace").strip().splitlines()[-1:] or [""]
            res = {"corner": c, "status": "fail", "why": [f"no result: {tail[0][:200]}"],
                   "measures": None}
        res["bounds_the_range"] = why.get(c, [])
        res["sdf"] = SDF_BY_PROCESS[c.split("_")[0]]
        m = res.get("measures") or {}
        print(f"{c:14} {res['status']:4} lock {m.get('lock_time_us')} us, vctrl p-p "
              f"{m.get('vctrl_pp_last_10us_mv')} mV, {res.get('wall_s')} s"
              + "".join(f"\n    {w}" for w in res.get("why") or []), flush=True)
        return res

    with ThreadPoolExecutor(max(1, a.jobs)) as pool:
        results = list(pool.map(one, corners))
    passed = [r["corner"] for r in results if r["status"] == "pass"]
    rep = {"script": "cosim_gl", "gate": "cosim_corners_gl",
           "status": "pass" if corners and len(passed) == len(corners) else "fail",
           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "failing_count": len(corners) - len(passed),
           "failing": [{"corner": r["corner"], "msg": "; ".join(r.get("why") or [])[:300]}
                       for r in results if r["status"] != "pass"],
           "facts": {"corners": passed, "locked": [r["corner"] for r in results if CC.locks(r)],
                     "swept": corners, "bounding": why, "digital": "gate-level + SDF",
                     "max_sync_ns": CC.MAX_SYNC_NS, "results": results},
           "inputs": inputs}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(rep, indent=1, default=str) + "\n")
    print(f"cosim_gl: {len(passed)}/{len(corners)} corners meet every bound -> {a.out}")
    return 0 if rep["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
