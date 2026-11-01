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

The netlist, SDC, nom SPEF and SDFs the runs read are committed in tb/gl/
(the harden's runs/ is not in git); --snapshot refreshes tb/gl/ from a fresh
vde harden (chip-flow gate --gate harden --skill vde --workspace
blocks/pll/digital). LibreLane writes SDFs at three liberty corners only
(ff -40C, ss 125C, tt 25C); tb/gl/gen_sdf.tcl writes the others from the same
netlist/SDC/SPEF (*.gen.sdf). Each analog corner gets the SDF of its own
process at the nearest characterised temperature (sdf_corner_for: ff_125c_*
-> ff_125C, ss_m40c_* -> ss_n40C, 27C -> -40C, the nearer of -40/125). The
liberty sets tie voltage to process (ff 3.60 V, ss 3.00 V, tt 3.30 V), so the
digital supply is not moved with the analog one. --sdf-by-process restores
the process-only choice the first recorded run used.

--vctrl-pad-pf C puts C pF from vctrl to vss inside the extracted cell (the
ua[0] pad and its routing, parallel to C2), in a copy of the extracted
netlist; the default run, and the spec's nominal loop, leave it off.

Writes reports/recorded/cosim_corners_gl.json (with a pad:
cosim_corners_gl_pad<C>pf.json), shaped as cosim_corners.json, with the
netlist and SDF hashes added to its inputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import re
import shutil
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cosim_corners as CC  # noqa: E402
import pll_tb_common as C  # noqa: E402

FINAL = C.WS / "digital" / "harden" / "runs" / "run" / "final"
GL = HERE / "gl"
TOP = "tt_um_ihsan_sa_pll"
OUT = C.WS / "reports" / "recorded" / "cosim_corners_gl.json"
SDF_BY_PROCESS = {"ff": "nom_ff_n40C_3v60", "ss": "nom_ss_125C_3v00", "tt": "nom_tt_025C_3v30"}
# liberty corners characterised per process: temperature -> SDF corner
SDF_BY_TEMP = {"ff": {-40: "nom_ff_n40C_3v60", 125: "nom_ff_125C_3v60"},
               "ss": {-40: "nom_ss_n40C_3v00", 125: "nom_ss_125C_3v00"},
               "tt": {25: "nom_tt_025C_3v30"}}
BY_PROCESS_ONLY = False      # --sdf-by-process


def corner_temp_c(corner: str) -> int:
    """The analog corner's temperature from its name (the spec's grid
    names: <process>_<m40c|27c|125c>[_vm10|_vp10]; ss_pff/ff_pss are 27C)."""
    m = re.search(r"_(m?)(\d+)c(?:_|$)", corner)
    return (-1 if m.group(1) else 1) * int(m.group(2)) if m else 27


def sdf_corner_for(corner: str) -> str:
    proc = corner.split("_")[0]
    if BY_PROCESS_ONLY:
        return SDF_BY_PROCESS[proc]
    temps = SDF_BY_TEMP[proc]
    t = corner_temp_c(corner)
    return temps[min(temps, key=lambda k: (abs(k - t), k))]


def sdf_for(corner: str) -> Path:
    c = sdf_corner_for(corner)
    for name in (f"{TOP}__{c}.sdf", f"{TOP}__{c}.gen.sdf"):
        if (GL / name).is_file():
            return GL / name
    return GL / f"{TOP}__{c}.sdf"


def snapshot() -> None:
    """Copy the harden's netlist, SDC, nom SPEF and SDFs into tb/gl/ and
    write the SDFs LibreLane does not (gen_sdf.tcl)."""
    GL.mkdir(exist_ok=True)
    shutil.copy(FINAL / "nl" / f"{TOP}.nl.v", GL)
    shutil.copy(FINAL / "sdc" / f"{TOP}.sdc", GL)
    shutil.copy(FINAL / "spef" / "nom" / f"{TOP}.nom.spef", GL)
    for c in SDF_BY_PROCESS.values():
        shutil.copy(FINAL / "sdf" / c / f"{TOP}__{c}.sdf", GL)
    libdir = C.pdk_ngspice_dir().parents[1] / "libs.ref" / "gf180mcu_fd_sc_mcu7t5v0" / "lib"
    eda = CC.CFH / "bin" / "eda"
    for temps in SDF_BY_TEMP.values():
        for c in temps.values():
            if c in SDF_BY_PROCESS.values():
                continue
            lib = libdir / f"gf180mcu_fd_sc_mcu7t5v0__{c.removeprefix('nom_')}.lib"
            subprocess.run([str(eda), "sta", "-no_init", "-exit", "gen_sdf.tcl"], cwd=GL, check=True,
                           env={**os.environ, "LIB": str(lib), "OUT": str(GL / f"{TOP}__{c}.gen.sdf")})


def with_vctrl_pad(extracted: Path, pf: float, work: Path) -> Path:
    """A copy of the extracted cell with pf pF from vctrl to vss inside
    .subckt pll_analog (the ua[0] pad on the loop node)."""
    text = extracted.read_text()
    m = re.search(r"^\.subckt\s+pll_analog\b[^\n]*(?:\n\+[^\n]*)*", text, re.M | re.I)
    if not m:
        raise SystemExit(f"cosim_gl: no .subckt pll_analog in {extracted}")
    pins = m.group(0).replace("\n+", " ").split()[2:]
    assert "vctrl" in pins and "vss" in pins, pins
    end = text.index("\n.ends", m.end())
    out = work / f"{extracted.stem}.vctrl_pad{pf:g}pf.spice"
    out.write_text(text[:end] + f"\ncpad_vctrl_ua0 vctrl vss {pf:g}p" + text[end:])
    return out


def gl_sources(corner: str, work: Path) -> tuple[list[Path], list[str]]:
    """The gate-level sources for this corner, built in work/gl."""
    import check_glsim  # noqa: E402
    import speclib  # noqa: E402
    import ttlib  # noqa: E402
    gl = work / "gl"
    gl.mkdir(parents=True, exist_ok=True)
    nl, sdf = GL / f"{TOP}.nl.v", sdf_for(corner)
    for p in (nl, sdf):
        if not p.is_file():
            raise SystemExit(f"cosim_gl: no {p}; run the vde harden gate, then --snapshot")
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
    for p in sorted(GL.glob("*")):
        if p.is_file() and p.suffix != ".pyc":
            h[str(p.relative_to(C.WS))] = "sha256:" + hashlib.sha256(p.read_bytes()).hexdigest()
    return h


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--corners", nargs="*")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--timeout-s", type=float, default=CC.TIMEOUT_S)
    ap.add_argument("--out", help=f"default {OUT.relative_to(C.WS)} (_pad<C>pf with a pad)")
    ap.add_argument("--vctrl-pad-pf", type=float, default=0.0,
                    help="pF from vctrl to vss in the cell (the ua[0] pad); default none")
    ap.add_argument("--sdf-by-process", action="store_true",
                    help="SDF by process only (the first recorded run's choice)")
    ap.add_argument("--snapshot", action="store_true",
                    help="refresh tb/gl/ from the harden's runs/ and exit")
    ap.add_argument("--one", help=argparse.SUPPRESS)
    ap.add_argument("--work", help=argparse.SUPPRESS)
    ap.add_argument("--extracted-cell", help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    global BY_PROCESS_ONLY
    BY_PROCESS_ONLY = a.sdf_by_process
    if a.snapshot:
        snapshot()
        return 0
    tag = f"_pad{a.vctrl_pad_pf:g}pf" if a.vctrl_pad_pf else ""
    if not a.out:
        a.out = str(OUT.with_name(f"{OUT.stem}{tag}.json"))
    extracted = CC.EXTRACTED
    if a.one:
        res = run_one_gl(a.one, Path(a.extracted_cell or extracted), Path(a.work), a.timeout_s)
        Path(a.out).write_text(json.dumps(res, indent=1, default=str))
        return 0 if res["status"] == "pass" else 1
    why = CC.bounding_corners(json.loads(CC.PEX_PVT.read_text()))
    corners = a.corners or list(why)
    inputs = input_hashes()
    root = C.WS / "log" / f"cosim_corners_gl{tag}"
    root.mkdir(parents=True, exist_ok=True)
    if a.vctrl_pad_pf:
        extracted = with_vctrl_pad(extracted, a.vctrl_pad_pf, root)

    def one(c: str) -> dict:
        work = root / c
        work.mkdir(parents=True, exist_ok=True)
        res_path = work / "result.json"
        res_path.unlink(missing_ok=True)
        cmd = [sys.executable, str(Path(__file__).resolve()), "--one", c, "--work", str(work),
               "--timeout-s", str(a.timeout_s), "--out", str(res_path),
               "--extracted-cell", str(extracted)] + (["--sdf-by-process"] if a.sdf_by_process else [])
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
        res["sdf"] = sdf_corner_for(c)
        res["vctrl_pad_pf"] = a.vctrl_pad_pf
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
                     "sdf_choice": "process only" if a.sdf_by_process else "process + nearest temperature",
                     "vctrl_pad_pf": a.vctrl_pad_pf,
                     "max_sync_ns": CC.MAX_SYNC_NS, "results": results},
           "inputs": inputs}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(rep, indent=1, default=str) + "\n")
    print(f"cosim_gl: {len(passed)}/{len(corners)} corners meet every bound -> {a.out}")
    return 0 if rep["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
