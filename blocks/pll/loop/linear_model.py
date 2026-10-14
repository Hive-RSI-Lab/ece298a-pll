#!/usr/bin/env python3
"""Layer 1 of the whole-loop verification: a linear (s-domain) model of the PLL.

Run from the repository root (tests/check.sh does). It needs only python3 and
PyYAML: no PDK and no simulator. It reads what the analog half was signed off
with, and builds the textbook type-II charge-pump loop from it:

  - R1, C1, C2 from analog/sizing/sizing.yaml (ppolyf_u at 350 ohm/sq over a
    2 um width, cap_mim_2f0 at 2 fF/um2 on a square side, as sizing.yaml says);
  - Icp (mean of UP and DN at code 00) and Kvco (mean slope, Hz/V) at every
    corner from the recorded PVT run, analog/reports/recorded/gate-sim_pvt.json.

  H(s) = Icp * Kvco * Z(s) / (s * P*N),  Z(s) = (1 + s R C1) / (s (C1+C2) (1 + s R Cs))

with Cs = C1 C2 / (C1 + C2), the same open-loop gain pll_analog_ol_tb.cir
measures, so the model can be checked against ngspice before later layers
lean on it. It fails when:
  - at a corner with typical passives, the model's phase margin at P*N = 16
    is more than PM_TOL_DEG from ngspice's ol_pm_pn16_nopad_pvt_deg;
  - the model's phase margin at P*N = 16 is under the spec's 30 deg floor at
    any corner it can model;
  - the 100 MHz nominal point lies outside a corner's measured VCO range;
  - the small-signal settling estimate 4/(zeta wn) exceeds the 50 us lock-time
    target at any P*N.
It prints the margins at P*N = 8..40 and the lock-table points each corner's
VCO range misses, which are reported, not failed: the spec scores only P*N = 16
at every corner.
"""
import json
import math
import sys
from pathlib import Path

import yaml

ANALOG = Path("blocks/pll/analog")
SHEET_OHM = 350.0  # ppolyf_u, sizing.yaml
MIM_F_PER_M2 = 2e-3  # 2 fF/um2
R1_W = 2e-6  # XR1 r_width in netlist/pll_analog.cir
P = 8
NS = [1, 2, 3, 4, 5]
PM_TOL_DEG = 3.0
PM_FLOOR_DEG = 30.0
LOCK_US_MAX = 50.0
NOMINAL = (6.25e6, 2)  # 6.25 MHz x 8 x 2 = 100 MHz
LOCK_TABLE = {5e6: [2, 3, 4, 5], 6.25e6: [1, 2, 3, 4], 10e6: [1, 2], 12.5e6: [1, 2]}


def filter_values():
    s = yaml.safe_load((ANALOG / "sizing/sizing.yaml").read_text())
    r1 = SHEET_OHM * s["r1_l"]["value"] / R1_W
    c1 = MIM_F_PER_M2 * s["c1_w"]["value"] ** 2
    c2 = MIM_F_PER_M2 * s["c2_w"]["value"] ** 2
    return r1, c1, c2


def corners():
    """Per corner: passive skew, Icp (A), Kvco (Hz/V), VCO range (Hz), ngspice PM16."""
    rep = json.loads((ANALOG / "reports/recorded/gate-sim_pvt.json").read_text())
    out = {}
    for row in rep["facts"]["results"]:
        c = out.setdefault(row["corner"], {"passive": row["passive"]})
        m = row["measures"]
        if "icp_up_code00_ua" in m and "icp_dn_code00_ua" in m:
            c["icp"] = (m["icp_up_code00_ua"] + m["icp_dn_code00_ua"]) / 2 * 1e-6
        if "vco_kvco_mhz_per_v" in m:
            c["kvco"] = m["vco_kvco_mhz_per_v"] * 1e6
            c["fmin"] = m["vco_fmin_tt_mhz"] * 1e6
            c["fmax"] = m["vco_fmax_tt_mhz"] * 1e6
        if "ol_pm_pn16_nopad_pvt_deg" in m:
            c["pm16_spice"] = m["ol_pm_pn16_nopad_pvt_deg"]
    return out


