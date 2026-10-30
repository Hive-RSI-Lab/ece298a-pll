"""Draw the review page's figures from what the repository records.

    uv run --python 3.12 --no-project --with gdstk --with matplotlib python docs/review/make_figures.py

Needs no EDA tools: it reads the analog macro's GDS, the post-layout corner
results (blocks/pll/analog/reports/recorded/pex_pvt.json), the analog spec's
post-layout bounds and the co-simulation's measures, and writes PNGs next to
this file. Rerun it after any of those change.
"""
from __future__ import annotations

import json
from pathlib import Path

import gdstk
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.collections import PolyCollection  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
BLOCK = ROOT / "blocks" / "pll"
OUT = Path(__file__).resolve().parent

INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df"
BLUE, ORANGE = "#2a78d6", "#eb6834"
plt.rcParams.update({
    "font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False,
    "axes.spines.right": False, "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": 0.6, "axes.axisbelow": True, "savefig.dpi": 110,
    "figure.facecolor": "white"})

# gf180mcuD drawing layers (GDS layer, datatype 0) in stacking order
LAYERS = [
    ("Nwell", 21, "#c9c3e6", 0.5), ("Comp (diffusion)", 22, "#9fd6a8", 0.7),
    ("Poly2", 30, "#e2554b", 0.8), ("Metal1", 34, "#5b8fd9", 0.45),
    ("Metal2", 36, "#d9a13b", 0.45), ("Metal3", 42, "#57b3a0", 0.4),
    ("Metal4", 46, "#a46ad1", 0.35), ("MIM top (FuseTop)", 75, "#6b6b6b", 0.35),
    ("Metal5", 81, "#e87ba4", 0.3)]


def layout() -> None:
    lib = gdstk.read_gds(str(BLOCK / "analog" / "layout" / "pll_analog.gds"))
    top = next(c for c in lib.top_level() if c.name == "pll_analog")
    polys = top.get_polygons()
    abstract = json.loads((BLOCK / "analog" / "layout" /
                           "pll_analog.abstract.json").read_text())
    fig, ax = plt.subplots(figsize=(7.6, 8.0))
    for name, layer, colour, alpha in LAYERS:
        pts = [p.points for p in polys if p.layer == layer and p.datatype == 0]
        if pts:
            ax.add_collection(PolyCollection(pts, facecolors=colour, edgecolors="none",
                                             alpha=alpha, label=name))
    bottom = sorted((p for p in abstract["pins"] if p["y"] < 0), key=lambda p: p["x"])
    x_right = abstract["bbox_um"][2]
    for pin in abstract["pins"]:
        low = pin in bottom
        ax.annotate(pin["name"], (pin["x"], pin["y"]), fontsize=7, color=INK,
                    xytext=(4 if pin["x"] > x_right - 2 else 0,
                            -9 - 9 * bottom.index(pin) if low else 0),
                    textcoords="offset points", ha="left" if pin["x"] > x_right - 2 or low else "center",
                    va="center")
    x0, y0, x1, y1 = abstract["bbox_um"]
    ax.set_xlim(x0 - 2, x1 + 22)
    ax.set_ylim(y0 - 42, y1 + 2)
    ax.set_aspect("equal")
    ax.grid(False)
    ax.set_xlabel("x (um)")
    ax.set_ylabel("y (um)")
    ax.set_title(f"pll_analog layout, {x1 - x0:.0f} x {y1 - y0:.0f} um "
                 "(ring VCO, bias, pump, R1, MOS-cap loop filter)",
                 fontsize=9, color=INK, loc="left")
    ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "analog-layout.png")
    plt.close(fig)


def tile() -> None:
    """The hardened tile, as committed in gds/ (Metal1-4 and the macro)."""
    gds = ROOT / "gds" / "tt_um_ihsan_sa_pll.gds"
    if not gds.is_file():
        return
    lib = gdstk.read_gds(str(gds))
    top = lib.top_level()[0]
    polys = top.get_polygons()
    fig, ax = plt.subplots(figsize=(8.4, 8.0))
    for name, layer, colour, alpha in LAYERS:
        if layer in (21, 22, 30):
            continue  # wells, COMP and poly hide the routing at this scale
        pts = [p.points for p in polys if p.layer == layer and p.datatype == 0]
        if pts:
            ax.add_collection(PolyCollection(pts, facecolors=colour, edgecolors="none",
                                             alpha=alpha, label=name))
    (x0, y0), (x1, y1) = top.bounding_box()
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect("equal")
    ax.grid(False)
    ax.set_xlabel("x (um)")
    ax.set_ylabel("y (um)")
    ax.set_title(f"{top.name}: the 1x2 tile, {x1 - x0:.0f} x {y1 - y0:.0f} um "
                 "(the analog macro in the middle, standard cells around it)",
                 fontsize=9, color=INK, loc="left")
    ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "tile.png")
    plt.close(fig)


