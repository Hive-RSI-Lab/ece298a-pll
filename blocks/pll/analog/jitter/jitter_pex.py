#!/usr/bin/env python3
"""VCO period jitter and phase noise on the extracted cell at the 100 MHz
operating point, plus a linear-model closed-loop estimate. Results and caveats:
jitter/RESULT.md.

ngspice-47 has no device transient noise, so the bench adds trnoise current
sources to the extracted netlist (log/pex_pvt/pll_analog.pex.ordered.spice):

  * every MOS except the output buffer and divider: drain to source, white and
    1/f levels from a BSIM4 .noise of a copy of the instance at its own bias
    (device_noise). Ring devices are biased as at their ring node's vdd/2
    crossing, the others at the average over the last 100 ns of a noiseless run.
  * every poly resistor except the R1 segment on vctrl: 4 k T / R. vctrl is held
    by an ideal source, so R1 enters the closed-loop model instead.

vctrl is found per corner by a secant search on the noiseless ring (100 MHz
+- 0.05 %). Three kinds of run: full (white + 1/f), white only, 1/f only, and a
noiseless floor. Rising vdd/2 crossings of r5 and vco_out after the settle time;
sigma_T has the mean, a linear drift and the deterministic period-2 pattern
removed (the pattern is reported apart).

L_vco(f) = a2/f^2 + b3/f^3: see analyse(). Closed loop (a linear continuous-time
model, not a simulation): H_ol(s) = Icp/(2 pi) * Kvco/s * Z(s) / PN, output phase
noise = L_vco |1/(1+H_ol)|^2 + R1's thermal noise through its own transfer, loop
values per corner (corner_loop).

Writes reports/recorded/jitter_pex.json. Usage in RESULT.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

CFH = Path(os.environ.get("CHIP_FLOW_HOME") or "/opt/chip-flow")
sys.path[:0] = [str(CFH / "engine" / "scripts"), str(CFH / "engine" / "lib")]
import sim_run  # noqa: E402
import speclib  # noqa: E402

WS = Path(__file__).resolve().parent.parent
DEF_NETLIST = WS / "log" / "pex_pvt" / "pll_analog.pex.ordered.spice"
OUT_JSON = WS / "reports" / "recorded" / "jitter_pex.json"
WORK = WS / "log" / "jitter_pex"
KB = 1.380649e-23
F_TARGET = 100e6
RING = {f"r{i}" for i in range(1, 6)}
NT = 50e-12          # trnoise sample interval (white to 10 GHz, >> the ring edges ~1 GHz)
TSTEP = 50e-12       # tran max step (the floor run measures what it costs)
T_SETTLE = 300e-9

# loop values: the paper's at the 100 MHz tt point; corner_loop replaces Icp, R1,
# C1, C2 per corner and analyse takes Kvco from the search points.
R1_SEGMENTS = ("X127", "X21", "X137", "X170")  # R1 in the extraction: vctrl .. vfilt
LOOP = {"icp_a": 18.8e-6, "r1_ohm": 27e3, "c1_f": 20.1e-12, "c2_f": 2.1e-12, "pn": 16,
        "f_ref_hz": 6.25e6}

MOSCAP = """.param cap_nmos_03v3_b_corner=mim_corner_2p0ff
.subckt cap_nmos_03v3_b 1 2 c_length=1e-6 c_width=1e-6 dtemp=0
.param cvar1=0.002458 cvar2=0.001533 cvar3=1.515152 cvar4=0.560606
C1 1 2 q='cap_nmos_03v3_b_corner*c_length*c_width*(cvar1*v(1,2)+cvar2/cvar3*(abs(cvar3*v(1,2)+cvar4)+ln(1+exp(-2*abs(cvar3*v(1,2)+cvar4)))-ln(2)))'
.ends cap_nmos_03v3_b"""


def base(n: str) -> str:
    return n.split(".t")[0] if re.search(r"\.t\d+$", n) else n


def parse_devices(netlist: Path) -> tuple[list[dict], list[dict]]:
    """MOS and poly-resistor instances of the extracted subckt."""
    mos, res = [], []
    for line in netlist.read_text().splitlines():
        if not line.startswith("X"):
            continue
        tok = line.split()
        name = tok[0]
        kv = dict(t.split("=", 1) for t in tok if "=" in t)
        model = [t for t in tok[1:] if "=" not in t][-1]
        if model in ("nfet_03v3", "pfet_03v3"):
            d, g, s, b = tok[1:5]
            mos.append({"name": name, "d": d, "g": g, "s": s, "b": b, "model": model,
                        "w": kv.get("w"), "l": kv.get("l"), "line": line})
        elif model == "ppolyf_u":
            res.append({"name": name, "a": tok[1], "b": tok[2], "sub": tok[3],
                        "r_length": kv["r_length"], "r_width": kv["r_width"]})
    for m in mos:
        out = [t for t in (m["d"], m["s"]) if base(t) in RING]
        m["ring_out"] = base(out[0]) if base(m["g"]) in RING and out else None
    return mos, res


def header(subs: dict, netlist: Path) -> str:
    p = f"{subs['PDK']}/libs.tech/ngspice"
    return "\n".join([
        f".include '{p}/design.spice'",
        f".lib '{p}/sm141064.spice' {subs['CORNER']}",
        f".lib '{p}/sm141064.spice' {subs['RES_CORNER']}",
        f".lib '{p}/sm141064.spice' {subs['MIM_CORNER']}",
        MOSCAP, f".include '{netlist}'", subs["SIZING"], f".temp {subs['TEMP_C']}",
        f".param vddp={subs['VDD']}", ""])


BENCH = """vdd_src vdd 0 dc {vddp}
vss_src vss 0 dc 0
ven pll_en 0 dc {vddp}
vup pfd_up 0 dc 0
vdn pfd_dn 0 dc 0
vt0 cp_trim0 0 dc 0
vt1 cp_trim1 0 dc 0
vvc vctrl 0 dc VCTRL
cload2 vco_div2 0 30f
xdut vco_div2 pfd_up pfd_dn pll_en cp_trim0 cp_trim1 vctrl bias_ref vdd vss pll_analog
ikick 0 xdut.r1 pulse(0 200u 1n 50p 50p 1n 1)
"""


def ngspice(deck: str, work: Path, tag: str, timeout: float) -> str:
    work.mkdir(parents=True, exist_ok=True)
    cir = work / f"{tag}.cir"
    cir.write_text(deck)
    cmd = [str(sim_run.EDA_BIN), "ngspice", "-b", str(cir)] if Path(sim_run.EDA_BIN).is_file() \
        else ["ngspice", "-b", str(cir)]
    r = subprocess.run(cmd, cwd=work, capture_output=True, text=True, timeout=timeout)
    (work / f"{tag}.log").write_text(r.stdout + r.stderr)
    return r.stdout + r.stderr


def read_wr(path: Path) -> list[list[float]]:
    rows = []
    for line in path.read_text().splitlines():
        try:
            rows.append([float(x) for x in line.split()])
        except ValueError:
            continue
    return rows


def rises(t: list[float], v: list[float], th: float, t0: float) -> list[float]:
    out = []
    for i in range(1, len(t)):
        if v[i - 1] < th <= v[i] and t[i] > t0:
            out.append(t[i - 1] + (th - v[i - 1]) * (t[i] - t[i - 1]) / (v[i] - v[i - 1]))
    return out


def freq_at(hdr: str, vc: float, vdd: float, work: Path, tag: str, tend: float = 120e-9) -> float:
    wr = work / f"{tag}.dat"
    deck = (f"* f at vctrl\n{hdr}{BENCH.replace('VCTRL', repr(vc))}.save v(xdut.vco_out)\n"
            f".control\nset noaskquit\ntran {TSTEP} {tend} 0 {TSTEP}\n"
            f"wrdata {wr} v(xdut.vco_out)\n.endc\n.end\n")
    ngspice(deck, work, tag, 1800)
    rows = read_wr(wr)
    tr = rises([r[0] for r in rows], [r[1] for r in rows], vdd / 2, 60e-9)
    return (len(tr) - 1) / (tr[-1] - tr[0]) if len(tr) >= 3 else 0.0


def find_vctrl(hdr, vdd, work, guess) -> dict:
    pts = []
    a, b = guess - 0.1, guess + 0.1
    fa, fb = freq_at(hdr, a, vdd, work, "fa"), freq_at(hdr, b, vdd, work, "fb")
    pts += [(a, fa), (b, fb)]
    for it in range(6):
        if fb == fa:
            break
        c = b + (F_TARGET - fb) * (b - a) / (fb - fa)
        c = min(max(c, 0.3), vdd)
        fc = freq_at(hdr, c, vdd, work, f"fs{it}")
        pts.append((c, fc))
        a, fa, b, fb = b, fb, c, fc
        if abs(fc / F_TARGET - 1) < 5e-4:
            break
    near = sorted(pts, key=lambda p: abs(p[1] - F_TARGET))[:2]
    (x1, y1), (x2, y2) = sorted(near)
    kv = (y2 - y1) / (x2 - x1) if x2 != x1 else float("nan")
    return {"vctrl_v": b, "f_hz": fb, "kvco_local_hz_per_v": kv, "search": pts}


def resistances(hdr: str, res: list[dict], work: Path) -> dict:
    lines = []
    for i, r in enumerate(res):
        lines.append(f"vr{i} ra{i} 0 dc 1\nxr{i} ra{i} 0 0 ppolyf_u r_width={r['r_width']} "
                     f"r_length={r['r_length']}")
    deck = (f"* R values\n{hdr}" + "\n".join(lines) + "\n.control\nset noaskquit\nop\n"
            + "".join(f"print -1/i(vr{i}) > {work}/r{i}.txt\n" for i in range(len(res)))
            + ".endc\n.end\n")
    ngspice(deck, work, "res", 600)
    out = {}
    for i, r in enumerate(res):
        txt = (work / f"r{i}.txt").read_text()
        out[r["name"]] = float(re.findall(r"=\s*([-+0-9.eE]+)", txt)[-1])
    return out


def op_gm(hdr: str, vc: float, vdd: float, mos: list[dict], work: Path) -> dict:
    """Per MOS: gm+gds and the terminal voltages (d, g, s, b), for the ring
    devices at their ring node's vdd/2 crossings, for the rest averaged over
    the last 100 ns of a noiseless T_SETTLE transient."""
    vecs = []
    for m in mos:
        n = m["name"].lower()
        vecs += [f"@m.xdut.{n}.m0[gm]", f"@m.xdut.{n}.m0[gds]"]
    term = sorted({m[k] for m in mos for k in ("d", "g", "s", "b")} | RING)
    nodes = [f"v(xdut.{t})" for t in term]
    wr = work / "gm.dat"
    names = nodes + vecs
    deck = (f"* gm\n{hdr}{BENCH.replace('VCTRL', repr(vc))}"
            + "".join(f".save {v}\n" for v in names)
            + f".control\nset noaskquit\ntran {TSTEP} {T_SETTLE} {T_SETTLE - 100e-9} {TSTEP}\n"
            f"linearize\nwrdata {wr} {' '.join(names)}\n.endc\n.end\n")
    ngspice(deck, work, "gm", 3600)
    rows = read_wr(wr)
    wr.unlink(missing_ok=True)
    cols = list(zip(*rows))  # wrdata writes a "t v" pair per vector
    t = cols[0]
    val = {nm: cols[2 * k + 1] for k, nm in enumerate(names)}
    win = list(range(len(t)))
    xs = {}
    for r in sorted(RING):
        v = val[f"v(xdut.{r})"]
        xs[r] = [i for i in win[1:] if (v[i - 1] - vdd / 2) * (v[i] - vdd / 2) <= 0]
    out = {}
    for m in mos:
        n = m["name"].lower()
        g = [a + b for a, b in zip(val[f"@m.xdut.{n}.m0[gm]"], val[f"@m.xdut.{n}.m0[gds]"])]
        idx = xs[m["ring_out"]] if m["ring_out"] and xs[m["ring_out"]] else win
        bias = {k: sum(val[f"v(xdut.{m[k]})"][i] for i in idx) / len(idx) for k in "dgsb"}
        out[m["name"]] = {"g": sum(abs(g[i]) for i in idx) / len(idx), "bias": bias}
    return out


def device_noise(hdr: str, mos: list[dict], op: dict, work: Path) -> dict:
    """BSIM4 drain-current noise of each instance at its bias (a copy with
    ideal sources on its terminals, .noise of the drain current): white PSD
    (at 1 GHz) and the 1/f coefficient K (S = K / f, from 1 kHz), A^2/Hz."""
    lines, ctl = [], []
    for i, m in enumerate(mos):
        b = op[m["name"]]["bias"]
        geo = " ".join(f"{k}={m[k]}" for k in ("w", "l") if m.get(k))
        extra = " ".join(t for t in m["line"].split() if t.split("=")[0] in ("ad", "as", "pd", "ps", "nf", "m"))
        lines += [f"vd{i} d{i} 0 dc {b['d']}", f"vg{i} g{i} 0 dc {b['g']} ac 1",
                  f"vs{i} s{i} 0 dc {b['s']}", f"vb{i} b{i} 0 dc {b['b']}",
                  f"h{i} o{i} 0 vd{i} 1", f"xm{i} d{i} g{i} s{i} b{i} {m['model']} {geo} {extra}"]
        ctl += [f"noise v(o{i}) vg{i} lin 2 1e3 1e9", f"setplot noise{2 * i + 1}",
                f"print onoise_spectrum > {work}/dn{i}.txt"]
    deck = (f"* device noise\n{hdr}" + "\n".join(lines) + "\n.control\nset noaskquit\n"
            + "\n".join(ctl) + "\n.endc\n.end\n")
    ngspice(deck, work, "devnoise", 1800)
    out = {}
    for i, m in enumerate(mos):
        f = work / f"dn{i}.txt"
        v = [float(x) for x in re.findall(r"^\s*\d+\s+\S+\s+([-+0-9.eE]+)", f.read_text(), re.M)] \
            if f.is_file() else []
        if len(v) == 2:
            w = v[1] ** 2
            out[m["name"]] = {"white": w, "kf": max(v[0] ** 2 - w, 0.0) * 1e3}
        f.unlink(missing_ok=True)
    return out


V2I_NETS = {"vi", "vs", "vcl", "vbp_vco", "vbn_vco"}


def group(m: dict) -> str:
    """Which block a MOS instance belongs to, from its nets."""
    nets = {base(m[k]) for k in ("d", "g", "s")}
    if m["ring_out"]:
        return "ring_inverter"
    if base(m["g"]) in ("vbp_vco", "vbn_vco") and not nets & {"vbp_vco", "vbn_vco"} - {base(m["g"])}:
        return "ring_starve"
    if nets & V2I_NETS:
        return "v2i_and_mirror"
    if nets & {"nb", "vco_out", "vco_div2", "dqb", "dqn", "dx", "dy", "da", "db", "dc"} or \
            any(base(n).startswith(("a_18352", "a_21", "a_22")) for n in nets):
        return "buffer_divider"
    return "bias_cp_other"


def noise_lines(mos, res, dn, rval, temp_k, flicker=True, white=True) -> str:
    """One trnoise current source per generator, drain to source (MOS) or
    across the resistor. White: NA = sqrt(S_w / (2 NT)) (linear-interpolated
    samples: one-sided S(0) = 2 NA^2 NT, checked by a periodogram of the
    source alone). 1/f: trnoise(.. 1 NAMP) gives S = NAMP^2 / (2 f) one-sided
    (same check, NT-independent), so NAMP = sqrt(2 K)."""
    out = []
    for i, m in enumerate(mos):
        d = dn.get(m["name"])
        if not d or d["white"] <= 0 or group(m) == "buffer_divider":
            continue  # switching rail to rail, an averaged bias means nothing: bounded in RESULT.md
        na = math.sqrt(d["white"] / (2 * NT)) if white else 0.0
        fl = f"1 {math.sqrt(2 * d['kf']):.4e}" if flicker and d["kf"] > 0 else "0 0"
        out.append(f"inm{i} xdut.{m['d']} xdut.{m['s']} dc 0 trnoise({na:.4e} {NT} {fl})")
    for i, r in enumerate(res):
        if not white:
            break
        if base(r["a"]) == "vctrl" or base(r["b"]) == "vctrl":
            continue  # shorted by the ideal vctrl source; closed-loop model
        na = math.sqrt(4 * KB * temp_k / rval[r["name"]] / (2 * NT))
        out.append(f"inr{i} xdut.{r['a']} xdut.{r['b']} dc 0 trnoise({na:.4e} {NT} 0 0)")
    return "\n".join(out) + "\n"


def crossings(t, v, th: float, t0: float) -> list[float]:
    """Rising th crossings after t0, a cubic through the 4 points around each."""
    import numpy as np
    idx = np.where((v[:-1] < th) & (v[1:] >= th) & (t[1:] > t0))[0]
    out = []
    for i in idx:
        if i < 1 or i + 3 > len(t):
            continue
        sl = slice(i - 1, i + 3)
        out.append(float(t[i] + np.polyfit(v[sl] - th, t[sl] - t[i], 3)[-1]))
    return out


def noisy(hdr, vc, vdd, nl, work, tag, tend, seed, timeout) -> dict:
    """Crossing times on ring node r5 and on vco_out."""
    import numpy as np
    wr = work / f"{tag}.dat"
    deck = (f"* noisy\n{hdr}{BENCH.replace('VCTRL', repr(vc))}{nl}.save v(xdut.vco_out) v(xdut.r5)\n"
            f".control\nset noaskquit\nset rndseed={seed}\nsetseed {seed}\n"
            f"tran {TSTEP} {tend} 0 {TSTEP}\nwrdata {wr} v(xdut.vco_out) v(xdut.r5)\n.endc\n.end\n")
    ngspice(deck, work, tag, timeout)
    d = np.loadtxt(wr)
    wr.unlink(missing_ok=True)
    return {"vco_out": crossings(d[:, 0], d[:, 1], vdd / 2, T_SETTLE),
            "r5": crossings(d[:, 0], d[:, 3], vdd / 2, T_SETTLE)}


def residual_periods(tr: list[float]):
    """Periods with their mean, linear drift and period-2 pattern removed."""
    import numpy as np
    per = np.diff(np.array(tr))
    k = np.arange(len(per))
    line = np.polyfit(k, per, 1)
    r = per - np.polyval(line, k)
    alt = (r[::2].mean() - r[1::2].mean()) / 2
    r = r - np.where(k % 2 == 0, r[::2].mean(), r[1::2].mean())
    return per, r, float(line[0]), float(alt)


def stats(tr: list[float]) -> dict:
    """sigma_t: rms period deviation, the deterministic period-2 alternation
    (reported apart as alternation_amp_s) and drift removed."""
    import numpy as np
    per, r, slope, alt = residual_periods(tr)
    n = len(per)
    acc = {}
    for k in (1, 2, 4, 8, 16, 32, 64):
        if n > 3 * k:
            d = np.convolve(r, np.ones(k), "valid")
            acc[k] = float(np.sqrt((d * d).mean()))
    c2c = np.diff(r)
    return {"periods": n, "mean_period_s": float(per.mean()), "f_hz": float(1 / per.mean()),
            "drift_s_per_period": slope, "alternation_amp_s": abs(alt),
            "sigma_t_s": float(np.sqrt((r * r).sum() / (n - 4))),
            "sigma_t_raw_s": float(per.std(ddof=1)),
            "c2c_over_sqrt2_s": float(np.sqrt((c2c * c2c).mean() / 2)),
            "accumulated_rms_s": acc}


def periodogram(tr_list: list[list[float]], f0: float) -> list[tuple[float, float]]:
    """Averaged periodogram of the time error x_k (detrended), as L(f) dBc/Hz,
    one point per octave band."""
    import numpy as np
    specs = []
    for tr in tr_list:
        x = np.cumsum(residual_periods(tr)[1])
        x = x - np.polyval(np.polyfit(np.arange(len(x)), x, 1), np.arange(len(x)))
        n = len(x)
        w = np.hanning(n)
        X = np.fft.rfft(x * w)
        fs = f0
        sx = 2 * np.abs(X) ** 2 / (fs * (w ** 2).sum())  # one-sided S_x, s^2/Hz
        specs.append(sx)
    m = min(len(s) for s in specs)
    sx = np.mean([s[:m] for s in specs], axis=0)
    f = np.fft.rfftfreq(len(tr_list[0]) - 1, 1 / f0)[:m]
    lf = (2 * np.pi * f0) ** 2 * sx / 2  # S_phi/2 = L
    out = []
    lo = 4 * f[1]
    while lo * 2 < f0 / 2:
        sel = (f >= lo) & (f < 2 * lo)
        if sel.any():
            out.append((float(np.sqrt(lo * 2 * lo)), float(10 * np.log10(lf[sel].mean()))))
        lo *= 2
    return out


def closed_loop(a2: float, b3: float, f0: float, kvco: float, temp_k: float, loop: dict) -> dict:
    """Linear continuous-time model. L_vco(f) = a2 / f^2 + b3 / f^3 (the fit to the simulated free-running VCO);
    R1 noise: v_n^2 = 4kTR1 in series with C1, into vctrl."""
    import numpy as np
    icp, r1, c1, c2, pn, fref = (loop[k] for k in ("icp_a", "r1_ohm", "c1_f", "c2_f", "pn", "f_ref_hz"))
    kv = 2 * np.pi * kvco  # rad/s/V
    f = np.logspace(3, np.log10(f0 / 2), 4000)
    s = 2j * np.pi * f
    z = (1 + s * r1 * c1) / (s * (c1 + c2) * (1 + s * r1 * c1 * c2 / (c1 + c2)))
    hol = icp / (2 * np.pi) * kv / s * z / pn
    eh = 1 / (1 + hol)                       # VCO noise -> output (high pass)
    lvco = a2 / f ** 2                       # white (1/f^2) part, single sideband
    lvco_fl = b3 / f ** 3                    # 1/f^3 (flicker) part
    # R1: noise voltage in series with C1; at vctrl: v_n * Zc2-divider
    zc1, zc2 = 1 / (s * c1), 1 / (s * c2)
    vctrl_per_vn = zc2 / (r1 + zc1 + zc2)
    # phase out per volt on vctrl inside the loop: (Kvco/s) * 1/(1+Hol)
    phi_r1 = np.abs(vctrl_per_vn * kv / s * eh) ** 2 * 4 * KB * temp_k * r1 / 2  # L = S_phi/2
    fc = f[np.argmin(np.abs(np.abs(hol) - 1))]
    out_total = (lvco + lvco_fl) * np.abs(eh) ** 2 + phi_r1

    def rms_jit(lf, f1, f2):
        sel = (f >= f1) & (f <= f2)
        return float(np.sqrt(2 * np.trapezoid(lf[sel], f[sel])) / (2 * np.pi * f0))

    def at(lf, fx):
        return float(10 * np.log10(np.interp(fx, f, lf)))
    pts = (1e4, 1e5, 1e6, 1e7)
    return {
        "label": "LINEAR MODEL (continuous-time, no sampling, no ref/PFD/CP noise), not simulated",
        "crossover_hz": float(fc), "kvco_hz_per_v": kvco, "loop": loop,
        "L_vco_free_dbc_hz": {f"{int(x)}": at(lvco + lvco_fl, x) for x in pts},
        "L_out_closed_dbc_hz": {f"{int(x)}": at(out_total, x) for x in pts},
        "L_out_r1_only_dbc_hz": {f"{int(x)}": at(phi_r1, x) for x in pts},
        "rms_jitter_10k_fref2_s": rms_jit(out_total, 1e4, fref / 2),
        "rms_jitter_10k_50M_s": rms_jit(out_total, 1e4, f0 / 2),
        "rms_jitter_vco_part_10k_50M_s": rms_jit((lvco + lvco_fl) * np.abs(eh) ** 2, 1e4, f0 / 2),
        "rms_jitter_vco_white_part_10k_50M_s": rms_jit(lvco * np.abs(eh) ** 2, 1e4, f0 / 2),
        "rms_jitter_vco_flicker_part_10k_50M_s": rms_jit(lvco_fl * np.abs(eh) ** 2, 1e4, f0 / 2),
        "rms_jitter_r1_part_10k_50M_s": rms_jit(phi_r1, 1e4, f0 / 2),
        "free_running_accum_note": "free-running VCO jitter grows as kappa*sqrt(t) without bound",
    }


def corner_loop(cn: str, d: dict) -> dict:
    """The loop at this corner: Icp from reports/recorded/pex_pvt.json (mean of
    up and down, extracted, code 00), R1 = the 4 extracted segments, C1, C2
    at the corner's MOS-cap factor (1, 1.1 ss, 0.9 ff)."""
    m = json.loads((WS / "reports" / "recorded" / "pex_pvt.json").read_text())["facts"]["measured"][cn]
    r1 = sum(d["noise_sources"]["resistors_ohm"][x] for x in R1_SEGMENTS)
    k = {"ss": 1.1, "ff": 0.9}.get(cn[:2], 1.0)
    return dict(LOOP, icp_a=(m["icp_up_code00_ua"] + m["icp_dn_code00_ua"]) / 2 * 1e-6, r1_ohm=r1,
                c1_f=LOOP["c1_f"] * k, c2_f=LOOP["c2_f"] * k)