def loop(icp, kvco, r1, c1, c2, pn):
    """Crossover (Hz), phase margin (deg), zeta and settling estimate (s)."""
    cs = c1 * c2 / (c1 + c2)

    def gain(f):
        w = 2 * math.pi * f
        z = math.hypot(1, w * r1 * c1) / (w * (c1 + c2) * math.hypot(1, w * r1 * cs))
        return icp * kvco * z / (w * pn)

    lo, hi = 1e3, 1e9
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        lo, hi = (mid, hi) if gain(mid) > 1 else (lo, mid)
    fc = math.sqrt(lo * hi)
    wc = 2 * math.pi * fc
    pm = math.degrees(math.atan(wc * r1 * c1) - math.atan(wc * r1 * cs))
    wn = math.sqrt(icp * 2 * math.pi * kvco / (2 * math.pi * pn * (c1 + c2)))
    zeta = r1 * c1 * wn / 2
    return fc, pm, zeta, 4 / (zeta * wn)


def main() -> int:
    r1, c1, c2 = filter_values()
    print(f"loop: R1 {r1/1e3:.1f} kOhm, C1 {c1*1e12:.1f} pF, C2 {c2*1e12:.2f} pF (sizing.yaml, typical passives)")
    problems, worst = [], {}
    for name, c in corners().items():
        if not {"icp", "kvco", "pm16_spice"} <= c.keys():
            problems.append(f"{name}: the recorded PVT run lacks Icp, Kvco or the P*N = 16 margin")
            continue
        if c["passive"] != "typical":
            print(f"loop: {name}: {c['passive']} passives, not modelled (ngspice PM16 {c['pm16_spice']:.1f} deg)")
            continue
        fc16, pm16, _, _ = loop(c["icp"], c["kvco"], r1, c1, c2, P * 2)
        if abs(pm16 - c["pm16_spice"]) > PM_TOL_DEG:
            problems.append(
                f"{name}: model PM16 {pm16:.1f} deg vs ngspice {c['pm16_spice']:.1f} deg, more than {PM_TOL_DEG} apart"
            )
        if pm16 < PM_FLOOR_DEG:
            problems.append(f"{name}: model PM16 {pm16:.1f} deg is under the {PM_FLOOR_DEG} deg floor")
        f_nom = NOMINAL[0] * P * NOMINAL[1]
        if not c["fmin"] <= f_nom <= c["fmax"]:
            problems.append(f"{name}: 100 MHz is outside the VCO range {c['fmin']/1e6:.0f}..{c['fmax']/1e6:.0f} MHz")
        for n in NS:
            fc, pm, zeta, ts = loop(c["icp"], c["kvco"], r1, c1, c2, P * n)
            if ts * 1e6 > LOCK_US_MAX:
                problems.append(f"{name}: P*N = {P*n} settles in {ts*1e6:.1f} us, over {LOCK_US_MAX} us")
            w = worst.setdefault(P * n, (math.inf, None, 0, 0))
            if pm < w[0]:
                worst[P * n] = (pm, name, fc, zeta)
        misses = [
            f"{fr/1e6:g}x{n}"
            for fr, ns in LOCK_TABLE.items()
            for n in ns
            if not c["fmin"] <= fr * P * n <= c["fmax"]
        ]
        print(
            f"loop: {name}: PM16 model {pm16:.1f} / ngspice {c['pm16_spice']:.1f} deg, fc16 {fc16/1e3:.0f} kHz,"
            f" VCO {c['fmin']/1e6:.0f}..{c['fmax']/1e6:.0f} MHz"
            + (f", lock-table points out of range: {' '.join(misses)}" if misses else "")
        )
    for pn, (pm, name, fc, zeta) in sorted(worst.items()):
        print(f"loop: P*N = {pn}: worst PM {pm:.1f} deg at {name} (fc {fc/1e3:.0f} kHz, zeta {zeta:.2f})")
    if problems:
        for p in problems:
            print(f"loop: {p}")
        return 1
    print("loop: ok, the linear model matches ngspice and meets the margin and settling targets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