def corners() -> None:
    rec = json.loads((BLOCK / "analog" / "reports" / "recorded" / "pex_pvt.json").read_text())
    # the bench's own bounds (spec.yaml post_layout_bounds, with the corners each is scored at)
    bounds = {b["measure"]: b for b in json.loads(
        (BLOCK / "analog" / "layout_ref" / "pll_analog_pex_pvt_tb.bounds.json").read_text())}
    meas = rec["facts"]["measured"]
    names = list(meas)
    rows = [("vco_kvco_mhz_per_v", "Kvco (MHz/V), mean over vctrl 0.3 .. vdd-0.3"),
            ("vco_fmax_tt_mhz", "VCO at vctrl = vdd - 0.3 V (MHz); the 200 MHz floor is scored at tt_27c only"),
            ("vco_f_vdd_mhz", "VCO ceiling, vctrl = vdd (MHz)"),
            ("icp_up_code00_ua", "pump UP current, code 00 (uA)")]
    fig, axes = plt.subplots(len(rows), 1, figsize=(9.6, 9.0), sharex=True)
    xs = range(len(names))
    for ax, (key, title) in zip(axes, rows):
        b = bounds.get(key, {})
        vals = [meas[c].get(key) for c in names]
        if "min" in b or "max" in b:
            lo = b.get("min", 0)
            hi = b.get("max", max(v for v in vals if v is not None) * 1.15)
            ax.axhspan(lo, hi, color=BLUE, alpha=0.08, lw=0)
            for edge in (b.get("min"), b.get("max")):
                if edge is not None:
                    ax.axhline(edge, color=BLUE, lw=1, ls="--")
        def out(v, c):
            if b.get("corners") and c not in b["corners"]:
                return not v
            return not v or v < b.get("min", float("-inf")) or v > b.get("max", float("inf"))
        ok = [(x, v) for x, v, c in zip(xs, vals, names) if not out(v, c)]
        bad = [(x, v) for x, v, c in zip(xs, vals, names) if out(v, c)]
        ax.scatter(*zip(*ok), s=22, color=BLUE, label="within its bound", zorder=3)
        if bad:
            ax.scatter(*zip(*bad), s=30, color=ORANGE, marker="D",
                       label="outside its bound (or no oscillation)", zorder=3)
        if key == "vco_fmax_tt_mhz":
            ax.axhline(100, color=MUTED, lw=1)
            ax.annotate("100 MHz nominal lock point", (-0.5, 100), fontsize=7,
                        color=INK2, ha="left", va="bottom")
        if key == "icp_up_code00_ua":
            ax.set_ylim(0, 40)
            for x, v in bad:
                if v > 40:
                    ax.annotate(f"{v:.0f} uA (second DC state)", (x, 39), fontsize=7,
                                color=INK2, ha="left", va="top")
        ax.set_title(title, fontsize=9, color=INK, loc="left")
    axes[0].legend(loc="upper right", fontsize=7, frameon=False)
    axes[-1].set_xticks(list(xs))
    axes[-1].set_xticklabels(names, rotation=70, fontsize=7)
    fig.suptitle("Post-layout benches on the extracted netlist, every corner the spec scores "
                 "(dashed: spec.yaml post_layout_bounds)", fontsize=10, color=INK, x=0.01,
                 ha="left")
    fig.tight_layout()
    fig.savefig(OUT / "post-layout-corners.png")
    plt.close(fig)


def cosim() -> None:
    m = json.loads((BLOCK / "reports" / "cosim_measures.json").read_text())
    t, v = zip(*m["vctrl_trace_us_v"])
    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.plot(t, v, color=BLUE, lw=2)
    for at, what in ((m["pll_en_rise_ns"] / 1e3, "pll_en rises"),
                     (m["lock_rise_ns"] / 1e3, f"lock rises ({m['lock_time_us']} us)")):
        ax.axvline(at, color=MUTED, lw=1, ls="--")
        ax.annotate(what, (at, max(v) * 0.15), xytext=(4, 0), textcoords="offset points",
                    fontsize=8, color=INK2)
    ax.set_xlabel("time (us)")
    ax.set_ylabel("vctrl (V)")
    op = m["operating_point"]
    ax.set_title(f"Co-simulation, digital RTL + transistor-level analog ({op['corner']}): "
                 f"{op['f_ref_hz'] / 1e6:g} MHz x {op['p_times_n']} locks at "
                 f"{m['vco_freq_hz'] / 1e6:.3f} MHz", fontsize=9, color=INK, loc="left")
    fig.tight_layout()
    fig.savefig(OUT / "cosim-lock.png")
    plt.close(fig)


if __name__ == "__main__":
    layout()
    tile()
    corners()
    cosim()
    print("wrote", ", ".join(p.name for p in sorted(OUT.glob("*.png"))))
