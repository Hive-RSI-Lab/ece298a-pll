#!/usr/bin/env python3
"""Monte Carlo of pll_analog at tt_27c with the GF180 PDK's own statistics.

What the PDK carries (gf180mcuD libs.tech/ngspice/sm141064.spice):
  * `.lib fets_mm` (pulled in by every MOS corner, `typical` included) wraps
    nfet_03v3 / pfet_03v3 / *_06v0 in subckts with per-instance Pelgrom
    mismatch: delvto = agauss(0, 0.7071*par_vth/sqrt(Weff*Leff), 1) and
    mulu0 = 1 - agauss(0, 0.7071*par_k/sqrt(Weff*Leff), 1), both scaled by
    sw_stat_mismatch (0 in design.spice). par_vth = 7.148 mV*um (nfet_03v3),
    6.66 mV*um (pfet_03v3); so a matched pair has sigma(dVth) = par_vth/sqrt(WL).
  * `.lib statistical` / `res_statistical`: global (die-to-die) process
    variation, scaled by sw_stat_global (0 in design.spice).
  * Poly resistors (ppolyf_u ...) have mis_r = 0: no per-instance mismatch.
  * The mismatch wrapper draws ONE delvto per X instance and ignores m, so an
    m=4 instance would get a single-device sigma instead of sigma/2. This
    script therefore simulates a copy of the netlist with every m=N instance
    expanded into N m=1 instances (the layout draws them as separate devices).

Modes:
  mm      typical models + res_typical, sw_stat_mismatch = 1 (local only)
  glob_mm statistical + res_statistical, sw_stat_global = 1 and
          sw_stat_mismatch = 1 (die-to-die + local)

Benches (schematic netlist, tt_27c device corner, 27 C, 3.3 V):
  cp       tb/pll_analog_cp_tb.cir stimulus, own .control: Icp UP/DN code 00,
           cp_updn_mismatch_pct (same definition as the bench), bias current
           Ib (through a 0 V sense source added to RBIAS_INT in the MC copy).
  overlap  tb/pll_analog_overlap_tb.cir stimulus: signed net charge per
           1 ns overlap event at vctrl = 0.3 / vdd/2 / vdd-0.3; the measure
           cp_overlap_net_charge_fc = max |Q|; static phase offset at vdd/2:
           spo_ps = -Q/Idn if Q > 0, -Q/Iup if Q < 0 (UP lead positive): the
           lead that cancels the net charge.
  vco      tb/pll_analog_vco_tb.cir stimulus, one 120 ns tran at vctrl = vdd/2
           (~100 MHz at tt): f = 5 / (rise 6 - rise 1) after 20 ns. (80 ns
           censored the slow tail: seed 62 ran out of rises.)
  startup  tb/pll_analog_startup_tb.cir as is, plus the settled vref and
           bias_ref at the end of the window (catches the high-Ib state).

Every run also simulates seed 0 with the statistics off: `nominal` in the report.
--corner takes another corner's models/temp/vdd from its rendered deck in
log/sim (mode mm only). Progress is checkpointed to /tmp, so a killed run
resumes where it stopped.

Usage: mc_mismatch.py --mode mm --n 200 [--jobs 4] [--benches cp,overlap,vco,startup]
                      [--corner tt_27c]
Writes reports/recorded/mc_<mode>_<corner>.json (summary + per-sample values).
"""
import argparse
import concurrent.futures as cf
import datetime
import json
import math
import os
import re
import statistics
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
BLOCK = os.path.dirname(HERE)
PDK = "/opt/eda-toolchain/iic-osic-tools-2026.09/foss/pdks/gf180mcuD"
EDA_ENV = os.path.expanduser("~/modules/bin/eda")

# spec bounds (spec/spec.yaml) for the measures that have one
BOUNDS = {
    "icp_up_code00_ua": (12.0, 30.0),
    "icp_dn_code00_ua": (12.0, 30.0),
    "cp_updn_mismatch_pct": (None, 10.0),
    "icp_code11_over_code00_ratio": (1.8, 2.2),
    "cp_overlap_net_charge_fc": (None, 10.0),
    "startup_time_us": (None, 5.0),
}


def sizing_line():
    y = yaml.safe_load(open(os.path.join(BLOCK, "sizing", "sizing.yaml")))
    return ".param " + " ".join(f"{k}={v['value']}" for k, v in y.items())


def sizing_values():
    y = yaml.safe_load(open(os.path.join(BLOCK, "sizing", "sizing.yaml")))
    return {k: v["value"] for k, v in y.items()}