def analyse(cn: str, d: dict) -> None:
    """L_vco = a2 / f^2 + b3 / f^3 and the closed-loop model, from recorded values.
    b3: the flicker-only runs (no white source, so measured well above the
    numerical floor), f^3 L = b3 + c2 f. a2: the full runs' bands below f0/8 less b3's share, from
    1.5 MHz up (the lowest band is the most detrended)."""
    import numpy as np
    f0 = sum(r["f_hz"] for r in d["full"]) / len(d["full"])
    fl = d.get("flicker_only")
    b3 = 0.0
    if fl:
        ff = np.array([b[0] for b in fl["L_dbc_hz"]])
        ll = 10 ** (np.array([b[1] for b in fl["L_dbc_hz"]]) / 10)
        sel = ff <= f0 / 8
        fl["slope_db_per_decade"] = float(np.polyfit(np.log10(ff[sel]), 10 * np.log10(ll[sel]), 1)[0])
        # f^3 L = b3 + c2 f: 1/f noise near DC gives 1/f^3, folded around the
        # carrier it gives 1/f^2 (c2, already inside the full runs' a2). Relative
        # error of a band ~ 1/sqrt(bins), bins ~ f: iteratively weighted.
        x, y = ff[sel], ll[sel] * ff[sel] ** 3
        b3, c2 = float(y.mean()), 0.0
        for _ in range(5):
            w = x / np.maximum(b3 + c2 * x, 1e-30) ** 2
            A = np.vstack([np.ones_like(x), x]).T
            c2_b = np.linalg.lstsq(A * np.sqrt(w)[:, None], y * np.sqrt(w), rcond=None)[0]
            b3, c2 = max(float(c2_b[0]), 0.0), max(float(c2_b[1]), 0.0)
        fl["fit"] = {"b3_hz2": b3, "c2_hz": c2, "f3L_per_band": [float(v) for v in y]}
    bands = [b for b in d["L_vco_periodogram_dbc_hz"] if 1.5e6 <= b[0] <= f0 / 8]
    a2s = [max(10 ** (lv / 10) - b3 / fx ** 3, 0.0) * fx * fx for fx, lv in bands]
    a2 = sum(a2s) / len(a2s)
    # the same a2 from the slope of the accumulated-jitter variance, lags >= 4
    acc = [(int(k), v ** 2) for r in d["full"] for k, v in r["accumulated_rms_s"].items() if 4 <= int(k) <= 32]
    xs, ys = np.array([k for k, _ in acc]), np.array([v for _, v in acc])
    a2_acc = float(np.polyfit(xs, ys, 1)[0] * f0 ** 3)
    d["L_vco_fit"] = {"a2_hz": a2, "b3_hz2": b3, "a2_from_sigma_t_hz": f0 ** 3 * d["sigma_t_full_net_of_floor_s"] ** 2,
                      "a2_from_accumulated_slope_hz": a2_acc, "a2_per_band_hz": a2s,
                      "flicker_corner_hz": b3 / a2 if a2 > 0 else None,
                      "L_1MHz_dbc_hz": 10 * math.log10(a2 / 1e12 + b3 / 1e18)}
    search = sorted(d["op"]["search"])
    kv = (search[-1][1] - search[0][1]) / (search[-1][0] - search[0][0])  # the +-100 mV points
    d["kvco_100mhz_hz_per_v"] = kv
    temp_k = float(d["temp_c"]) + 273.15
    loop = corner_loop(cn, d)
    d["closed_loop"] = closed_loop(a2, b3, f0, kv, temp_k, loop)
    d["closed_loop_no_flicker"] = closed_loop(a2, 0.0, f0, kv, temp_k, loop)
    d["closed_loop_paper_kvco_116"] = closed_loop(a2, b3, f0, 116e6, temp_k, loop)


