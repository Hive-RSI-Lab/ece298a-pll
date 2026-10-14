#!/usr/bin/env python3
"""Layer 1 of the whole-loop verification: a linear model of the PLL loop.

Run from the repository root (tests/check.sh does). It needs only python3 and
PyYAML. It takes R1, C1 and C2 from the analog netlist's .param defaults, and
Icp (code 00, mean of UP and DN) and Kvco from the recorded PVT simulation
(blocks/pll/analog/reports/recorded/gate-sim_pvt.json), and at every corner
there and every point of the proposal's lock table it computes the
open-loop crossover and phase margin, the Gardner sampling limit and the
small-signal settling time of the type-2, third-order loop

    H(s) = K (1 + s tz) / (s^2 (1 + s tp)),  K = Icp Kvco / (P N (C1 + C2)),
    tz = R1 C1,  tp = R1 C1 C2 / (C1 + C2).

It fails when:
  - the model's phase margin at P*N = 16 is more than PM_TOL_DEG away from
    ngspice's ol_pm_pn16_nopad_pvt_deg at the same corner (the model no
    longer describes the cell the benches measured);
  - the phase margin at P*N = 16 is under the spec's 30 degree floor;
  - a lock-table point breaks the Gardner limit, or its small-signal settling
    time is over the 50 us lock-time bound (digital spec.yaml).
Lock-table points under 30 degrees at other P*N are printed, not failed: the
spec scores the floor at P*N = 16 only.
"""
import json
import math
import re
import sys
from pathlib import Path

NETLIST = Path("blocks/pll/analog/netlist/pll_analog.cir")
PVT = Path("blocks/pll/analog/reports/recorded/gate-sim_pvt.json")

# ppolyf_u sheet resistance and MIM density, as sizing.yaml uses them
# (r1_l = 150 um at 2 um width is ~26 kOhm; 2 fF/um^2).
R_SHEET = 350.0
R1_WIDTH = 2e-6
C_MIM = 2e-3  # F/m^2

# The proposal's lock table: f_ref (Hz) and the N that lock there; P = 8.
LOCK_TABLE = [(5e6, (2, 3, 4, 5)), (6.25e6, (1, 2, 3, 4)), (10e6, (1, 2)), (12.5e6, (1, 2))]

PM_TOL_DEG = 3.0
R_SKEW = (0.6, 1.6)  # the R1 scale a passive corner may fit to
PM_FLOOR_DEG = 30.0
LOCK_MAX_S = 50e-6


def params():
    text = NETLIST.read_text()
    vals = dict(re.findall(r"\b(\w+)=([0-9.eE+-]+)", " ".join(l for l in text.splitlines() if l.startswith(".param"))))
    r1 = R_SHEET * float(vals["r1_l"]) / R1_WIDTH
    c1 = C_MIM * float(vals["c1_w"]) ** 2
    c2 = C_MIM * float(vals["c2_w"]) ** 2
    return r1, c1, c2


def corners():
    """{corner: {icp, kvco, pm16}} from the recorded PVT run."""
    out = {}
    for row in json.loads(PVT.read_text())["facts"]["results"]:
        m, c = row["measures"], out.setdefault(row["corner"], {"passive": row.get("passive")})
        if row["bench"] == "pll_analog_cp_tb.cir":
            c["icp"] = (m["icp_up_code00_ua"] + m["icp_dn_code00_ua"]) / 2 * 1e-6
        elif row["bench"] == "pll_analog_vco_tb.cir":
            c["kvco"] = m["vco_kvco_mhz_per_v"] * 1e6
        elif row["bench"] == "pll_analog_ol_tb.cir":
            if "ol_pm_pn16_nopad_pvt_deg" in m:
                c["pm16"] = m["ol_pm_pn16_nopad_pvt_deg"]
            c["pm_pn"] = {pn: m[f"ol_pm_pn{pn}_nopad_deg"] for pn in (8, 40) if f"ol_pm_pn{pn}_nopad_deg" in m}
    return out


def loop(icp, kvco, pn, r1, c1, c2):
    """(crossover Hz, phase margin deg, settling s) of the linear loop."""
    k = icp * kvco / (pn * (c1 + c2))
    tz, tp = r1 * c1, r1 * c1 * c2 / (c1 + c2)
    mag = lambda w: k * math.hypot(1, w * tz) / (w * w * math.hypot(1, w * tp))
    lo, hi = 1e3, 1e10
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        lo, hi = (mid, hi) if mag(mid) > 1 else (lo, mid)
    wc = lo
    pm = math.degrees(math.atan(wc * tz) - math.atan(wc * tp))
    # closed-loop poles: tp s^3 + s^2 + K tz s + K = 0 (Durand-Kerner)
    coef = [1.0, 1 / tp, k * tz / tp, k / tp]
    roots = [complex(0.4, 0.9) ** i * wc for i in range(3)]
    for _ in range(500):
        roots = [
            r - sum(c * r ** (3 - j) for j, c in enumerate(coef)) / math.prod(r - q for q in roots if q is not r)
            for r in roots
        ]
    sigma = min(-r.real for r in roots)
    settle = math.log(100) / sigma if sigma > 0 else math.inf
    return wc / (2 * math.pi), pm, settle