def expanded_netlist(path):
    """Copy of netlist/pll_analog.cir with m=N instances split into N, and a
    0 V sense source in series with RBIAS_INT (for Ib)."""
    sz = sizing_values()
    out = []
    for line in open(os.path.join(BLOCK, "netlist", "pll_analog.cir")):
        m = re.match(r"^(X\S+)(.*)\sm=(\S+)\s*$", line)
        if m and not line.startswith("*"):
            name, body, mv = m.groups()
            n = int(float(sz.get(mv, mv)))
            for k in range(n):
                out.append(f"{name}_{k}{body} m=1\n")
            continue
        if line.startswith("XRBIAS_INT "):
            line = line.replace("XRBIAS_INT bias_ref vss vss", "XRBIAS_INT bias_ref ib_sense vss")
            out.append(line)
            out.append("VIB_SENSE ib_sense vss 0\n")
            continue
        out.append(line)
    open(path, "w").write("".join(out))


def corner_setup(mode, corner):
    """(MOS lib, resistor lib, MIM lib, temp, vdd) of a corner."""
    if mode == "glob_mm":
        return "statistical", "res_statistical", "mimcap_typical", "27", "3.3"
    deck = open(os.path.join(BLOCK, "log", "sim", f"pll_analog_cp_tb__{corner}.cir")).read()
    libs = re.findall(r"^\.lib '[^']*sm141064\.spice' (\S+)", deck, re.M)
    temp = re.search(r"^\.temp (\S+)", deck, re.M).group(1)
    vdd = re.search(r"^\.param vddp=(\S+)", deck, re.M).group(1)
    return libs[0], libs[1], libs[2], temp, vdd


def render(tb, mode, seed, netlist, corner):
    """seed 0 is the nominal reference: the statistics stay off."""
    t = open(os.path.join(BLOCK, "tb", tb)).read()
    mos, res, mim, temp, vdd = corner_setup(mode, corner)
    if seed == 0:
        mos, res = {"statistical": "typical"}.get(mos, mos), {"res_statistical": "res_typical"}.get(res, res)
    t = (t.replace("{{PDK}}", PDK).replace("{{CORNER}}", mos)
          .replace("{{RES_CORNER}}", res).replace("{{MIM_CORNER}}", mim)
          .replace("{{NETLIST}}", netlist).replace("{{SIZING}}", sizing_line())
          .replace("{{TEMP_C}}", temp).replace("{{VDD}}", vdd))
    if seed == 0:
        return t
    sw = ".param sw_stat_mismatch=1\n"
    if mode == "glob_mm":
        sw += ".param sw_stat_global=1\n"
    sw += f".option seed={seed}\n"
    inc = f".include '{PDK}/libs.tech/ngspice/design.spice'\n"
    assert inc in t
    return t.replace(inc, inc + sw, 1)


def replace_control(t, control):
    a = t.index(".control")
    b = t.index(".endc") + len(".endc")
    return t[:a] + control.strip() + "\n" + t[b:]


CP_CONTROL = r"""
.control
set noaskquit
alter vup dc = $&vddp
op
let x = i(vvc)*1e6
set iu00 = "$&x"
let x = i(v.xdut.vib_sense)*1e6
set ib = "$&x"
let x = v(xdut.vref)
set vref = "$&x"
alter vup dc = 0
alter vdn dc = $&vddp
op
let x = -i(vvc)*1e6
set id00 = "$&x"
alter vdn dc = 0
alter vup dc = $&vddp
alter vt0 dc = $&vddp
alter vt1 dc = $&vddp
op
let x = i(vvc)*1e6/$iu00
set rat = "$&x"
alter vt0 dc = 0
alter vt1 dc = 0
dc vvc 0.3 $&vhi $&vstp
set pu = $curplot
let iupv = i(vvc)
alter vup dc = 0
alter vdn dc = $&vddp
dc vvc 0.3 $&vhi $&vstp
let idnv = -i(vvc)
let icpm = ($iu00 + $id00)/2
let x = vecmax(abs({$pu}.iupv - idnv))*1e6/icpm*100
set mm = "$&x"
echo "MC icp_up_code00_ua = $iu00"
echo "MC icp_dn_code00_ua = $id00"
echo "MC cp_updn_mismatch_pct = $mm"
echo "MC icp_code11_over_code00_ratio = $rat"
echo "MC ib_ua = $ib"
echo "MC vref_v = $vref"
.endc
"""