def pooled(runs: list[dict]) -> float:
    n = sum(r["periods"] for r in runs)
    return math.sqrt(sum(r["sigma_t_s"] ** 2 * r["periods"] for r in runs) / n)


def main(argv=None) -> int:
    global T_SETTLE
    ap = argparse.ArgumentParser()
    ap.add_argument("--corners", nargs="+", default=["tt_27c", "ss_125c_vm10"])
    ap.add_argument("--netlist", type=Path, default=DEF_NETLIST)
    ap.add_argument("--seeds", type=int, default=3, help="white + 1/f runs")
    ap.add_argument("--white-seeds", type=int, default=1, help="white-only runs")
    ap.add_argument("--periods", type=int, default=520)
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--floor-periods", type=int, default=150)
    ap.add_argument("--timeout", type=float, default=8 * 3600)
    ap.add_argument("--out", type=Path, default=OUT_JSON)
    ap.add_argument("--settle", type=float, default=T_SETTLE)
    ap.add_argument("--only-flicker", action="store_true", help="corners already run: add the flicker-only runs")
    ap.add_argument("--flicker-seeds", type=int, default=1)
    ap.add_argument("--recalc", action="store_true", help="no sims: redo the fits and the model from the json")
    a = ap.parse_args(argv)
    T_SETTLE = a.settle
    spec = speclib.load_spec(WS / "spec" / "spec.yaml")
    sweep, _ = sim_run.spec_sweep(WS)
    by = {c["name"]: c for c in sweep}
    mos, res = parse_devices(a.netlist)
    guess = {"ff_pss": 2.203, "ff_m40c_vm10": 1.446, "ff_125c_vp10": 1.772, "ss_m40c_vm10": 1.814}
    prev = json.loads(a.out.read_text()) if a.out.is_file() else {}
    results = dict(prev.get("corners", {}))
    pool = ThreadPoolExecutor(max(1, a.jobs))
    def save():
        for cn, d in results.items():
            analyse(cn, d)
        doc = {"script": "jitter/jitter_pex.py", "netlist": prev.get("netlist") or str(a.netlist),
               "netlist_sha256": hashlib.sha256(a.netlist.read_bytes()).hexdigest(),
               "ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "corners": results}
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps(doc, indent=1))
    if a.recalc:
        save()
        return 0
    setup, jobs, fljobs = {}, {}, {}
    for cn in a.corners:
        subs = sim_run.build_subs(sim_run.toolchain_root(sim_run.EDA_BIN), a.netlist, by[cn],
                                  spec["supply"]["vdd"], sim_run.load_sizing(WS))
        vdd, temp_k = float(subs["VDD"]), float(subs["TEMP_C"]) + 273.15
        hdr = header(subs, a.netlist)
        work = WORK / cn
        opf = work / "op.json"  # the vctrl search is the same every run: cached
        op = json.loads(opf.read_text()) if opf.is_file() else find_vctrl(hdr, vdd, work, guess.get(cn, 1.8))
        opf.write_text(json.dumps(op))
        print(cn, "vctrl", op["vctrl_v"], op["f_hz"], flush=True)
        devf = work / "devices.json"  # so are R, the bias and the device noise
        if devf.is_file():
            rval, g, dn = json.loads(devf.read_text())
        else:
            rval = resistances(hdr, res, work)
            g = op_gm(hdr, op["vctrl_v"], vdd, mos, work)
            dn = device_noise(hdr, mos, g, work)
            devf.write_text(json.dumps([rval, g, dn]))
        nl_full = noise_lines(mos, res, dn, rval, temp_k, flicker=True)
        nl_white = noise_lines(mos, res, dn, rval, temp_k, flicker=False)
        nl_fl = noise_lines(mos, res, dn, rval, temp_k, flicker=True, white=False)
        tend = T_SETTLE + (a.periods + 2) / op["f_hz"]
        tfl = T_SETTLE + (a.floor_periods + 2) / op["f_hz"]
        vc = op["vctrl_v"]
        setup[cn] = (subs, vdd, temp_k, op, rval, g, dn)
        fljobs[cn] = [(hdr, vc, vdd, nl_fl, work, f"flicker{s}", tend, 200 + s, a.timeout)
                      for s in range(1, a.flicker_seeds + 1)]
        if a.only_flicker:
            jobs[cn] = []
            continue
        jobs[cn] = [(hdr, vc, vdd, nl_full, work, f"full{s}", tend, s, a.timeout)
                    for s in range(1, a.seeds + 1)]
        jobs[cn] += [(hdr, vc, vdd, nl_white, work, f"white{s}", tend, 100 + s,
                                 a.timeout) for s in range(1, a.white_seeds + 1)]
        jobs[cn] += [(hdr, vc, vdd, "", work, "floor", tfl, 1, a.timeout)]
    jobs = {cn: [pool.submit(noisy, *args) for args in v] for cn, v in jobs.items()}
    fljobs = {cn: [pool.submit(noisy, *args) for args in v] for cn, v in fljobs.items()}
    t0 = time.monotonic()
    for cn in a.corners:
        subs, vdd, temp_k, op, rval, g, dn = setup[cn]
        trf = [j.result() for j in fljobs[cn]]
        fl_doc = {"runs": [stats(t["r5"]) for t in trf], "L_dbc_hz": periodogram([t["r5"] for t in trf], F_TARGET),
                  "note": "1/f sources only (BSIM K per device, not the buffer or divider), no white source"}
        if a.only_flicker:
            results[cn]["flicker_only"] = fl_doc
            save()
            continue
        trs = [j.result() for j in jobs[cn]]
        tr_full, tr_white, tr_floor = trs[:a.seeds], trs[a.seeds:-1], trs[-1]
        full = [stats(t["r5"]) for t in tr_full]
        white = [stats(t["r5"]) for t in tr_white]
        floor = stats(tr_floor["r5"])
        full_out = [stats(t["vco_out"]) for t in tr_full]
        floor_out = stats(tr_floor["vco_out"])
        f0 = sum(r["f_hz"] for r in full) / len(full)
        sig_full, sig_white = pooled(full), (pooled(white) if white else None)
        fl2 = floor["sigma_t_s"] ** 2
        sig_full_net = math.sqrt(max(sig_full ** 2 - fl2, 0))
        bands = periodogram([t["r5"] for t in tr_full], f0)
        bands_w = periodogram([t["r5"] for t in tr_white], f0) if white else []
        grp, kt4 = {}, 4 * KB * temp_k
        for m in mos:
            k = group(m)
            e = grp.setdefault(k, {"devices": 0, "white_a2_hz": 0.0, "kf_a2": 0.0,
                                   "4kT_gm_gds_a2_hz": 0.0})
            d = dn.get(m["name"], {"white": 0.0, "kf": 0.0})
            e["devices"] += 1
            e["white_a2_hz"] += d["white"]
            e["kf_a2"] += d["kf"]
            e["4kT_gm_gds_a2_hz"] += kt4 * g[m["name"]]["g"]
        for e in grp.values():
            e["gamma_eff_vs_gm_gds"] = e["white_a2_hz"] / e["4kT_gm_gds_a2_hz"] if e["4kT_gm_gds_a2_hz"] else None
            e["flicker_corner_hz"] = e["kf_a2"] / e["white_a2_hz"] if e["white_a2_hz"] else None
        results[cn] = {
            "vdd": vdd, "temp_c": subs["TEMP_C"], "op": op,
            "noise_sources": {"mos": len(mos), "resistors": len(res), "nt_s": NT, "tstep_s": TSTEP,
                              "mos_noise": "BSIM4 drain-current noise of each instance at its bias "
                                           "(.noise of a copy): white + 1/f",
                              "by_group": grp, "resistors_ohm": rval},
            "flicker_only": fl_doc,
            "floor_noiseless": floor, "floor_noiseless_vco_out": floor_out,
            "full": full, "full_vco_out": full_out, "white_only": white,
            "sigma_t_vco_out_s": pooled(full_out),
            "L_vco_periodogram_white_only_dbc_hz": bands_w,
            "sigma_t_full_s": sig_full, "sigma_t_full_net_of_floor_s": sig_full_net,
            "sigma_t_white_only_s": sig_white,
            "sigma_t_rel_stat_err": 1 / math.sqrt(2 * sum(r["periods"] for r in full)),
            "L_vco_periodogram_dbc_hz": bands,
            "wall_s": time.monotonic() - t0,
        }
        save()
    return 0


if __name__ == "__main__":
    sys.exit(main())