def gardner_ok(icp, kvco, pn, r1, c1, f_ref):
    """Gardner's sampling limit for a charge-pump loop: wn^2 < wi^2 / (pi (tz wi + pi))."""
    wn2 = icp * kvco / (pn * c1)
    wi = 2 * math.pi * f_ref
    return wn2 < wi * wi / (math.pi * (r1 * c1 * wi + math.pi))


def fit_skew(group, r1, c1, c2):
    """The R1 scale that best matches ngspice's PM at P*N = 16 over a passive corner's corners."""
    err = lambda s: max(abs(loop(c["icp"], c["kvco"], 16, r1 * s, c1, c2)[1] - c["pm16"]) for c in group)
    lo, hi = R_SKEW[0], R_SKEW[1]
    for _ in range(60):
        a, b = lo + (hi - lo) * 0.382, lo + (hi - lo) * 0.618
        lo, hi = (lo, b) if err(a) < err(b) else (a, hi)
    return (lo + hi) / 2


def main() -> int:
    r1, c1, c2 = params()
    data = corners()
    problems, notes, worst = [], [], {}
    for name, c in list(data.items()):
        if not {"icp", "kvco", "pm16"} <= c.keys():
            problems.append(f"{name}: the recorded PVT run lacks Icp, Kvco or ol_pm_pn16_nopad_pvt_deg")
            del data[name]
    # The ss and ff corners skew the passives with the devices (and tt_pss /
    # tt_pff skew them alone). The record does not give the resistor's value, so
    # one R1 scale per passive corner is fitted to ngspice's PM, and every
    # corner of that passive corner then has to agree with it.
    skew = {"typical": 1.0}
    for passive in sorted({c["passive"] for c in data.values()} - {"typical"}):
        s = fit_skew([c for c in data.values() if c["passive"] == passive], r1, c1, c2)
        if not R_SKEW[0] < s < R_SKEW[1]:
            problems.append(f"passive {passive}: the fitted R1 scale {s:.2f} is outside {R_SKEW}")
        skew[passive] = s
    print("loop: R1 scale per passive corner, fitted to ngspice: " + ", ".join(f"{p} {s:.2f}" for p, s in skew.items()))
    tt = data.get("tt_27c", {})
    if len(tt.get("pm_pn", {})) != 2:
        problems.append("tt_27c: the recorded PVT run lacks ol_pm_pn8_nopad_deg or ol_pm_pn40_nopad_deg")
    for pn, pm_ref in tt.get("pm_pn", {}).items():
        pm = loop(tt["icp"], tt["kvco"], pn, r1, c1, c2)[1]
        if abs(pm - pm_ref) > PM_TOL_DEG:
            problems.append(f"tt_27c: model PM at P*N={pn} is {pm:.1f} deg, ngspice {pm_ref:.1f} deg")
    resid = 0.0
    for name, c in data.items():
        r = r1 * skew[c["passive"]]
        _, pm16, _ = loop(c["icp"], c["kvco"], 16, r, c1, c2)
        resid = max(resid, abs(pm16 - c["pm16"]))
        if abs(pm16 - c["pm16"]) > PM_TOL_DEG:
            problems.append(f"{name}: model PM at P*N=16 is {pm16:.1f} deg, ngspice {c['pm16']:.1f} deg")
        if pm16 < PM_FLOOR_DEG:
            problems.append(f"{name}: PM at P*N=16 is {pm16:.1f} deg, under the {PM_FLOOR_DEG:.0f} deg floor")
        for f_ref, ns in LOCK_TABLE:
            for n in ns:
                fc, pm, settle = loop(c["icp"], c["kvco"], 8 * n, r, c1, c2)
                point = f"f_ref {f_ref / 1e6:g} MHz N={n}"
                if not gardner_ok(c["icp"], c["kvco"], 8 * n, r, c1, f_ref):
                    problems.append(f"{name} {point}: breaks the Gardner limit")
                if settle > LOCK_MAX_S:
                    problems.append(f"{name} {point}: settles in {settle * 1e6:.1f} us, over 50 us")
                if pm < PM_FLOOR_DEG:
                    notes.append(f"{name} {point}: PM {pm:.1f} deg")
                w = worst.setdefault(point, [math.inf, "", 0.0, 0.0, 0.0])
                if pm < w[0]:
                    w[:2] = pm, name
                w[2] = max(w[2], fc / f_ref)
                w[3] = max(w[3], settle)
    for point, (pm, name, ratio, settle, _) in worst.items():
        print(f"loop: {point:22s} worst PM {pm:5.1f} deg ({name}), fc <= f_ref/{1 / ratio:4.1f}, settles <= {settle * 1e6:4.1f} us")
    for n in notes:
        print(f"loop: note, under {PM_FLOOR_DEG:.0f} deg off P*N=16: {n}")
    if problems:
        for p in problems:
            print(f"loop: {p}")
        return 1
    print(
        f"loop: ok ({len(data)} corner(s), R1 {r1 / 1e3:.1f} kOhm, C1 {c1 * 1e12:.1f} pF, C2 {c2 * 1e12:.2f} pF,"
        f" model within {resid:.1f} deg of ngspice)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
