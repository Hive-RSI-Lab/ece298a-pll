"""Draw the paper's figures from what the repository records.

    uv run --python 3.12 --no-project --with gdstk --with matplotlib --with numpy \
        python docs/paper/make_figs.py

Reads only committed results (recorded gate reports, co-simulation measures,
the GDS files) plus docs/paper/data/, which docs/paper/sims/ writes from the
extracted netlist. No EDA tool is needed. Writes PDFs to docs/paper/figs/.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

import gdstk
import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.collections import PolyCollection  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
B = ROOT / "blocks" / "pll"
DATA = Path(__file__).resolve().parent / "data"
OUT = Path(__file__).resolve().parent / "figs"
OUT.mkdir(exist_ok=True)

INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df"
# categorical slots, fixed per entity (never by rank)
S = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
CORNERS4 = ["ff_pss", "ff_m40c_vm10", "ff_125c_vp10", "ss_m40c_vm10"]
CCOL = dict(zip(CORNERS4, S[:4]))
CCOL["tt_27c"] = S[6]
CCOL["ss_125c_vm10"] = S[5]
PROC = {"tt": S[0], "ss": S[1], "ff": S[2]}

plt.rcParams.update({
    "font.family": "serif", "font.size": 8, "axes.titlesize": 8,
    "axes.labelsize": 8, "legend.fontsize": 7, "xtick.labelsize": 7,
    "ytick.labelsize": 7, "axes.edgecolor": MUTED, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False,
    "axes.spines.right": False, "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": 0.5, "axes.axisbelow": True, "lines.linewidth": 1.4,
    "legend.frameon": False, "savefig.bbox": "tight", "pdf.fonttype": 42})
W1, W2 = 3.4, 7.0   # one column, two columns (in)


def load(p):
    return json.loads((ROOT / p).read_text())


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf")
    fig.savefig(OUT / f"{name}.png", dpi=160)
    plt.close(fig)


def pex():
    return load("blocks/pll/analog/reports/recorded/pex_pvt.json")["facts"]["measured"]


def sim_pvt():
    m = defaultdict(dict)
    for r in load("blocks/pll/analog/reports/recorded/gate-sim_pvt.json")["facts"]["results"]:
        m[r["corner"]].update(r["measures"])
    return m


def proc(c):
    return c[:2]


# ---------------------------------------------------------------- layout
LAYERS = [("Nwell", 21, "#c9c3e6", 0.5), ("Comp", 22, "#9fd6a8", 0.7),
          ("Poly2", 30, "#e2554b", 0.8), ("Metal1", 34, "#5b8fd9", 0.45),
          ("Metal2", 36, "#d9a13b", 0.45), ("Metal3", 42, "#57b3a0", 0.4),
          ("Metal4", 46, "#a46ad1", 0.3)]


def draw_gds(ax, path, cell, layers, flatten=True):
    lib = gdstk.read_gds(str(path))
    top = next(c for c in lib.top_level() if c.name == cell) if cell else lib.top_level()[0]
    polys = top.get_polygons()
    for name, layer, colour, alpha in layers:
        pts = [p.points for p in polys if p.layer == layer and p.datatype == 0]
        if pts:
            ax.add_collection(PolyCollection(pts, facecolors=colour, edgecolors="none",
                                             alpha=alpha, label=name))
    (x0, y0), (x1, y1) = top.bounding_box()
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect("equal")
    ax.grid(False)
    return top, (x0, y0, x1, y1)


def fig_layout():
    fig, (a, b) = plt.subplots(1, 2, figsize=(W2, 4.2), gridspec_kw={"width_ratios": [1, 2.1]})
    _, bb = draw_gds(a, B / "analog/layout/pll_analog.gds", "pll_analog", LAYERS)
    a.set_title(f"(a) analog macro, {bb[2]-bb[0]:.0f} x {bb[3]-bb[1]:.0f} um", loc="left")
    a.set_xlabel("x (um)")
    a.set_ylabel("y (um)")
    ann = [("ring VCO + TSPC /2", 0.80, 0.03), ("bias, buffers, enable", 0.5, 0.17),
           ("R1, R_V2I, bias R", 0.5, 0.42), ("charge pump", 0.5, 0.62),
           ("C1 (12 MOS units)", 0.5, 0.83), ("C2", 0.85, 0.97)]
    for t, fx, fy in ann:
        a.annotate(t, (bb[0] + fx * (bb[2] - bb[0]), bb[1] + fy * (bb[3] - bb[1])),
                   fontsize=6, ha="center", color=INK,
                   bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8))
    top, bb2 = draw_gds(b, ROOT / "gds/tt_um_ihsan_sa_pll.gds", None, LAYERS[3:])
    b.set_title(f"(b) the 1x2 Tiny Tapeout tile, {bb2[2]-bb2[0]:.0f} x {bb2[3]-bb2[1]:.0f} um",
                loc="left")
    b.set_xlabel("x (um)")
    b.legend(loc="upper left", bbox_to_anchor=(0, -0.12), ncol=4, fontsize=6)
    for t, xy in [("analog macro", (157, 175)), ("digital standard cells", (290, 160)),
                  ("digital standard cells", (45, 160))]:
        b.annotate(t, xy, ha="center", fontsize=7, color=INK,
                   bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85))
    save(fig, "layout")


# ---------------------------------------------------------------- VCO
def read_pts(corner):
    p = DATA / f"vco_{corner}.txt"
    if not p.exists():
        return None
    a = np.atleast_2d(np.loadtxt(p))
    a = a[a[:, 1] > 0]
    return a[np.argsort(a[:, 0])]


def fig_vco():
    fig, ax = plt.subplots(figsize=(W1, 2.5))
    for c in ["ff_m40c_vm10", "tt_27c", "ss_125c_vm10", "ff_pss"]:
        a = read_pts(c)
        if a is None:
            continue
        ax.plot(a[:, 0], a[:, 1] / 1e6, "-o", ms=3, color=CCOL[c], label=c)
    ax.axhline(100, color=MUTED, lw=0.8, ls="--")
    ax.text(0.32, 103, "100 MHz nominal point", fontsize=6, color=INK2)
    ax.set_xlabel("vctrl (V)")
    ax.set_ylabel("f(vco_out) (MHz)")
    ax.set_ylim(bottom=0)
    ax.legend(loc="upper left")
    save(fig, "vco_tuning")


def fig_tspc():
    p = DATA / "wave_tt_27c.txt"
    if not p.exists():
        return
    a = np.loadtxt(p)
    t = a[:, 0] * 1e9
    k = (t > 30) & (t < 60)
    fig, ax = plt.subplots(figsize=(W1, 1.9))
    ax.plot(t[k], a[k, 1], color=S[0], lw=1.1, label="vco_out (internal)")
    ax.plot(t[k], a[k, 2] - 4.0, color=S[1], lw=1.1, label="vco_div2 (pin), offset -4 V")
    ax.set_xlabel("time (ns)")
    ax.set_ylabel("V")
    ax.set_yticks([-4, -0.7, 0, 3.3])
    ax.set_yticklabels(["0", "3.3", "0", "3.3"])
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.28), ncol=2)
    save(fig, "tspc_wave")


# ---------------------------------------------------------------- corners
def order(m):
    return sorted(m, key=lambda c: ("tt ss ff".split().index(proc(c)) if proc(c) in ("tt", "ss", "ff") else 3, c))


def fig_corners():
    P, Q = pex(), sim_pvt()
    cs = order(P)
    x = np.arange(len(cs))
    fig, axs = plt.subplots(3, 1, figsize=(W2, 5.4), sharex=True)
    ax = axs[0]
    for i, c in enumerate(cs):
        m = P[c]
        ax.plot([i, i], [m["vco_f_lo_mhz"], m["vco_f_vdd_mhz"]], color=PROC.get(proc(c), MUTED),
                lw=3.5, solid_capstyle="round")
        ax.plot(i, Q[c]["vco_fmax_ff_mhz"], "_", color=INK2, ms=7, mew=1.2)
    ax.axhline(100, color=MUTED, ls="--", lw=0.8)
    ax.set_ylabel("VCO range (MHz)")
    ax.set_title("(a) post-layout VCO range, f(vctrl = 0.3 V) to f(vctrl = vdd); "
                 "tick: pre-layout f(vdd); dashed: 100 MHz", loc="left")
    ax = axs[1]
    ax.bar(x, [P[c]["vco_kvco_mhz_per_v"] for c in cs], width=0.7,
           color=[PROC.get(proc(c), MUTED) for c in cs])
    ax.axhline(30, color=S[7], ls="--", lw=0.8)
    ax.text(len(cs) - 0.5, 120, "dashed: post-layout floor 30 MHz/V", fontsize=6, ha="right", color=INK2)
    ax.set_ylabel("Kvco (MHz/V)")
    ax.set_title("(b) mean VCO gain over 0.3 .. vdd-0.3 V, extracted", loc="left")
    ax = axs[2]
    ax.plot(x, [Q[c]["ol_pm_pn16_nopad_pvt_deg"] for c in cs], "o", ms=4, color=INK2,
            mfc="white", label="schematic")
    ax.plot(x, [P[c]["ol_pm_pn16_nopad_pvt_deg"] for c in cs], "o", ms=4, color=S[0],
            label="extracted layout")
    ax.axhline(30, color=S[7], ls="--", lw=0.8)
    ax.set_ylabel("phase margin (deg)")
    ax.set_ylim(25, 60)
    ax.set_title("(c) loop phase margin at P N = 16 (no pad); floor 30 deg", loc="left")
    ax.legend(loc="lower right", ncol=2)
    ax.set_xticks(x)
    ax.set_xticklabels(cs, rotation=70, fontsize=6)
    save(fig, "corners")


def fig_cp():
    Q = sim_pvt()
    cs = order(Q)
    codes = ["icp_up_code00_ua", "icp_up_code01_ua", "icp_up_code10_ua", "icp_up_code11_ua"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(W2, 2.2))
    data = [[Q[c][k] for c in cs] for k in codes]
    for i, d in enumerate(data):
        a.plot(np.full(len(d), i) + np.random.default_rng(i).uniform(-0.15, 0.15, len(d)), d,
               "o", ms=3, color=S[0], alpha=0.6)
        a.plot([i - 0.25, i + 0.25], [np.median(d)] * 2, color=INK, lw=1.2)
    a.set_xticks(range(4))
    a.set_xticklabels(["00", "01", "10", "11"])
    a.set_xlabel("cp_trim code")
    a.set_ylabel("Icp (uA)")
    a.set_title("(a) pump current, 31 corners (bar: median)", loc="left")
    mm = [Q[c]["cp_updn_mismatch_pct"] for c in cs]
    ov = [Q[c]["cp_overlap_net_charge_fc"] for c in cs]
    b.plot(mm, ov, "o", ms=3.5, color=S[1])
    b.set_xlabel("UP/DN mismatch (%), bound 10")
    b.set_ylabel("net overlap charge (fC), bound 10")
    b.set_xlim(0, 10)
    b.set_ylim(0, 10)
    b.set_title("(b) pump matching, 31 corners", loc="left")
    save(fig, "chargepump")


# ---------------------------------------------------------------- loop model
def fig_bode():
    lm = load("blocks/pll/reports/loop_model.json")["point"]
    icp, kv, r1, c1, c2 = lm["icp_a"], lm["kvco_hz_per_v"] * 2 * np.pi, lm["r1_ohm"], lm["c1_f"], lm["c2_f"]
    f = np.logspace(3.5, 8, 600)
    s = 2j * np.pi * f
    z = (1 + s * r1 * c1) / (s * (c1 + c2) * (1 + s * r1 * c1 * c2 / (c1 + c2)))
    fig, (a, b) = plt.subplots(2, 1, figsize=(W1, 3.4), sharex=True)
    for i, pn in enumerate([8, 16, 40]):
        h = icp / (2 * np.pi) * kv * z / (s * pn)
        mag = 20 * np.log10(abs(h))
        ph = np.degrees(np.unwrap(np.angle(h)))
        k = np.argmin(abs(mag))
        a.semilogx(f, mag, color=S[i], label=f"P N = {pn}")
        b.semilogx(f, ph, color=S[i])
        b.plot(f[k], ph[k], "o", color=S[i], ms=4)
        b.annotate(f"PM {180 + ph[k]:.0f} deg", (f[k], ph[k]), xytext=(8, 10 - 11 * i),
                   textcoords="offset points", fontsize=6, color=INK2)
    a.axhline(0, color=MUTED, lw=0.8)
    a.axvline(6.25e6, color=MUTED, ls=":", lw=0.8)
    a.text(6.25e6 * 1.15, 55, "f_ref", fontsize=6, color=INK2)
    a.set_ylabel("|H| (dB)")
    a.set_ylim(-60, 80)
    a.legend(loc="lower left")
    b.set_ylabel("phase (deg)")
    b.set_xlabel("frequency (Hz)")
    b.set_ylim(-185, -95)
    save(fig, "bode")


# ---------------------------------------------------------------- co-simulation
def ms(kind, c):
    return load(f"blocks/pll/log/{kind}/{c}/measures.json")


def fig_lock():
    fig, (a, b) = plt.subplots(2, 1, figsize=(W1, 3.9), sharex=True)
    for c in CORNERS4:
        m = ms("cosim_corners_gl", c)
        tr = np.array(m["vctrl_trace_us_v"])
        a.plot(tr[:, 0], tr[:, 1], color=CCOL[c], lw=1.1, label=c)
        e = np.array(m["edge_times_ns"])
        fb = 1e3 / np.diff(e)                       # MHz, clk_fb
        b.plot(e[1:] / 1e3, fb * 16, color=CCOL[c], lw=1.1)
        a.plot(m["lock_rise_ns"] / 1e3, np.interp(m["lock_rise_ns"] / 1e3, tr[:, 0], tr[:, 1]),
               "v", color=CCOL[c], ms=5, mec="white")
    a.set_ylabel("vctrl (V)")
    a.legend(loc="lower right", fontsize=6)
    a.set_title("(a) control voltage; triangles: LOCK rises", loc="left")
    b.axhline(100, color=MUTED, ls="--", lw=0.8)
    b.set_ylabel("16 x f(clk_fb) (MHz)")
    b.set_xlabel("time (us)")
    b.set_ylim(0, 160)
    b.set_title("(b) VCO frequency seen through the feedback divider", loc="left")
    save(fig, "lock")


def fig_settle():
    fig, ax = plt.subplots(figsize=(W1, 2.3))
    x = np.arange(len(CORNERS4))
    for j, (kind, lab, col) in enumerate([("cosim_corners", "RTL digital (zero-delay PFD)", MUTED),
                                          ("cosim_corners_gl", "gate-level digital + SDF", S[0])]):
        v = [ms(kind, c)["vctrl_pp_last_10us_mv"] for c in CORNERS4]
        e = [ms(kind, c)["vctrl_pp_at_ref_edges_last_10us_mv"] for c in CORNERS4]
        ax.bar(x + (j - 0.5) * 0.38, v, 0.36, color=col, label=lab)
        ax.plot(x + (j - 0.5) * 0.38, e, "_", color=INK, ms=9, mew=1.4,
                label="sampled at reference edges" if j else None)
        for xi, vi in zip(x, v):
            ax.text(xi + (j - 0.5) * 0.38, vi + 0.6, f"{vi:.1f}", ha="center", fontsize=6, color=INK2)
    ax.axhline(20, color=S[7], ls="--", lw=0.8)
    ax.text(3.6, 20.6, "bound 20 mV", fontsize=6, ha="right", color=INK2)
    ax.set_xticks(x)
    ax.set_xticklabels(CORNERS4, fontsize=6)
    ax.set_ylabel("vctrl p-p, last 10 us (mV)")
    ax.set_ylim(0, 32)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), fontsize=6, ncol=2)
    save(fig, "settle")


# ---------------------------------------------------------------- timing
def fig_sta():
    t = load("blocks/pll/digital/reports/recorded/gate-timing.json")["facts"]["corners"]
    cs = sorted(t, key=lambda c: (c.split("_")[1], c))
    x = np.arange(len(cs))
    fig, ax = plt.subplots(figsize=(W1, 2.2))
    ax.bar(x - 0.2, [t[c]["setup_ws"] for c in cs], 0.38, color=S[0], label="setup")
    ax.bar(x + 0.2, [t[c]["hold_ws"] for c in cs], 0.38, color=S[1], label="hold")
    ax.set_xticks(x)
    ax.set_xticklabels([c.replace("_", " ", 1) for c in cs], rotation=60, fontsize=6)
    ax.set_ylabel("worst slack (ns)")
    ax.set_ylim(0, 4.6)
    ax.legend(loc="upper right", ncol=2)
    save(fig, "sta")


# ---------------------------------------------------------------- review follow-ups
CORNERS5 = CORNERS4 + ["tt_27c"]


def fig_pad():
    """The 5 pF ua[0] pad on vctrl: traces with the pad, and p-p/lock with and without."""
    fig, (a, b) = plt.subplots(2, 1, figsize=(W1, 3.9))
    for c in CORNERS5:
        m = ms("cosim_corners_gl_pad5pf", c)
        tr = np.array(m["vctrl_trace_us_v"])
        a.plot(tr[:, 0], tr[:, 1], color=CCOL[c], lw=1.0, label=c)
        if m.get("lock_rise_ns"):
            a.plot(m["lock_rise_ns"] / 1e3, np.interp(m["lock_rise_ns"] / 1e3, tr[:, 0], tr[:, 1]),
                   "v", color=CCOL[c], ms=5, mec="white")
    a.set_ylabel("vctrl (V)")
    a.set_xlabel("time (us)")
    a.legend(loc="lower right", fontsize=6)
    a.set_title("(a) with 5 pF on vctrl; triangles: LOCK rises", loc="left")
    x = np.arange(len(CORNERS4))
    for j, (kind, lab, col) in enumerate([("cosim_corners_gl", "no pad", MUTED),
                                          ("cosim_corners_gl_pad5pf", "5 pF pad", S[0])]):
        v = [ms(kind, c)["vctrl_pp_last_10us_mv"] for c in CORNERS4]
        lt = [ms(kind, c)["lock_time_us"] for c in CORNERS4]
        b.bar(x + (j - 0.5) * 0.38, v, 0.36, color=col, label=lab)
        for xi, vi, li in zip(x, v, lt):
            b.text(xi + (j - 0.5) * 0.38, vi + 0.6, f"{vi:.1f}\n{li:.1f}us", ha="center", fontsize=5,
                   color=INK2)
    b.axhline(20, color=S[7], ls="--", lw=0.8)
    b.set_xticks(x)
    b.set_xticklabels(CORNERS4, fontsize=6)
    b.set_ylabel("vctrl p-p, last 10 us (mV)")
    b.set_ylim(0, 30)
    b.legend(loc="upper right", fontsize=6, ncol=2)
    b.set_title("(b) ripple (label: p-p and lock time)", loc="left")
    fig.tight_layout()
    save(fig, "pad")


def fig_cov():
    """Divider steps at f_ref = 5 MHz: all corners, then ff_pss's 120 MHz step given longer."""
    fig, (ax, b) = plt.subplots(2, 1, figsize=(W1, 3.9))
    rep = load("blocks/pll/reports/recorded/cosim_cov.json")
    for r in rep["facts"]["results"]:
        c, m = r["corner"], r.get("measures") or {}
        tr = np.array(m["vctrl_trace_us_v"])
        ax.plot(tr[:, 0], tr[:, 1], color=CCOL.get(c, INK2), lw=1.0, label=c)
        for t in m.get("lock_rises_ns") or []:
            if t > 1:
                ax.plot(t / 1e3, np.interp(t / 1e3, tr[:, 0], tr[:, 1]), "v", color=CCOL.get(c, INK2),
                        ms=4, mec="white")
    plan = rep["facts"]["plan"]
    for (t, n) in plan["segments"]:
        f = 8 * n * plan["f_ref_hz"] / 1e6
        ax.axvline(t / 1e3, color=MUTED, ls=":", lw=0.8)
        ax.text(t / 1e3 + 0.4, 0.15, f"N={n}, {f:.0f} MHz", fontsize=6, color=INK2)
    ax.set_ylabel("vctrl (V)")
    ax.set_xlabel("time (us)")
    ax.set_ylim(0, 4.8)
    ax.legend(loc="upper center", fontsize=5, ncol=3)
    ax.set_title("(a) N = 1, 3, 2 at five corners", loc="left")
    cases = {r["case"]: r for r in load("blocks/pll/reports/recorded/cosim_cov_cases.json")["facts"]["results"]}
    for name, lab, col in (("ff_pss_step_120_long", "no pad", CCOL["ff_pss"]),
                           ("ff_pss_step_120_pad5p", "5 pF pad", S[6])):
        tr = np.array(cases[name]["measures"]["vctrl_trace_us_v"])
        b.plot(tr[:, 0], tr[:, 1], color=col, lw=1.0, label=lab)
    b.axvline(20, color=MUTED, ls=":", lw=0.8)
    b.set_ylabel("vctrl (V)")
    b.set_xlabel("time (us)")
    b.legend(loc="lower right", fontsize=6)
    b.set_title("(b) ff_pss, step to 120 MHz at 20 us", loc="left")
    fig.tight_layout()
    save(fig, "cov")


if __name__ == "__main__":
    for f in (fig_corners, fig_cp, fig_bode, fig_lock, fig_settle, fig_sta, fig_vco,
              fig_tspc, fig_layout, fig_pad, fig_cov):
        f()
        print("ok", f.__name__)
