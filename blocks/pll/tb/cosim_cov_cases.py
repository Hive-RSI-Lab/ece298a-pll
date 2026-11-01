#!/usr/bin/env python
"""cosim_cov_cases.py - follow-up cases of cosim_cov.py's bench, after its
default plan missed at ff_pss (N=3, 120 MHz, against the corner's 125.6 MHz
ceiling: the step winds vctrl past the supply and the last 4 us of the
20 us segment had not settled).

    $CHIP_FLOW_HOME/bin/eda python blocks/pll/tb/cosim_cov_cases.py [--jobs N]

Each case runs cosim_cov.py --one with its own plan and pad, extracted cell +
gate-level digital, into log/cosim_cov_cases/<case>/. Writes
reports/recorded/cosim_cov_cases.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
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

STEPS = [[0, 1], [20000, 3], [40000, 2]]
CASES = {
    # does the 120 MHz step at the lowest-ceiling corner settle, given time?
    "ff_pss_step_120_long": ("ff_pss", 0, 5e6, [[0, 1], [20000, 3]], 70000),
    # the same point acquired directly from pll_en
    "ff_pss_direct_120": ("ff_pss", 0, 5e6, [[0, 3]], 30000),
    # the same step with the pad on vctrl
    "ff_pss_step_120_pad5p": ("ff_pss", 5, 5e6, [[0, 1], [20000, 3]], 70000),
    # the lowest pad-loaded phase margin: its steps, then the largest in-range P*N
    "ff_125c_vp10_steps_pad5p": ("ff_125c_vp10", 5, 5e6, STEPS, 60000),
    "ff_125c_vp10_pn32_pad5p": ("ff_125c_vp10", 5, 5e6, [[0, 4]], 30000),
    # the top of the reference range
    "tt_27c_fref12p5_n1": ("tt_27c", 0, 12.5e6, [[0, 1]], 20000),
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--timeout-s", type=float, default=30000.0)
    ap.add_argument("--cases", nargs="*", default=list(CASES))
    a = ap.parse_args()
    root = C.WS / "log" / "cosim_cov_cases"
    root.mkdir(parents=True, exist_ok=True)
    pad = GL.with_vctrl_pad(CC.EXTRACTED, 5.0, root)
    inputs = GL.input_hashes()
    for f in (HERE / "cosim_cov.py", HERE / "cosim_cov_cases.py", HERE / "cov" / "test_pll_cov.py"):
        inputs[str(f.relative_to(C.WS))] = "sha256:" + hashlib.sha256(f.read_bytes()).hexdigest()

    def one(name: str) -> dict:
        corner, pf, fref, segs, dur = CASES[name]
        work = root / name
        work.mkdir(parents=True, exist_ok=True)
        res = work / "result.json"
        res.unlink(missing_ok=True)
        plan = {"f_ref_hz": fref, "segments": segs, "duration_ns": dur}
        cmd = [sys.executable, str(HERE / "cosim_cov.py"), "--one", corner, "--work", str(work),
               "--extracted-cell", str(pad if pf else CC.EXTRACTED), "--plan", json.dumps(plan),
               "--timeout-s", str(a.timeout_s), "--out", str(res)]
        with (work / "run.log").open("w") as f:
            subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
        try:
            r = json.loads(res.read_text())
        except (OSError, ValueError):
            r = {"corner": corner, "status": "fail", "why": ["no result"], "measures": None}
        r.update(case=name, vctrl_pad_pf=pf)
        print(name, r["status"], r.get("why"), flush=True)
        return r

    with ThreadPoolExecutor(a.jobs) as pool:
        results = list(pool.map(one, a.cases))
    out = C.WS / "reports" / "recorded" / "cosim_cov_cases.json"
    out.write_text(json.dumps({"script": "cosim_cov_cases", "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                               "facts": {"results": results}, "inputs": inputs}, indent=1, default=str) + "\n")
    print("cosim_cov_cases: done ->", out, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
