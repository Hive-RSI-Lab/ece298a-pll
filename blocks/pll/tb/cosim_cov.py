#!/usr/bin/env python
"""cosim_cov.py - closed-loop coverage beyond the 100 MHz point: other
divider settings and re-lock after a change of N, on the extracted analog
cell with the gate-level digital and its SDF in the loop (cosim_gl.py's
sources and SDF choice).

    $CHIP_FLOW_HOME/bin/eda python blocks/pll/tb/cosim_cov.py \
        [--corners NAME ...] [--plan JSON] [--vctrl-pad-pf C] [--jobs N] [--out FILE]

The bench is tb/cov/test_pll_cov.py (its docstring says what it measures).
Default plan: f_ref = 5 MHz, n_sel 1 -> 3 -> 2 (VCO 40 -> 120 -> 80 MHz, the
bottom, near the top and the middle of the 13..125 MHz every corner covers),
20 us each, the loop running throughout: the first segment is acquisition
from pll_en, the next two re-lock after a step of N. Default corners: the
bounding corners (cosim_corners.bounding_corners) plus tt_27c.
Writes reports/recorded/cosim_cov.json.
"""
from __future__ import annotations

import argparse
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
import cosim_gl as GL  # noqa: E402
import pll_tb_common as C  # noqa: E402

COV = HERE / "cov"
OUT = C.WS / "reports" / "recorded" / "cosim_cov.json"
PLAN = {"f_ref_hz": 5e6, "segments": [[0, 1], [20000, 3], [40000, 2]], "duration_ns": 60000}
TIMEOUT_S = 3 * 3600.0


def run_one(corner: str, extracted: Path, work: Path, plan: dict, timeout_s: float) -> dict:
    import check_cosim  # noqa: E402
    import cocotb_tools.runner as R  # noqa: E402
    import cocotblib  # noqa: E402
    check_cosim.ensure_ngspice_env(check_cosim.toolchain_root())
    work.mkdir(parents=True, exist_ok=True)
    meas = work / "measures.json"
    meas.unlink(missing_ok=True)
    os.environ["PLL_COSIM_SETUP"] = json.dumps(CC.setup_for(corner, extracted, meas))
    os.environ["PLL_COSIM_MAX_SYNC_NS"] = str(CC.MAX_SYNC_NS)
    os.environ["PLL_COV_PLAN"] = json.dumps(plan)
    sources, build_args = GL.gl_sources(corner, work)
    real = R.get_runner

    def get_runner(name):
        r = real(name)
        build = r.build
        r.build = lambda *a, **kw: build(*a, **{**kw, "build_args": build_args})
        return r
    R.get_runner = get_runner
    t0 = time.monotonic()
    err = None
    try:
        cocotblib.run_cocotb(work / "build", COV, sources, "pll_cosim_top", ["test_pll_cov"],
                             work / "results.xml", timeout_s=timeout_s)
    except Exception as e:  # noqa: BLE001
        err = f"{type(e).__name__}: {str(e).strip()[:200]}"
    log = work / "build" / "sim.log"
    nonconv = check_cosim.scan_nonconvergence(log.read_text(errors="replace")) if log.is_file() else []
    m = json.loads(meas.read_text()) if meas.is_file() else None
    segs = (m or {}).get("segments") or []
    why = ([err] if err else []) + [f"ngspice: {n}" for n in nonconv] + \
        ([] if m else ["no measures"]) + \
        [f"N={s['n_sel']} not locked at {s['f_vco_target_mhz']:.0f} MHz" for s in segs if not s["pass"]] + \
        ([f"bridge: {m['bridge_error']}"] if m and m.get("bridge_error") else []) + \
        ([f"{len(segs)} of {len(plan['segments'])} segments ran"] if m and len(segs) != len(plan["segments"]) else [])
    return {"corner": corner, "status": "fail" if why else "pass", "why": why, "sdf": GL.sdf_corner_for(corner),
            "wall_s": round(time.monotonic() - t0, 1), "measures": m}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--corners", nargs="*")
    ap.add_argument("--plan", help="json, default " + json.dumps(PLAN))
    ap.add_argument("--vctrl-pad-pf", type=float, default=0.0)
    ap.add_argument("--jobs", type=int, default=5)
    ap.add_argument("--timeout-s", type=float, default=TIMEOUT_S)
    ap.add_argument("--out")
    ap.add_argument("--one", help=argparse.SUPPRESS)
    ap.add_argument("--work", help=argparse.SUPPRESS)
    ap.add_argument("--extracted-cell", help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    plan = json.loads(a.plan) if a.plan else PLAN
    if a.one:
        res = run_one(a.one, Path(a.extracted_cell), Path(a.work), plan, a.timeout_s)
        Path(a.out).write_text(json.dumps(res, indent=1, default=str))
        return 0 if res["status"] == "pass" else 1
    tag = f"_pad{a.vctrl_pad_pf:g}pf" if a.vctrl_pad_pf else ""
    out = Path(a.out) if a.out else OUT.with_name(f"{OUT.stem}{tag}.json")
    why = CC.bounding_corners(json.loads(CC.PEX_PVT.read_text()))
    corners = a.corners or list(why) + ["tt_27c"]
    root = C.WS / "log" / f"cosim_cov{tag}"
    root.mkdir(parents=True, exist_ok=True)
    extracted = CC.EXTRACTED
    if a.vctrl_pad_pf:
        extracted = GL.with_vctrl_pad(extracted, a.vctrl_pad_pf, root)
    inputs = GL.input_hashes()
    for f in (HERE / "cosim_cov.py", COV / "test_pll_cov.py"):
        import hashlib
        inputs[str(f.relative_to(C.WS))] = "sha256:" + hashlib.sha256(f.read_bytes()).hexdigest()

    def one(c: str) -> dict:
        work = root / c
        work.mkdir(parents=True, exist_ok=True)
        res_path = work / "result.json"
        res_path.unlink(missing_ok=True)
        cmd = [sys.executable, str(Path(__file__).resolve()), "--one", c, "--work", str(work),
               "--extracted-cell", str(extracted), "--plan", json.dumps(plan),
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
            res = {"corner": c, "status": "fail", "why": [f"no result: {tail[0][:200]}"], "measures": None}
        res["vctrl_pad_pf"] = a.vctrl_pad_pf
        segs = (res.get("measures") or {}).get("segments") or []
        print(f"{c:14} {res['status']:4} " + "; ".join(
            f"N={s['n_sel']} {s['f_vco_target_mhz']:.0f} MHz lock {s['lock_rise_after_change_us']} us "
            f"err {s['fb_period_rel_err']}" for s in segs) + "".join(f"\n    {w}" for w in res.get("why") or []),
            flush=True)
        return res

    with ThreadPoolExecutor(max(1, a.jobs)) as pool:
        results = list(pool.map(one, corners))
    passed = [r["corner"] for r in results if r["status"] == "pass"]
    rep = {"script": "cosim_cov", "status": "pass" if len(passed) == len(corners) else "fail",
           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "failing": [{"corner": r["corner"], "msg": "; ".join(r.get("why") or [])[:300]}
                       for r in results if r["status"] != "pass"],
           "facts": {"plan": plan, "corners": passed, "swept": corners, "vctrl_pad_pf": a.vctrl_pad_pf,
                     "digital": "gate-level + SDF (process + nearest temperature)", "results": results},
           "inputs": inputs}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rep, indent=1, default=str) + "\n")
    print(f"cosim_cov: {len(passed)}/{len(corners)} corners lock at every setting -> {out}")
    return 0 if rep["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