OVERLAP_CONTROL = r"""
.control
set noaskquit
alter vvc dc = 0.3
tran 10p 140n 0 10p
meas tran q0 integ i(vvc) from=99n to=139n
let x0 = q0*1e15
echo "MC q_v0_fc = $&x0"
destroy $curplot
alter vvc dc = $&vmid
tran 10p 140n 0 10p
meas tran q1 integ i(vvc) from=99n to=139n
let x1 = q1*1e15
echo "MC q_v1_fc = $&x1"
destroy $curplot
alter vvc dc = $&vhi
tran 10p 140n 0 10p
meas tran q2 integ i(vvc) from=99n to=139n
let x2 = q2*1e15
echo "MC q_v2_fc = $&x2"
destroy $curplot
.endc
"""

VCO_CONTROL = r"""
.control
set noaskquit
alter vvc dc = $&vmid
tran 20p 120n 0 20p
meas tran ta when v(xdut.vco_out)=$&vmid rise=1 td=20n
meas tran tb when v(xdut.vco_out)=$&vmid rise=6 td=20n
let x = 5/(tb - ta)/1e6
echo "MC vco_f_mid_mhz = $&x"
.endc
"""


def bench_text(bench, mode, seed, netlist, corner):
    if bench == "cp":
        return replace_control(render("pll_analog_cp_tb.cir", mode, seed, netlist, corner), CP_CONTROL)
    if bench == "overlap":
        return replace_control(render("pll_analog_overlap_tb.cir", mode, seed, netlist, corner), OVERLAP_CONTROL)
    if bench == "vco":
        return replace_control(render("pll_analog_vco_tb.cir", mode, seed, netlist, corner), VCO_CONTROL)
    if bench == "startup":
        t = render("pll_analog_startup_tb.cir", mode, seed, netlist, corner)
        extra = ('meas tran vref_end avg v(xdut.vref) from=$&t_tail to=$&t_stop\n'
                 'meas tran vbr_end avg v(bias_ref) from=$&t_tail to=$&t_stop\n'
                 'echo "MC startup_time_us = $res"\n'
                 'echo "MC vref_end_v = $&vref_end"\n'
                 'echo "MC bias_ref_end_v = $&vbr_end"\n')
        return t.replace("echo\necho \"  Measurements for Transient", extra + "echo\necho \"  Measurements for Transient", 1)
    raise ValueError(bench)


EXPECTED = {
    "cp": ["icp_up_code00_ua", "icp_dn_code00_ua", "cp_updn_mismatch_pct",
           "icp_code11_over_code00_ratio", "ib_ua", "vref_v"],
    "overlap": ["q_v0_fc", "q_v1_fc", "q_v2_fc"],
    "vco": ["vco_f_mid_mhz"],
    "startup": ["startup_time_us", "vref_end_v", "bias_ref_end_v"],
}


def run_one(bench, mode, seed, netlist, workdir, corner):
    cir = os.path.join(workdir, f"{bench}_{mode}_{seed}.cir")
    open(cir, "w").write(bench_text(bench, mode, seed, netlist, corner))
    env = dict(os.environ, PDK="gf180mcuD", PATH=EDA_ENV + ":" + os.environ["PATH"])
    try:
        p = subprocess.run(["ngspice", "-b", cir], capture_output=True, text=True,
                           timeout=1800, cwd=workdir, env=env)
        out = p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return bench, seed, {"error": "timeout"}
    res = {}
    for k, v in re.findall(r"^MC (\w+) = (\S+)", out, re.M):
        try:
            res[k] = float(v)
        except ValueError:
            res[k] = v
    missing = [k for k in EXPECTED[bench] if k not in res]
    if missing:
        res["error"] = f"missing {missing}: " + out[-400:]
    else:
        os.remove(cir)
    return bench, seed, res


def binom_cdf(k, n, p):
    return sum(math.comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k + 1))


def fail_ci95(k, n):
    """Clopper-Pearson 95 % interval of a failure rate, k failures in n."""
    def solve(f):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if f(mid):
                lo = mid
            else:
                hi = mid
        return lo
    low = 0.0 if k == 0 else solve(lambda p: 1 - binom_cdf(k - 1, n, p) < 0.025)
    high = 1.0 if k == n else solve(lambda p: binom_cdf(k, n, p) > 0.025)
    return [round(low, 4), round(high, 4)]


def derive(r):
    """Measures computed from the raw per-sample values."""
    qs = [r.get(f"q_v{i}_fc") for i in range(3)]
    if all(isinstance(q, float) for q in qs):
        r["cp_overlap_net_charge_fc"] = round(max(abs(q) for q in qs), 5)
    q = r.get("q_v1_fc")
    iu, id_ = r.get("icp_up_code00_ua"), r.get("icp_dn_code00_ua")
    if isinstance(q, float) and isinstance(iu, float) and isinstance(id_, float):
        r["spo_ps"] = round(-q * 1e-15 / ((id_ if q > 0 else iu) * 1e-6) * 1e12, 4)


def summarise(samples):
    keys = sorted({k for s in samples.values() for k in s if k != "error"})
    summ = {}
    for k in keys:
        vals = [s[k] for s in samples.values() if isinstance(s.get(k), float)]
        nonnum = [s[k] for s in samples.values() if k in s and not isinstance(s[k], float)]
        if not vals:
            continue
        mu = statistics.fmean(vals)
        sd = statistics.stdev(vals) if len(vals) > 1 else 0.0
        e = {"n": len(vals), "mean": round(mu, 5), "sigma": round(sd, 5),
             "min": round(min(vals), 5), "max": round(max(vals), 5)}
        if nonnum:
            e["non_numeric"] = sorted(set(map(str, nonnum)))
            e["non_numeric_count"] = len(nonnum)
        if k in BOUNDS:
            lo, hi = BOUNDS[k]
            e["bound"] = {"min": lo, "max": hi}
            fails = [v for v in vals if (lo is not None and v < lo) or (hi is not None and v > hi)]
            e["fail_count"] = len(fails) + len(nonnum)
            e["fail_rate_ci95"] = fail_ci95(e["fail_count"], e["n"] + len(nonnum))
            margins = []
            if hi is not None and sd > 0:
                margins.append((hi - mu) / sd)
            if lo is not None and sd > 0:
                margins.append((mu - lo) / sd)
            if margins:
                e["margin_sigma"] = round(min(margins), 2)
        summ[k] = e
    return summ


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["mm", "glob_mm"], default="mm")
    ap.add_argument("--corner", default="tt_27c")
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed0", type=int, default=1)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--benches", default="cp,overlap,vco,startup")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if a.mode == "glob_mm" and a.corner != "tt_27c":
        ap.error("glob_mm replaces the corner models: tt_27c only")
    benches = a.benches.split(",")
    tag = f"mc_{a.mode}_{a.corner}"
    out = a.out or os.path.join(BLOCK, "reports", "recorded", f"{tag}.json")
    work = tempfile.mkdtemp(prefix="pll_mc_", dir="/tmp")
    netlist = os.path.join(work, "pll_analog_mc.cir")
    expanded_netlist(netlist)
    seeds = list(range(a.seed0, a.seed0 + a.n))
    per = {b: {} for b in benches}
    ckpt = f"/tmp/pll_{tag}.ckpt.jsonl"
    if os.path.exists(ckpt):
        for line in open(ckpt):
            b, s, r = json.loads(line)
            if b in per and "error" not in r:
                per[b][s] = r
    todo = [(b, s) for s in [0] + seeds for b in benches if s not in per[b]]
    print(f"{len(todo)} runs to do", flush=True)
    with cf.ThreadPoolExecutor(a.jobs) as ex, open(ckpt, "a") as ck:
        futs = [ex.submit(run_one, b, a.mode, s, netlist, work, a.corner) for b, s in todo]
        for i, f in enumerate(cf.as_completed(futs)):
            b, s, r = f.result()
            per[b][s] = r
            ck.write(json.dumps([b, s, r]) + "\n")
            ck.flush()
            if (i + 1) % 20 == 0:
                print(f"{i + 1}/{len(futs)}", flush=True)
    # one sample = one seed: the same seed draws the same devices in every bench
    samples, errs = {}, {}
    for b in benches:
        for s, r in per[b].items():
            samples.setdefault(s, {}).update({k: v for k, v in r.items() if k != "error"})
            if "error" in r:
                errs.setdefault(s, {})[b] = r["error"]
    for r in samples.values():
        derive(r)
    nominal = samples.pop(0)
    rep = {
        "script": "mc/mc_mismatch.py",
        "mode": a.mode,
        "corner": a.corner,
        "corner_setup": dict(zip(["mos", "res", "mim", "temp_c", "vdd"], corner_setup(a.mode, a.corner))),
        "netlist": "netlist/pll_analog.cir (schematic), m=N instances expanded to N devices",
        "statistics": ("sw_stat_mismatch=1" if a.mode == "mm" else "sw_stat_global=1, sw_stat_mismatch=1"),
        "n": a.n, "seeds": [seeds[0], seeds[-1]], "benches": benches,
        "date": datetime.date.today().isoformat(),
        "nominal": nominal,
        "summary": summarise(samples),
        "errors": {str(s): e for s, e in errs.items()},
        "samples": {str(s): samples[s] for s in sorted(samples)},
    }
    json.dump(rep, open(out, "w"), indent=1)
    if not errs:
        os.remove(ckpt)
    print(json.dumps({"nominal": nominal, "summary": rep["summary"]}, indent=1))
    print("errors:", len(errs), "->", out)


if __name__ == "__main__":
    main()
