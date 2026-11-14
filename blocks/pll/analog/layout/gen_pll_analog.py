"""gen_pll_analog.py - layout generator for blocks/pll/analog (pll_analog,
the analog half of the GF180 charge-pump PLL). Layout is code: every shape
below is drawn by this file from GF180's own primitive cells.

Draws netlist/pll_analog.cir at sizing/sizing.yaml. Sizes are typed in
here as constants named after the sizing.yaml entries; LVS checks them.

Floorplan, bottom to top: the VCO block, then five rows, each with a
private routing channel above it:

  ring     the VCO ring block (ring_block): stages in the order
           3 2 4 1 5, then NAND2 (r5's input first), output
           inverter and the static /2 (vco_out -> vco_div2), flush right
           under the vco_div2 pin. NMOS half below one shared channel, PMOS half
           mirrored above it. Each stage is one column: its inverter
           (2 fingers, drain in the middle) next to the channel, its
           starve device behind it, n_k/p_k joined by a metal2 strap.
           Every inverter-row device's gate via sits over its left pad
           and its top is level with the stage inverters', so no stub
           runs further than the channel for the taller NAND/output.
           Sources tie in metal1 to a rail per half. The starve gates
           run on their own metal3 track behind the inverters, so the
           channel carries only r1..r5, nb, vco_out, pll_en and the
           divider's nodes (dx, dy, dqn, dqb, vco_div2), as short
           metal3 hops between 0.3 um stubs. The rails and the
           vbn_vco/vbp_vco tracks rise in metal4 at the block's left end
           to the rows above.
  mix_n    buffer NMOS pair (ABBA) and mirror load (ABBA), the vref
           mirror bank (FLR BUFT BUFT B1 BUFT BUFT), MN_B2, startup,
           standby clamps, starve masters MN_V2IM/MN_ENV, V2I, ENS
  buf_p    buffer PMOS pair (ABBAABBA), PMOS mirror load (ABBA), the
           inverters' PMOS, MP_STL, UP switches, starve master PMOS pair
           MP_V2I/MP_V2IB (ABBA), MP_ENV
  res      ppolyf_u serpentines: R1, R_V2I, RBIAS_TOP, RBIAS_INT
  cp_n     pump NMOS mirror CPREF/CPREF2/DNS (ABCCBA), DN and trim
           switches, inverter NMOS, MN_CL
  cp_p     pump PMOS mirror CPREF/UPS (ABBA, 50 um units) and the
           14-unit vbp bank, common centroid about its middle:
           BUFT T4 BUFT T4 T2 T1A B2 B1 T1B T2 T4 BUFT T4 BUFT

The ring block is drawn for speed, not equal wire lengths: post-layout
fmax is set by the wire and drain-junction C on r1..r5, so each node gets
the shortest wiring the folded order allows. No metal4 and no cap plate
is near it.

C1 (20 pF) and C2 (2 pF) are MOS caps (cap_nmos_03v3_b, the PDK's
cap_nmos_b cell: n+ in nwell under the poly, accumulation, about 3.9 fF/um2
above 0.5 V) in two rows of their own at the top, cap_a and cap_b, under
one nwell tied to vss through every unit's n+ side. They were MIM-B caps
over the rows until 2026-10-30: a MIM-B top plate is Metal5, which Tiny
Tapeout's GF180 precheck forbids, so nothing here draws above Metal4.

Outside the ring block each device is one or more single-finger units
(draw_nfet/draw_pfet, gate contact on top). netgen merges parallel units (W add) and series
resistor segments (r_length add), so a W=50 device is 2 x 25 here.

Routing ("row + channel"): in a row every unit has three metal2 stubs,
all going UP into the row's own channel: left diffusion, right
diffusion, and the gate, whose metal1 jog carries it to a via right of
the right diffusion pad (so the three stubs never sit closer than metal2
spacing, even at L=0.28). A diode-connected unit (gate = right pad net)
ties the jog to its right pad in metal1. Channel tracks are metal3, one
net per track span (left-edge packing). A net seen in more than one
channel gets a vertical metal4 trunk with a via3 on each of its tracks.
Pins: digital-side pins (vco_div2,
pfd_up, pfd_dn, pll_en, cp_trim0, cp_trim1) are metal3 tracks run out to
the RIGHT edge - the edge facing the digital half and its prescaler;
vctrl, bias_ref, vdd, vss are metal4 trunks run to the BOTTOM edge. Each
pin ends in a via stack on a metal2 pad carrying its metal2 pin label.

Taps: a P+ substrate tap (vss) at each end of every NMOS row and at
most ~10 um apart inside it (DF.14), an N+ tap (vdd) likewise in every
PMOS row under one nwell per row (DF.13). Every resistor segment carries
the PDK cell's own substrate tap, strapped to vss.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# layout_gen.py puts engine/lib on sys.path itself; this is for running
# the file directly.
sys.path.insert(0, str(Path(os.environ.get(
    "CHIP_FLOW_HOME", Path.home() / ".claude/skills/chip-flow"))
    / "engine" / "lib"))
import layoutlib  # noqa: E402

LY = dict(layoutlib.GF180_LAYER)
LY.update({"via2": (38, 0), "metal3": (42, 0), "via3": (40, 0),
           "metal4": (46, 0),
           "metal3_label": (42, 10), "metal4_label": (46, 10)})
M1, M2, M3, M4 = (LY[k] for k in ("metal1", "metal2", "metal3", "metal4"))

CELL = "pll_analog"
PINS = ["vco_div2", "pfd_up", "pfd_dn", "pll_en", "cp_trim0", "cp_trim1",
        "vctrl", "bias_ref", "vdd", "vss"]
RIGHT_PINS = ["vco_div2", "pfd_up", "pfd_dn", "pll_en", "cp_trim0",
              "cp_trim1"]
BOTTOM_PINS = ["vctrl", "bias_ref", "vdd", "vss"]

# ---- sizing (um), sizing/sizing.yaml values ----------------------------
W_BP, L_BP = 4.0, 2.0
W_B1, L_B1 = 2.0, 2.0
W_B2, L_B2 = 4.0, 1.0
RB_L, RBT_L = 366.0, 180.0
W_CPN, L_CPN = 40.0, 4.0
W_CPP, L_CPP = 100.0, 4.0
W_SWN, W_SWP, L_SW = 2.0, 4.0, 0.5
R1_L = 150.0
C1_W, C1_L, C2_W, C2_L = 420.0, 12.0, 43.0, 12.0
W_V2I, L_V2I, RV2I_L = 10.0, 1.0, 43.0
W_FLR, L_FLR = 2.0, 2.0
W_V2IP, W_V2IN, L_V2I2 = 10.0, 4.0, 0.5
W_SP, W_SN, L_S = 10.0, 4.0, 0.5
W_RP, W_RN, L_R = 6.0, 3.0, 0.28
W_GP, W_GN = 4.0, 4.0
W_OP, W_ON = 12.0, 6.0
M_BUFT = 4
W_BUFP, L_BUFP, W_BUFN, L_BUFN = 20.0, 1.0, 10.0, 1.0
W_BUFLN, W_BUFLP, L_BUFL = 4.0, 8.0, 2.0
W_CL, L_CL = 50.0, 1.0
LMIN = 0.28

# ---- devices: name -> (type, drain, gate, source, W total, L, units) ---
# W total includes the netlist's m; units = how many equal single-finger
# pieces it is drawn as.
DEV = {
    "MP_ENI": ("p", "en_b", "pll_en", "vdd", 2.0, LMIN, 1),
    "MN_ENI": ("n", "en_b", "pll_en", "vss", 1.0, 4.0, 1),  # slow en_b fall, topology.md
    "MP_B2": ("p", "vbp", "vbp", "vdd", W_BP, L_BP, 1),
    "MP_B1": ("p", "va", "vbp", "vdd", W_BP, L_BP, 1),
    "MN_B1": ("n", "va", "vref", "vss", W_B1, L_B1, 1),
    "MN_B2": ("n", "vbp", "va", "vref", W_B2, L_B2, 1),
    "MP_STL": ("p", "vst", "en_b", "vdd", 0.5, 10.0, 1),
    "MN_STD": ("n", "vst", "vref", "vss", 10.0, 1.0, 2),
    "MN_ST": ("n", "vbp", "vst", "vss", 0.5, 4.0, 1),
    "MN_STE": ("n", "vst", "en_b", "vss", 1.0, LMIN, 1),
    "MP_ENB": ("p", "vbp", "pll_en", "vdd", 1.0, LMIN, 1),
    "MN_ENA": ("n", "va", "en_b", "vss", 1.0, LMIN, 1),
    "MN_ENB": ("n", "vref", "en_b", "vss", 1.0, LMIN, 1),
    "MP_T4": ("p", "vcp_n", "vbp", "vdd", 4 * W_BP, L_BP, 4),
    "MP_T1A": ("p", "t1a", "vbp", "vdd", W_BP, L_BP, 1),
    "MN_SW0": ("n", "vcp_n", "cp_trim0", "t1a", 2.0, LMIN, 1),
    "MP_T2": ("p", "t2", "vbp", "vdd", 2 * W_BP, L_BP, 2),
    "MN_SW1": ("n", "vcp_n", "cp_trim1", "t2", 2.0, LMIN, 1),
    "MP_T1B": ("p", "t1b", "vbp", "vdd", W_BP, L_BP, 1),
    "MN_SW0B": ("n", "t1c", "cp_trim0", "t1b", 2.0, LMIN, 1),
    "MN_SW1B": ("n", "vcp_n", "cp_trim1", "t1c", 2.0, LMIN, 1),
    "MP_HT1C": ("p", "t1a", "cp_trim0", "vdd", 1.0, LMIN, 1),
    "MP_HT1D": ("p", "t1b", "cp_trim0", "vdd", 1.0, LMIN, 1),
    "MP_HT2B": ("p", "t2", "cp_trim1", "vdd", 1.0, LMIN, 1),
    "MP_HP1": ("p", "p1", "pll_en", "vdd", 1.0, 0.28, 1),
    "MP_HP2": ("p", "p2", "pll_en", "vdd", 1.0, 0.28, 1),
    "MP_HP3": ("p", "p3", "pll_en", "vdd", 1.0, 0.28, 1),
    "MP_HP4": ("p", "p4", "pll_en", "vdd", 1.0, 0.28, 1),
    "MP_HP5": ("p", "p5", "pll_en", "vdd", 1.0, 0.28, 1),
    "MN_CPREF": ("n", "vcp_n", "vcp_n", "vss", W_CPN, L_CPN, 2),
    "MN_CPREF2": ("n", "vcp_p", "vcp_n", "vss", W_CPN, L_CPN, 2),
    "MP_CPREF": ("p", "vcp_p", "vcp_p", "vdd", W_CPP, L_CPP, 2),
    "MP_UPS": ("p", "up_s", "vcp_p", "vdd", W_CPP, L_CPP, 2),
    "MP_UP": ("p", "vctrl", "up_b", "up_s", W_SWP, L_SW, 1),
    "MP_UPD": ("p", "vdump", "pfd_up", "up_s", W_SWP, L_SW, 1),
    "MP_UPI": ("p", "up_b", "pfd_up", "vdd", 2.0, LMIN, 1),
    "MN_UPI": ("n", "up_b", "pfd_up", "vss", 1.0, LMIN, 1),
    "MN_DNS": ("n", "dn_s", "vcp_n", "vss", W_CPN, L_CPN, 2),
    "MN_DN": ("n", "vctrl", "pfd_dn", "dn_s", W_SWN, L_SW, 1),
    "MN_DND": ("n", "vdump", "dn_b", "dn_s", W_SWN, L_SW, 1),
    "MP_DNI": ("p", "dn_b", "pfd_dn", "vdd", 2.0, LMIN, 1),
    "MN_DNI": ("n", "dn_b", "pfd_dn", "vss", 1.0, LMIN, 1),
    "MP_ENP": ("p", "vcp_p", "pll_en", "vdd", 1.0, LMIN, 1),
    "MN_ENN": ("n", "vcp_n", "en_b", "vss", 1.0, LMIN, 1),
    "MP_BUFT": ("p", "vbt", "vbp", "vdd", M_BUFT * W_BP, L_BP, M_BUFT),
    "MP_BUF1": ("p", "vbl", "vctrl", "vbt", W_BUFP, L_BUFP, 4),
    "MP_BUF2": ("p", "vdump", "vdump", "vbt", W_BUFP, L_BUFP, 4),
    "MN_BUFL1": ("n", "vbl", "vbl", "vss", W_BUFLN, L_BUFL, 2),
    "MN_BUFL2": ("n", "vdump", "vbl", "vss", W_BUFLN, L_BUFL, 2),
    "MN_BUFT": ("n", "vnt", "vref", "vss", M_BUFT * W_B1, L_B1, M_BUFT),
    "MN_BUF1": ("n", "vbh", "vctrl", "vnt", W_BUFN, L_BUFN, 2),
    "MN_BUF2": ("n", "vdump", "vdump", "vnt", W_BUFN, L_BUFN, 2),
    "MP_BUFL1": ("p", "vbh", "vbh", "vdd", W_BUFLP, L_BUFL, 2),
    "MP_BUFL2": ("p", "vdump", "vbh", "vdd", W_BUFLP, L_BUFL, 2),
    "MN_V2I": ("n", "vi", "vctrl", "vs", W_V2I, L_V2I, 2),
    "MN_CL": ("n", "vcl", "vref", "vss", W_CL, L_CL, 4),
    "MN_FLR": ("n", "vi", "vref", "vss", W_FLR, L_FLR, 1),
    "MN_ENS": ("n", "vbp_vco", "pll_en", "vi", 10.0, LMIN, 2),
    "MP_V2I": ("p", "vbp_vco", "vbp_vco", "vdd", W_V2IP, L_V2I2, 2),
    "MP_V2IB": ("p", "vbn_vco", "vbp_vco", "vdd", W_V2IP, L_V2I2, 2),
    "MN_V2IM": ("n", "vbn_vco", "vbn_vco", "vss", W_V2IN, L_V2I2, 1),
    "MP_ENV": ("p", "vbp_vco", "pll_en", "vdd", 1.0, LMIN, 1),
    "MN_ENV": ("n", "vbn_vco", "en_b", "vss", 1.0, LMIN, 1),
    "MP_G1": ("p", "nb", "r5", "vdd", W_GP, LMIN, 1),
    "MP_G2": ("p", "nb", "pll_en", "vdd", W_GP, LMIN, 1),
    "MN_G1": ("n", "nb", "r5", "ng", W_GN, LMIN, 1),
    "MN_G2": ("n", "ng", "pll_en", "vss", W_GN, LMIN, 1),
    "MP_O": ("p", "vco_out", "nb", "vdd", W_OP, LMIN, 2),
    "MN_O": ("n", "vco_out", "nb", "vss", W_ON, LMIN, 1),
    # (8) static master-slave /2, vco_out -> vco_div2 (netlist block 8)
    "MP_DCI": ("p", "clkb", "vco_out", "vdd", 1.0, LMIN, 1),
    "MN_DCI": ("n", "clkb", "vco_out", "vss", 0.5, LMIN, 1),
    "MN_DCT": ("n", "ck", "vdd", "vco_out", 0.5, LMIN, 1),
    "MP_DCT": ("p", "ck", "vss", "vco_out", 1.0, LMIN, 1),
    "MN_DXA": ("n", "vss", "m1", "vss", 4.0, 1.0, 1),
    "MN_DXB": ("n", "vss", "s1", "vss", 4.0, 1.0, 1),
    "MN_DXC": ("n", "vss", "mf", "vss", 4.0, 1.0, 1),
    "MN_DXD": ("n", "vss", "sf", "vss", 4.0, 1.0, 1),
    "MN_DT1": ("n", "m1", "clkb", "s1", 1.0, LMIN, 1),
    "MP_DT1": ("p", "m1", "ck", "s1", 2.0, LMIN, 1),
    "MP_DF1": ("p", "m2", "m1", "vdd", 2.0, LMIN, 1),
    "MN_DF1": ("n", "m2", "m1", "vss", 1.0, LMIN, 1),
    "MP_DK1": ("p", "mf", "m2", "vdd", 1.0, LMIN, 1),
    "MN_DK1": ("n", "mf", "m2", "vss", 0.5, LMIN, 1),
    "MN_DT2": ("n", "m1", "ck", "mf", 0.5, LMIN, 1),
    "MP_DT2": ("p", "m1", "clkb", "mf", 1.0, LMIN, 1),
    "MN_DT3": ("n", "s1", "ck", "m2", 1.0, LMIN, 1),
    "MP_DT3": ("p", "s1", "clkb", "m2", 2.0, LMIN, 1),
    "MP_DF2": ("p", "dqn", "s1", "vdd", 2.0, LMIN, 1),
    "MN_DF2": ("n", "dqn", "s1", "dr", 2.0, LMIN, 1),
    "MN_DF2R": ("n", "dr", "pll_en", "vss", 2.0, LMIN, 1),
    "MP_DF2R": ("p", "dqn", "pll_en", "vdd", 1.0, LMIN, 1),
    "MP_DK2": ("p", "sf", "dqn", "vdd", 1.0, LMIN, 1),
    "MN_DK2": ("n", "sf", "dqn", "vss", 0.5, LMIN, 1),
    "MN_DT4": ("n", "s1", "clkb", "sf", 0.5, LMIN, 1),
    "MP_DT4": ("p", "s1", "ck", "sf", 1.0, LMIN, 1),
    "MP_DO1": ("p", "dqb", "dqn", "vdd", 2.0, LMIN, 1),
    "MN_DO1": ("n", "dqb", "dqn", "vss", 1.0, LMIN, 1),
    "MP_DO2": ("p", "vco_div2", "dqb", "vdd", 6.0, LMIN, 1),
    "MN_DO2": ("n", "vco_div2", "dqb", "vss", 3.0, LMIN, 1),
}
for _k in range(1, 6):
    _prev = f"r{5 if _k == 1 else _k - 1}"
    DEV[f"MP_S{_k}"] = ("p", f"p{_k}", "vbp_vco", "vdd", W_SP, L_S, 1)
    DEV[f"MP_I{_k}"] = ("p", f"r{_k}", _prev, f"p{_k}", W_RP, L_R, 1)
    DEV[f"MN_I{_k}"] = ("n", f"r{_k}", _prev, f"n{_k}", W_RN, L_R, 1)
    DEV[f"MN_S{_k}"] = ("n", f"n{_k}", "vbn_vco", "vss", W_SN, L_S, 1)

# ---- resistors: name -> (end a, end b, width, total length, segments) --
RES = {
    "R_V2I": ("vs", "vcl", 1.0, RV2I_L, 2),
    "R1": ("vctrl", "vfilt", 2.0, R1_L, 4),
    "RBIAS_TOP": ("vref", "bias_ref", 1.0, RBT_L, 6),
    "RBIAS_INT": ("bias_ref", "vss", 1.0, RB_L, 10),
}
# ---- MOS caps (cap_nmos_03v3_b): name -> (gate net, n+/nwell net,
# W total, L, units). A unit is the PDK's cap_nmos_b cell, poly L along x.
CAPS = {"C1": ("vfilt", "vss", C1_W, C1_L, 12),
        "C2": ("vctrl", "vss", C2_W, C2_L, 1)}
CAP_GAP = 2.0     # COMP to COMP between neighbouring cap units


RING_ORDER = [3, 2, 4, 1, 5]   # every hop spans 1-2 stages; 5 next to NAND
# the ring block: columns left to right, each (NMOS group, PMOS group).
# A group's devices abut, sharing the diffusion between them (a stage's
# starve device and inverter share n_k / p_k; the NAND's series pair
# shares ng; its parallel PMOS pair shares nb).
# the static /2, left to right. An inverter's NMOS and PMOS share a
# column (same gate net, same output pad). A pass gate's NMOS and PMOS
# take a column each: their gates are opposite clock phases, and paired
# they would set clkb under vco_out at one gate and over it at the next
# (a track cycle in the shared channel).
DIV_COLS = [
    ("MN_DCI", "MP_DCI"), ("MN_DCT", None), (None, "MP_DCT"),
    ("MN_DXA", None), ("MN_DT1", None), (None, "MP_DT1"), ("MN_DXC", None),
    ("MN_DF1", "MP_DF1"), ("MN_DK1", "MP_DK1"), ("MN_DT2", None),
    (None, "MP_DT2"), ("MN_DT3", None), (None, "MP_DT3"),
    ("MN_DF2R", "MP_DF2R"), ("MN_DF2", "MP_DF2"), ("MN_DK2", "MP_DK2"),
    ("MN_DXB", None), ("MN_DXD", None),
    ("MN_DT4", None), (None, "MP_DT4"), ("MN_DO1", "MP_DO1"),
    ("MN_DO2", "MP_DO2")]
RING_COLS = (
    [("stage", k) for k in RING_ORDER]
    + [("row", ["MN_G1", "MN_G2"], ["MP_G1", "MP_G2"]),
       ("row", ["MN_O"], ["MP_O"]), ("row", [], ["MP_O"]),
       # the static /2, columns from DIV_COLS
       ] + [("row", [n] if n else [], [q] if q else []) for n, q in DIV_COLS])
# nets that live only between a stage's (or the NAND's) own devices,
# joined by a metal2 strap under them: no channel stub
INTERNAL = {f"n{k}" for k in range(1, 6)} | {f"p{k}" for k in range(1, 6)} \
    | {"ng", "dr"}

# rows bottom to top: (name, kind, items). An item is a device name (its
# next unit) or "T" (a tap). Taps are also added wherever a row runs more
# than TAP_RUN um without one.
ROWS = [
    ("ring", "ring", None),
    ("mix_n", "n", ["MN_BUF1", "MN_BUF2", "MN_BUF2", "MN_BUF1",
                    "MN_BUFL1", "MN_BUFL2", "MN_BUFL2", "MN_BUFL1",
                    "MN_FLR", "MN_BUFT", "MN_BUFT", "MN_B1", "MN_BUFT",
                    "MN_BUFT", "MN_B2", "MN_STD", "MN_STD", "MN_ST",
                    "MN_STE", "MN_ENA", "MN_ENB",
                    "MN_V2IM", "MN_ENV", "MN_V2I", "MN_V2I", "MN_ENS",
                    "MN_ENS"]),
    ("buf_p", "p", ["MP_BUF1", "MP_BUF2", "MP_BUF2", "MP_BUF1",
                    "MP_BUF1", "MP_BUF2", "MP_BUF2", "MP_BUF1",
                    "MP_BUFL1", "MP_BUFL2", "MP_BUFL2", "MP_BUFL1",
                    "MP_UPI", "MP_DNI", "MP_ENP", "MP_ENB", "MP_ENI",
                    "MP_STL", "MP_UP", "MP_UPD",
                    "MP_V2I", "MP_V2IB", "MP_V2IB", "MP_V2I", "MP_ENV"]),
    ("res", "r", None),
    ("cp_n", "n", ["MN_CPREF", "MN_CPREF2", "MN_DNS", "MN_DNS",
                   "MN_CPREF2", "MN_CPREF",
                   "MN_DN", "MN_DND", "MN_SW0", "MN_SW1", "MN_SW0B",
                   "MN_SW1B", "MN_UPI", "MN_DNI", "MN_ENN", "MN_ENI",
                   "MN_CL", "MN_CL", "MN_CL", "MN_CL"]),
    ("cp_p", "p", ["MP_CPREF", "MP_UPS", "MP_UPS", "MP_CPREF",
                   "MP_BUFT", "MP_T4", "MP_BUFT", "MP_T4", "MP_T2",
                   "MP_T1A", "MP_B2", "MP_B1", "MP_T1B", "MP_T2",
                   "MP_T4", "MP_BUFT", "MP_T4", "MP_BUFT",
                   "MP_HT2B", "MP_HT1C", "MP_HT1D"]),
    ("cap_a", "c", ["C1"] * 7),
    ("cap_b", "c", ["C1"] * 5 + ["C2"]),
]
RES_ORDER = ["R1", "R_V2I", "RBIAS_TOP", "RBIAS_INT"]

# ---- geometry (um) -----------------------------------------------------
GAP = 1.2         # COMP to COMP between neighbouring units/taps in a row
GOFF = 0.75       # gate via: this far right of the right diffusion pad
TAP = 1.0         # tap COMP size
TAP_RUN = 15.0    # longest stretch of a row without a tap
TRK_W = 0.4       # metal2/3/4 wire width (= a via landing)
TRK_P = 0.8       # metal3 track pitch, metal4 column pitch
RING_TRK_P = 0.8  # the ring block's shared channel: every ring node's
RING_LW = 0.3     # stubs cross all of it, so its pitch is the rows'; thinner
                  # wires (0.4 via landings kept) - less coupling
CH_IN = 1.0       # row's top shape to the channel's first track
ROW_SP = 1.6      # channel's last track to the next row's lowest shape
RES_P = {1.0: 3.0, 2.0: 4.0}   # resistor segment pitch by width
RES_GAP = 3.0     # extra space between two resistor chains
# supplies: the whole block's vdd/vss current runs up one metal4 trunk each
# and out along each channel's first (bottom) metal3 track, so they are
# drawn wider than a signal track (em_ir, transient, sized off the worst
# corner's mean/rms current with margin at the EM limits' temperature)
SUP_NETS = ("vdd", "vss")
# Supply widths, from the worst PVT corner (ff, -40 C, vdd +10 %: 1.06 mA
# rms on vdd and vss) with 1.5x margin on the 125 C limits (0.67 mA/um
# wire, 0.18 mA per via cut). The whole supply current runs only between
# the pin and the trunk's lowest channel rail: that stretch is widened to
# SUP_FOOT_W = 1.06*1.5/0.67 = 2.4 um (2.8 for the op, below), into free room beside it, so no
# signal column moves. Above it the trunk carries at most 0.45 mA (2.0 um
# keeps 3x). The busiest rail carries 0.63 mA: 1.6 um and 6 via3 cuts per
# crossing. The pin foot carries all of it: 9 cuts, a 2.0 um tall pad.
# The DC operating point is heavier than the running ring (every ring stage
# sits at its trip point there, so the inverters pass crowbar current):
# 1.72 mA up the foot and 1.29 mA along a channel's supply track at the
# worst corner. The foot is 2.8 um (0.61 mA/um) and the track 2.0 um
# (0.65 mA/um), both under 0.67 mA/um at that op.
SUP_M4_W = 2.0    # supply metal4 trunk width
SUP_FOOT_W = 2.8  # its pin-to-first-rail stretch (the whole supply current)
SUP_M3_W = 2.0    # supply metal3 channel track width, grown DOWN from the
                  # track's usual top edge (rows carry no metal3 below it)
SUP_FOOT_H = 2.0  # supply pin-foot pad height (via2/via3 arrays)
CUT, CUT_SP, CUT_EN = 0.26, 0.26, 0.12   # via2/via3 cut, space, enclosure
RAIL_STRAP_E = 1.6   # a ring rail's metal2 strap, grown past the rail
RAIL_M1_E = 0.8      # its metal1, grown the same way: where the strap is
                     # notched round another net's foot the metal1 alone
                     # carries the ring current (0.78 mA at the operating
                     # point, 1.5 x 0.47 mA rms: 1.4 um at 0.67 mA/um)
# Ring signal nets whose wiring carries the ring's switching current
# (worst corner ff_m40c_vp10, from the em_ir segment currents):
#   nb      NAND output, 0.235 mA rms, 0.49 mA at the operating point
#   vco_out output inverter, 0.315 mA rms
#   ng      NAND series node, 0.241 mA rms, 0.49 mA at the operating point
#   vco_div2 divider output, 0.163 mA rms
# 1.5x the rms over 0.18 mA a cut is 2 to 3 cuts, so every pad via1 and
# channel via2 of these nets grows to SIG_CUTS cuts where the metal has
# room (sig_em_arrays); 1.5x the rms (and the operating point) over
# 0.67 mA/um is 0.71-0.73 um, so their stubs are SIG_W wide.
SIG_EM = ("nb", "vco_out", "ng", "vco_div2")
SIG_WIDE = ("nb", "vco_out")
SIG_CUTS = 3
SIG_W = 0.76
NG_STRAP_W = 0.8     # the ng strap (and its drops): 0.49 mA / 0.67 mA/um
SIG_SPOTS = []       # (x, y, cut, lower, upper): filled while drawing
SIG_STUBS = []       # (x, y0, y1) metal2 stubs to widen


# ======================================================================
def r5(v):
    """Round onto the 5 nm grid."""
    return round(round(v / 0.005) * 0.005, 3)


def rect(top, x0, y0, x1, y1, layer):
    layoutlib.rect(top, r5(min(x0, x1)), r5(min(y0, y1)),
                   r5(max(x0, x1)), r5(max(y0, y1)), layer)


def via(top, x, y, cut, lower, upper, land=TRK_W):
    h, e = 0.13, land / 2
    rect(top, x - h, y - h, x + h, y + h, LY[cut])
    rect(top, x - e, y - e, x + e, y + e, lower)
    rect(top, x - e, y - e, x + e, y + e, upper)


def via_array(top, x0, y0, x1, y1, cut, lower, upper):
    """As many `cut` cuts as fit in x0..x1 x y0..y1 (a pitch of CUT+CUT_SP,
    CUT_EN inside the box), with lower/upper metal over the whole box.
    Returns the cut count."""
    rect(top, x0, y0, x1, y1, lower)
    rect(top, x0, y0, x1, y1, upper)
    pit = CUT + CUT_SP
    nx = max(int((x1 - x0 - 2 * CUT_EN - CUT) / pit + 1e-6) + 1, 1)
    ny = max(int((y1 - y0 - 2 * CUT_EN - CUT) / pit + 1e-6) + 1, 1)
    sx = ((x0 + x1) - (nx - 1) * pit) / 2
    sy = ((y0 + y1) - (ny - 1) * pit) / 2
    h = CUT / 2
    for i in range(nx):
        for j in range(ny):
            x, y = r5(sx + i * pit), r5(sy + j * pit)
            rect(top, x - h, y - h, x + h, y + h, LY[cut])
    return nx * ny


def widen_supply_feet(top, feet):
    """Widen each supply trunk's foot stretch (pin to its first rail) to
    SUP_FOOT_W, into whichever side has room (0.4 from any other net's
    metal4, and from other metal2/metal3 at the pin pad), then draw the pin
    pad's via2/via3 arrays over the widened foot."""
    import klayout.db as kdb

    dbu = top.kcl.dbu
    regs = {m: kdb.Region(top.kdb_cell.begin_shapes_rec(top.kcl.layer(*m)))
            .merged() for m in (M2, M3, M4)}

    def box(x0, y0, x1, y1):
        return kdb.Box(*(int(round(v / dbu)) for v in (x0, y0, x1, y1)))

    def others(m, own):
        return regs[m] - regs[m].interacting(kdb.Region(own))

    for net, x, hw, y0, y1, f1 in feet:
        own = box(x - 0.01, y0, x + 0.01, y0 + 0.02)
        grow = r5(SUP_FOOT_W / 2 - hw)
        for left, right in ((grow, grow), (2 * grow, 0), (0, 2 * grow)):
            ext = box(x - hw - left, y0, x + hw + right, y1)
            pad = box(x - hw - left, y0, x + hw + right, f1)
            ok = not (others(M4, own) & kdb.Region(ext.enlarged(
                int(round(0.4 / dbu))))).count()
            for m in (M2, M3):
                ok = ok and not (others(m, own) & kdb.Region(pad.enlarged(
                    int(round(0.4 / dbu))))).count()
            if ok:
                break
        else:
            raise layoutlib.LayoutError(
                f"no room to widen the {net} trunk's foot to {SUP_FOOT_W} um")
        xa, xb = r5(x - hw - left), r5(x + hw + right)
        rect(top, xa, y0, xb, y1, M4)
        via_array(top, xa, y0, xb, f1, "via3", M3, M4)
        via_array(top, xa, y0, xb, f1, "via2", M2, M3)


def widen_supply_taps(top, taps):
    """Give each supply stub onto its wide metal3 track a via2 array inside
    the track: 2 x 3 cuts on a metal2 pad 1.02 um wide, centred on the stub
    or slid towards either side, wherever it clears other nets' metal2
    and metal3 by 0.3 um; else 3 cuts in a column on the stub itself.

    em_ir charges an array with the whole current of every extraction node
    within 1 um of it (magic does not say which cut a wire crosses), so a
    tap on a rail carries the rail's current: up to 0.63 mA at the worst
    corner, 3.5 cuts at 0.18 mA a cut, 5.3 with 1.5x margin."""
    import klayout.db as kdb

    dbu = top.kcl.dbu
    regs = {m: kdb.Region(top.kdb_cell.begin_shapes_rec(top.kcl.layer(*m)))
            .merged() for m in (M2, M3)}

    def box(x0, y0, x1, y1):
        return kdb.Box(*(int(round(v / dbu)) for v in (x0, y0, x1, y1)))

    sp = int(round(0.3 / dbu))    # metal2/3 space is 0.28
    pw = 2 * CUT_EN + 2 * CUT + CUT_SP          # 2 cuts across
    for net, x, b0, b1 in taps:
        y0, y1 = r5(b0 + 0.03), r5(b1 - 0.03)
        own = {m: regs[m].interacting(kdb.Region(box(x - 0.01, y0, x + 0.01,
                                                     y1))) for m in (M2, M3)}
        # centred first, then sliding out to either side in 20 nm steps
        # until the pad is flush with a side of the stub
        steps = int(round((pw - TRK_W) / 2 / 0.02))
        for xa in [r5(x - pw / 2 + s * k * 0.02) for k in range(steps + 1)
                   for s in ((1, -1) if k else (1,))]:
            pad = box(xa, y0, xa + pw, y1)
            if all(not ((regs[m] - own[m]) & kdb.Region(pad.enlarged(sp)))
                   .count() for m in (M2, M3)):
                via_array(top, r5(xa), y0, r5(xa + pw), y1, "via2", M2, M3)
                break
        else:
            pit = CUT + CUT_SP
            yc = (y0 + y1) / 2
            for k in (-1, 0, 1):
                via(top, x, r5(yc + k * pit), "via2", M2, M3)


def widen_supply_stacks(top, stacks):
    """Draw each supply via stack (the ring's rail risers) as 12-cut
    arrays (3 x 4, 4 x 3 or 2 x 6) on pads of every metal it joins, placed over the
    0.4 um wire end at (x, y) wherever the pads clear other nets' metal by
    0.3 um: the riser pair sits 0.8 um apart, so a pad grows to the free
    side. A stack with no room raises: a single cut there would carry the
    whole ring current (1.24 mA rms at the worst corner: 1.5x that over
    0.18 mA a cut is 10.3 cuts)."""
    import klayout.db as kdb

    dbu = top.kcl.dbu
    mets = (M1, M2, M3, M4)
    regs = {m: kdb.Region(top.kdb_cell.begin_shapes_rec(top.kcl.layer(*m)))
            .merged() for m in mets}

    def box(x0, y0, x1, y1):
        return kdb.Box(*(int(round(v / dbu)) for v in (x0, y0, x1, y1)))

    sp = int(round(0.3 / dbu))
    st = 0.02
    for x, y, cuts in stacks:
      for ncx, ncy in ((3, 4), (4, 3), (2, 6)):
        pw = 2 * CUT_EN + ncx * CUT + (ncx - 1) * CUT_SP
        ph = 2 * CUT_EN + ncy * CUT + (ncy - 1) * CUT_SP
        xs = [r5(x0) for x0 in
              (k * st for k in range(int(round((pw - TRK_W) / st)) + 1))]
        ys = [r5(y0) for y0 in
              (k * st for k in range(int(round((ph - TRK_W) / st)) + 1))]
        ms = sorted({m for _c, lo, hi in cuts for m in (lo, hi)})
        dot = kdb.Region(box(x - 0.01, y - 0.01, x + 0.01, y + 0.01))
        own = {m: regs[m].interacting(dot) for m in ms}
        # pad corner (xa, ya) with the wire end inside; try nearest-centred
        cand = sorted(((x + TRK_W / 2 - pw + dx, y + TRK_W / 2 - ph + dy)
                       for dx in xs for dy in ys),
                      key=lambda c: (abs(c[0] + pw / 2 - x)
                                     + abs(c[1] + ph / 2 - y)))
        done = False
        for xa, ya in cand:
            pad = box(xa, ya, xa + pw, ya + ph)
            if all(not ((regs[m] - own[m]) & kdb.Region(pad.enlarged(sp)))
                   .count() for m in ms):
                for cut, lo, hi in cuts:
                    via_array(top, r5(xa), r5(ya), r5(xa + pw), r5(ya + ph),
                              cut, lo, hi)
                done = True
                break
        if done:
            break
      else:
        raise layoutlib.LayoutError(
            f"no room for a 12-cut supply array at ({x}, {y})")


def strap_ring_rails(top, rails, feet):
    """Lay a metal2 strap over each ring supply rail (metal1, 0.6 um), from
    its riser end to the ring's far end, grown RAIL_STRAP_E away from the
    ring and notched 0.3 um clear of other nets' metal2, with a row of via1
    cuts along the rail. It joins the rail's own trunk foot where it
    passes over it, feeding the rail from both ends. The rail carries the
    whole ring current from its riser: 1.24 mA rms at the worst corner,
    1.5x that at 0.67 mA/um is 2.8 um of metal: 0.6 of metal1 plus 0.6 +
    1.6 of metal2."""
    import klayout.db as kdb

    dbu = top.kcl.dbu

    def box(x0, y0, x1, y1):
        return kdb.Box(*(int(round(v / dbu)) for v in (x0, y0, x1, y1)))

    def reg(m):
        return kdb.Region(top.kdb_cell.begin_shapes_rec(
            top.kcl.layer(*m))).merged()

    m1, m2 = reg(M1), reg(M2)
    sp = int(round(0.3 / dbu))
    for net, px, ry, out, x_end in rails:
        line = kdb.Region(box(px - 0.01, ry - 0.01, px + 0.01, ry + 0.01))
        piece = (m1 & kdb.Region(box(-1e3, ry - 0.3, 1e3, ry + 0.3))
                 ).merged().interacting(line)
        b = piece.bbox()
        # the rail runs on into the block's other metal1 past the ring
        xa, xb = r5(b.left * dbu), r5(min(b.right * dbu, x_end + 1.0))
        y0, y1 = r5(ry - 0.3), r5(ry + 0.3)
        own = m2.interacting(kdb.Region(box(xa, y0, xb, y1)))
        for fn_, fx, _hw, fy0, _fy1, _f1 in feet:
            if fn_ == net:
                own += m2.interacting(kdb.Region(
                    box(fx - 0.01, fy0 + 0.01, fx + 0.01, fy0 + 0.03)))
        strap = kdb.Region(box(xa, y0 - RAIL_STRAP_E * (out < 0), xb,
                               y1 + RAIL_STRAP_E * (out > 0)))
        strap -= (m2 - own).sized(sp)
        # keep what joins the rail, cleared of slivers under metal2 width
        strap = strap.interacting(kdb.Region(box(xa, y0, xb, y1)))
        strap = strap.sized(-int(round(0.15 / dbu))).sized(
            int(round(0.15 / dbu)))
        if strap.is_empty():
            raise layoutlib.LayoutError(f"no room for the {net} rail strap")
        li = top.kcl.layer(*M2)
        for poly in strap.each():
            top.kdb_cell.shapes(li).insert(poly)
        rect(top, xa, y0, xb, y1, M2)
        m1 = reg(M1)
        own1 = m1.interacting(kdb.Region(box(xa, y0, xb, y1)))
        grow = kdb.Region(box(xa, y0 - RAIL_M1_E * (out < 0), xb,
                              y1 + RAIL_M1_E * (out > 0)))
        grow -= (m1 - own1).sized(sp)
        grow = grow.interacting(kdb.Region(box(xa, y0, xb, y1)))
        grow = grow.sized(-int(round(0.12 / dbu))).sized(
            int(round(0.12 / dbu)))
        l1 = top.kcl.layer(*M1)
        for poly in grow.each():
            top.kdb_cell.shapes(l1).insert(poly)
        v1 = reg(LY["via1"])
        pit = CUT + CUT_SP
        h = CUT / 2
        x = xa + CUT_EN + h
        while x + h + CUT_EN <= xb:
            c = box(x - h, ry - h, x + h, ry + h)
            if not (v1 & kdb.Region(c.enlarged(int(round(CUT_SP / dbu))))
                    ).count():
                rect(top, x - h, ry - h, x + h, ry + h, LY["via1"])
            x = r5(x + pit)

def sig_em_arrays(top, stubs, spots):
    """Widen the SIG_WIDE metal2 stubs to SIG_W, toward whichever side
    clears other nets' metal2 by 0.3 um, then grow each single via in
    `spots` to SIG_CUTS cuts (or as many as fit, at least 2): a column
    along its stub or a row along its track, on 0.4 um landings in both
    metals, wherever the landings clear other nets' metal by 0.3 um.
    Of the arrays that fit, the one adding least new metal wins (least
    added capacitance on the VCO nodes)."""
    import klayout.db as kdb

    dbu = top.kcl.dbu
    sp = int(round(0.3 / dbu))

    def box(x0, y0, x1, y1):
        return kdb.Box(*(int(round(v / dbu)) for v in (x0, y0, x1, y1)))

    def reg(m):
        return kdb.Region(top.kdb_cell.begin_shapes_rec(
            top.kcl.layer(*m))).merged()

    def dot(x, y):
        return kdb.Region(box(x - 0.01, y - 0.01, x + 0.01, y + 0.01))

    short = []
    m2 = reg(M2)
    for x, y0, y1 in stubs:
        own = m2.interacting(dot(x, (y0 + y1) / 2))
        n = int(round((SIG_W - TRK_W) / 0.02))
        for k in sorted(range(n + 1), key=lambda k: abs(k - n / 2)):
            xa = r5(x + TRK_W / 2 - SIG_W + k * 0.02)
            b = box(xa, y0, xa + SIG_W, y1)
            if not ((m2 - own) & kdb.Region(b.enlarged(sp))).count():
                rect(top, xa, y0, xa + SIG_W, y1, M2)
                m2 = reg(M2)
                break
        else:
            short.append(("stub", x, y0, y1))
    pit = CUT + CUT_SP
    h, e = CUT / 2, TRK_W / 2
    seen = set()
    thin = []
    for x, y, cut, lo, hi in spots:
        if (round(x, 3), round(y, 3), cut) in seen:
            continue
        seen.add((round(x, 3), round(y, 3), cut))
        rl, rh, rc = reg(lo), reg(hi), reg(LY[cut])
        if not rc.interacting(dot(x, y)).count():
            short.append(("no cut here", cut, x, y))
            continue
        own = {lo: rl.interacting(dot(x, y)), hi: rh.interacting(dot(x, y))}
        best = None
        for k in range(SIG_CUTS, 1, -1):
            for dx, dy in ((0, -pit), (0, pit), (pit, 0), (-pit, 0)):
                for s in range(k):
                    pts = [(r5(x + (i - s) * dx), r5(y + (i - s) * dy))
                           for i in range(k)]
                    # one solid landing strip: 0.4 um squares on the
                    # 0.52 um cut pitch would leave 0.12 um notches
                    xs_, ys_ = [q[0] for q in pts], [q[1] for q in pts]
                    land = kdb.Region(box(min(xs_) - e, min(ys_) - e,
                                          max(xs_) + e, max(ys_) + e))
                    ok = all(not ((r - own[m]) & land.sized(sp)).count()
                             for m, r in ((lo, rl), (hi, rh)))
                    for i, (px, py) in enumerate(pts):
                        if i != s and (rc & kdb.Region(box(
                                px - h, py - h, px + h, py + h).enlarged(
                                int(round(CUT_SP / dbu)) - 1))).count():
                            ok = False
                    if not ok:
                        continue
                    new = sum((land - own[m]).area() for m in (lo, hi))
                    if best is None or new < best[0]:
                        best = (new, pts, s)
            if best:
                break
        if best is None:
            short.append((cut, x, y))
            continue
        for i, (px, py) in enumerate(best[1]):
            if i != best[2]:
                via(top, px, py, cut, lo, hi)
        xs_, ys_ = [q[0] for q in best[1]], [q[1] for q in best[1]]
        for m in (lo, hi):
            rect(top, min(xs_) - e, min(ys_) - e, max(xs_) + e,
                 max(ys_) + e, m)
        # The landing strip carries the current between the cuts of the
        # array (up to (k-1)/k of it): grow its cross width to SIG_W,
        # sliding toward whichever side clears other nets by 0.3 um.
        col = max(xs_) == min(xs_)
        n = int(round((SIG_W - TRK_W) / 0.02))
        for m in (lo, hi):
            rm = reg(m)
            own_m = rm.interacting(dot(x, y))
            for k in sorted(range(n + 1), key=lambda k: abs(k - n / 2)):
                if col:
                    a = r5(x + e - SIG_W + k * 0.02)
                    bx = (a, min(ys_) - e, a + SIG_W, max(ys_) + e)
                else:
                    a = r5(y + e - SIG_W + k * 0.02)
                    bx = (min(xs_) - e, a, max(xs_) + e, a + SIG_W)
                if not ((rm - own_m) & kdb.Region(
                        box(*bx).enlarged(sp))).count():
                    rect(top, *bx, m)
                    break
            else:
                short.append(("landing width", m, x, y))
                if m == M2 and col:
                    thin.append((x, min(ys_) - e, max(ys_) + e))
        if len(best[1]) < SIG_CUTS:
            short.append((cut, x, y, len(best[1])))
    # A metal2 column that other nets' metal2 keeps at 0.4 um gets a
    # parallel metal3 strap instead: SIG_W wide over the column, run on
    # to the net's own metal3 landing just above or below it and tied
    # down with via2 cuts on the cut pitch, so the column's current
    # shares two layers rather than crowding one 0.4 um wire.
    for x, ya, yb in thin:
        m2, m3, c2 = reg(M2), reg(M3), reg(LY["via2"])
        stub = m2.interacting(dot(x, (ya + yb) / 2))
        own3 = m3.interacting(c2 & stub)
        near = [p.bbox() for p in own3.each()
                if p.bbox().left * dbu < x < p.bbox().right * dbu]
        up = [b.bottom * dbu for b in near if b.bottom * dbu >= yb - 0.01]
        dn = [b.top * dbu for b in near if b.top * dbu <= ya + 0.01]
        y0, y1 = ya, yb
        if up and min(up) - yb < 1.5:
            y1 = min(up) + TRK_W
        elif dn and ya - max(dn) < 1.5:
            y0 = max(dn) - TRK_W
        else:
            short.append(("m3 strap: no own metal3 near", x, ya, yb))
            continue
        n = int(round((SIG_W - TRK_W) / 0.02))
        for k in sorted(range(n + 1), key=lambda k: abs(k - n / 2)):
            a = r5(x + e - SIG_W + k * 0.02)
            if not ((m3 - own3) & kdb.Region(
                    box(a, y0, a + SIG_W, y1).enlarged(sp))).count():
                rect(top, a, y0, a + SIG_W, y1, M3)
                break
        else:
            short.append(("m3 strap: no room", x, ya, yb))
            continue
        placed = 0
        yy = ya + e
        while yy <= yb - e + 1e-6:
            cb = box(x - h, yy - h, x + h, yy + h)
            inside = (kdb.Region(cb.enlarged(int(round(0.07 / dbu))))
                      - stub).is_empty()
            clear = not (c2 & kdb.Region(cb.enlarged(
                int(round(CUT_SP / dbu)) - 1))).count()
            if inside and clear:
                via(top, r5(x), r5(yy), "via2", M2, M3)
                c2 = reg(LY["via2"])
                placed += 1
            yy = r5(yy + pit)
        print("sig_em_arrays: metal3 strap at", round(x, 2), round(y0, 2),
              round(y1, 2), "via2 cuts", placed)
    for s_ in short:
        print("sig_em_arrays: short of room:", s_)


def fill_m3_notches(top):
    """Two via landings on one thinner (ring channel) metal3 track closer
    than M3.2a (0.28) leave a notch between them, inside one shape: fill
    it. The landings can sit in different cells (a ring half's via2 and a
    trunk's via3), so this reads the merged metal3 of the whole top cell.
    A gap between two separate shapes is left alone (a different net).
    The same goes for metal1 (0.23) and metal2 (0.28), where the supply
    landings and rail straps meet. The fill covers only the span where
    the two edges face each other."""
    import klayout.db as kdb

    dbu = top.kcl.dbu
    for m, space in ((M3, 0.28), (M2, 0.28), (M1, 0.23)):
        li = top.kcl.layer(*m)
        reg = kdb.Region(top.kdb_cell.begin_shapes_rec(li)).merged()
        for ep in reg.space_check(int(round(space / dbu))).each():
            a, b = ep.first, ep.second
            if a.dx() == 0 and b.dx() == 0:
                lo = max(min(a.p1.y, a.p2.y), min(b.p1.y, b.p2.y))
                hi = min(max(a.p1.y, a.p2.y), max(b.p1.y, b.p2.y))
                box = kdb.Box(min(a.p1.x, b.p1.x), lo,
                              max(a.p1.x, b.p1.x), hi)
            elif a.dy() == 0 and b.dy() == 0:
                lo = max(min(a.p1.x, a.p2.x), min(b.p1.x, b.p2.x))
                hi = min(max(a.p1.x, a.p2.x), max(b.p1.x, b.p2.x))
                box = kdb.Box(lo, min(a.p1.y, b.p1.y), hi,
                              max(a.p1.y, b.p1.y))
            else:
                continue
            if box.width() <= 0 or box.height() <= 0:
                continue
            if reg.interacting(kdb.Region(box.enlarged(1, 1))).count() != 1:
                continue
            top.kdb_cell.shapes(li).insert(box)


def tbox(b, dx, dy):
    return (b[0] + dx, b[1] + dy, b[2] + dx, b[3] + dy)


def cx(b):
    return (b[0] + b[2]) / 2


def cy(b):
    return (b[1] + b[3]) / 2


class Router:
    """Collects terminals per channel, metal4 ports, then draws tracks,
    stubs, trunks."""

    def __init__(self):
        self.ch = []          # channel dicts, bottom to top
        self.ports = []       # (net, x, y): metal4 points a net must reach
        self.keepout = []     # metal4 keep-out boxes (caps)

    def channel(self, name, base_y):
        c = {"name": name, "base": base_y, "terms": [], "tracks": {},
             "ntracks": 0}
        self.ch.append(c)
        return c


def fet_cell(draw_fet, kind, w, l):
    fn = draw_fet.draw_nfet if kind == "n" else draw_fet.draw_pfet
    return fn(l_gate=l, w_gate=w, gate_con_pos="top")


def fet_geom(cell):
    comp = layoutlib.layer_boxes(cell, LY["comp"])[0]
    m1 = layoutlib.layer_boxes(cell, M1)
    if len(m1) != 3:
        raise layoutlib.LayoutError(f"expected 3 metal1 pads, got {m1}")
    by_y = sorted(m1, key=cy)
    gate = by_y[-1]
    left, right = sorted(by_y[:2], key=lambda b: b[0])
    return comp, {"l": left, "r": right, "g": gate}


def build_row(top, draw_fet, name, kind, items, y0, used):
    """Place one row with its COMP bottom at y0. Returns (terms, top_y,
    bottom_y, x_end, nwell box or None). terms: (net, x, y_start)."""
    terms = []
    x = 0.0
    since_tap = 1e9
    tops, bots = [], []
    lefts, rights = [], []

    def place_tap(x):
        cell = (layoutlib.psub_tap(TAP) if kind == "n"
                else layoutlib.nwell_tap(TAP))
        top.add_ref(cell).move((r5(x), r5(y0)))
        net = "vss" if kind == "n" else "vdd"
        via(top, x + TAP / 2, y0 + TAP / 2, "via1", M1, M2)
        terms.append((net, x + TAP / 2, y0 + TAP / 2))
        tops.append(y0 + TAP + 0.2)
        bots.append(y0 - 0.2)
        lefts.append(x)
        rights.append(x + TAP)
        return x + TAP + GAP

    seq = list(items)
    if seq[0] != "T":
        seq.insert(0, "T")
    if seq[-1] != "T":
        seq.append("T")
    for it in seq:
        if it == "T":
            x = place_tap(x)
            since_tap = 0.0
            continue
        typ, d, g, s, wt, l, nu = DEV[it]
        assert typ == kind, (it, kind)
        w = wt / nu
        cell = fet_cell(draw_fet, kind, w, l)
        comp, pads = fet_geom(cell)
        cw = comp[2] - comp[0]
        if since_tap + cw > TAP_RUN:
            x = place_tap(x)
            since_tap = 0.0
        dx, dy = r5(x - comp[0]), r5(y0 - comp[1])
        top.add_ref(cell).move((dx, dy))
        used[it] = used.get(it, 0) + 1
        p = {k: tbox(v, dx, dy) for k, v in pads.items()}
        bb = cell.dbbox()
        tops.append(bb.top + dy)
        bots.append(bb.bottom + dy)
        lefts.append(x)
        rights.append(x + cw)
        # left pad = source, right pad = drain (gate==drain ties right)
        lp, rp, gp = p["l"], p["r"], p["g"]
        for net, pad in ((s, lp), (d, rp)):
            via(top, cx(pad), pad[3] - 0.2, "via1", M1, M2)
            terms.append((net, cx(pad), pad[3] - 0.2))
            if net in SUP_NETS:
                # a supply pad's device current (up to 0.2 mA at the
                # worst corner, 0.3 with 1.5x margin) needs two cuts at
                # 0.18 mA a cut: more down the pad where it is tall enough
                yc = pad[3] - 0.2
                for k in (1, 2):
                    yk = r5(yc - k * (CUT + CUT_SP))
                    if yk - 0.13 < pad[1] + 0.06:
                        break
                    via(top, cx(pad), yk, "via1", M1, M2)
                    for lay in (M1, M2):
                        rect(top, cx(pad) - TRK_W / 2, yk,
                             cx(pad) + TRK_W / 2, yc, lay)
        xg = cx(rp) + GOFF
        rect(top, gp[0], gp[1], xg + TRK_W / 2, gp[3], M1)
        if g == d:
            rect(top, rp[0], rp[3] - 0.3, rp[2], gp[3], M1)
        else:
            via(top, xg, cy(gp), "via1", M1, M2)
            terms.append((g, xg, cy(gp)))
        tops.append(gp[3] + 0.3)
        x = x + cw + GAP
        since_tap += cw + GAP
    nw = None
    if kind == "p":
        nwb = layoutlib.layer_boxes(top, LY["nwell"])
        nw = (min(lefts) - 1.1, y0 - 0.8, max(rights) + 1.1,
              max(b[3] for b in nwb if b[1] >= y0 - 1.0))
        rect(top, *nw, LY["nwell"])
        bots.append(nw[1])
        tops.append(nw[3])
    return terms, max(tops), min(bots), x - GAP


def build_res_row(top, draw_res, y0):
    """Every resistor as a serpentine of vertical ppolyf_u segments, body
    bottom at y0. Even segment counts put both chain ends on top heads.
    Returns (terms, top_y, bottom_y, x_end)."""
    terms = []
    x = 2.0                      # room for the substrate strap's stub
    subs = []
    tops, bots = [], []
    for rname in RES_ORDER:
        a, b, w, ltot, nseg = RES[rname]
        assert nseg % 2 == 0
        lseg = ltot / nseg
        cell = draw_res.draw_ppolyf_res(l_res=lseg, w_res=w,
                                        res_type="ppolyf_u")
        m1 = layoutlib.layer_boxes(cell, M1)
        heads0 = [bb for bb in m1 if -1.0 < bb[0] < 0]
        heads1 = [bb for bb in m1 if bb[0] > lseg]
        subp = [bb for bb in m1 if bb[2] < -1.0]
        pitch = RES_P[w]
        heads = []
        for i in range(nseg):
            # rotate +90: (x, y) -> (-y, x); body lands at x-w..x
            ref = top.add_ref(cell)
            ref.rotate(90)
            ox, oy = r5(x + w), r5(y0)
            ref.move((ox, oy))
            rot = lambda bb: (-bb[3] + ox, bb[0] + oy, -bb[1] + ox, bb[2] + oy)
            h0 = [rot(bb) for bb in heads0]
            h1 = [rot(bb) for bb in heads1]
            hb = (min(q[0] for q in h0), min(q[1] for q in h0),
                  max(q[2] for q in h0), max(q[3] for q in h0))
            ht = (min(q[0] for q in h1), min(q[1] for q in h1),
                  max(q[2] for q in h1), max(q[3] for q in h1))
            heads.append((hb, ht))
            subs += [rot(bb) for bb in subp]
            bb = ref.dbbox()
            tops.append(bb.top)
            bots.append(bb.bottom)
            x += pitch
        for i in range(nseg - 1):
            k = 0 if i % 2 == 0 else 1   # bottom strap after even segs
            p, q = heads[i][k], heads[i + 1][k]
            rect(top, p[0], p[1], q[2], p[3], M1)
        for net, hd in ((a, heads[0][1]), (b, heads[-1][1])):
            # head pads are 0.38 tall: widen the via landing's metal1
            via(top, cx(hd), cy(hd), "via1", M1, M2)
            terms.append((net, cx(hd), cy(hd)))
        x += RES_GAP
    # substrate straps: one metal1 bar over every segment's own P+ tap
    sy0 = min(s[1] for s in subs)
    sy1 = max(s[3] for s in subs)
    rect(top, 0.6, sy0, max(s[2] for s in subs), sy1, M1)
    via(top, 0.8, cy((0, sy0, 0, sy1)), "via1", M1, M2)
    terms.append(("vss", 0.8, cy((0, sy0, 0, sy1))))
    return terms, max(tops), min(bots), x - RES_GAP


RAIL = (-1.7, -1.1)     # a ring-block metal1 supply rail, from S COMP bottom
RTAP_Y = -2.2           # its taps' COMP bottom, from S COMP bottom
RTAP_P = 8.0            # tap pitch along a rail
RWELL_Y = -2.6          # PMOS half nwell bottom, from S COMP bottom
NEXT_X = 0.6            # COMP right edge to the next column's left pad,
NEXT_XR = 0.6           # stage or NAND/output: no jog reaches past COMP
STRAP_Y = -0.6          # metal2 strap joining an inverter's n_k/p_k pads
MINI_Y = -1.6           # metal3 starve-gate track (vbn_vco / vbp_vco)
RING_CH_IN = 0.6        # inverter-row top shape to the first ring track
S_TOP = -3.2            # starve-device COMP top (inverter COMP bottom = 0)

# ring-block devices drawn as multi-finger cells: the stage inverter
# (n_k | r_k | n_k) halves each ring node's drain diffusion, and every
# inverter-row device is about the same height, so the shared channel is
# close to all of them
RING_NF = {f"M{t}_{d}{k}": 2 for t in "NP" for d in "SI" for k in range(1, 6)}
RING_NF.update({d: 2 for d in ("MP_G1", "MP_G2", "MN_G1", "MN_G2", "MP_O",
                               "MN_O", "MP_DO2", "MN_DO2")})


def fet_geom_nf(cell, nf):
    """COMP box, S/D pads left to right, gate pads, of a top-contacted
    draw_nfet/draw_pfet with nf fingers."""
    comp = layoutlib.layer_boxes(cell, LY["comp"])[0]
    m1 = layoutlib.layer_boxes(cell, M1)
    if len(m1) != 2 * nf + 1:
        raise layoutlib.LayoutError(f"expected {2 * nf + 1} pads: {m1}")
    by_y = sorted(m1, key=cy)
    gates = sorted(by_y[nf + 1:], key=lambda b: b[0])
    sd = sorted(by_y[:nf + 1], key=lambda b: b[0])
    return comp, sd, gates


def ring_dev_cell(draw_fet, dev):
    kind, _d, _g, _s, wt, l, nu = DEV[dev]
    nf = RING_NF.get(dev, 1)
    fn = draw_fet.draw_nfet if kind == "n" else draw_fet.draw_pfet
    # inner S/D long enough for its contacts (CO.7) and for neighbouring
    # top gate pads to clear each other (PL.3a); the cell's 0.24 is not
    return fn(l_gate=l, w_gate=wt / nu / nf, nf=nf, gate_con_pos="top",
              inter_sd_l=0.52), nf


def fin_w(dev):
    """A ring-block device's finger width: its COMP height."""
    _k, _d, _g, _s, wt, _l, nu = DEV[dev]
    return wt / nu / RING_NF.get(dev, 1)


def gate_right(dev):
    """True when the left pad's net is neither a rail nor a strap net, so a
    gate via over it would sit on that pad's own channel stub."""
    return DEV[dev][3] not in ("vdd", "vss") and DEV[dev][3] not in INTERNAL


def dev_width(draw_fet, dev):
    cell, nf = ring_dev_cell(draw_fet, dev)
    comp, sd, _g = fet_geom_nf(cell, nf)
    right = comp[2]
    if gate_right(dev):
        right = max(right, sd[-1][2] + GOFF + TRK_W / 2)
    return right - comp[0]


def ring_place(top, draw_fet, dev, xl, ybot, used, imps):
    """Place dev with its left pad at x=xl and COMP bottom at ybot; draw
    its gate jog and gate via (over the left pad). Returns (pads,
    nets per pad, gate net, gate via (x, y), COMP box); its implant box
    goes on imps."""
    typ, d, g, s, wt, l, nu = DEV[dev]
    cell, nf = ring_dev_cell(draw_fet, dev)
    comp, sd, gps = fet_geom_nf(cell, nf)
    dx, dy = r5(xl - sd[0][0]), r5(ybot - comp[1])
    top.add_ref(cell).move((dx, dy))
    used[dev] = used.get(dev, 0) + 1
    sd = [tbox(b, dx, dy) for b in sd]
    gps = [tbox(b, dx, dy) for b in gps]
    nets = [s if k % 2 == 0 else d for k in range(nf + 1)]
    imp = LY["nplus"] if typ == "n" else LY["pplus"]
    imps.extend(tbox(b, dx, dy) for b in layoutlib.layer_boxes(cell, imp))
    gy0, gy1 = gps[0][1], gps[0][3]
    if gate_right(dev):
        # both pads' nets go to the channel (a pass gate): the gate via
        # sits GOFF right of the right pad instead, as in the other rows
        xg = sd[-1][2] + GOFF
        rect(top, gps[0][0], gy0, xg + TRK_W / 2, gy1, M1)
    else:
        # the gate via sits over the left pad, whose net leaves away from
        # the channel, so the jog is no longer than the gate pads' own span
        xg = cx(sd[0])
        rect(top, xg - TRK_W / 2, gy0, gps[-1][2], gy1, M1)
    via(top, xg, (gy0 + gy1) / 2, "via1", M1, M2)
    return sd, nets, g, (xg, (gy0 + gy1) / 2), tbox(comp, dx, dy)


def ring_half(top, draw_fet, kind, cols, used):
    """One half of the ring block in its own frame, gates toward the
    shared channel above:
      inverter row   COMP top at the stage inverters' (bottom y=0):
                     stage inverters, NAND, output
      n_k/p_k strap  metal2 at STRAP_Y under each stage inverter
      starve track   metal3 at MINI_Y: vbn_vco (or vbp_vco)
      starve row     COMP top at S_TOP, under its stage's inverter
      rail           metal1 + taps under the starve row
    cols: [(x, starve dev or None, [inverter-row devs])]. Returns (terms
    [(net, x, y)] for the shared channel, inverter row top y, x end,
    rail (x0, y), starve track (x0, y), bottom y)."""
    rail_net = "vss" if kind == "n" else "vdd"
    sdev = next(c[1] for c in cols if c[1])
    s_w = DEV[sdev][4] / DEV[sdev][6] / RING_NF[sdev]
    s_bot = S_TOP - s_w
    rail_y = (s_bot + RAIL[0], s_bot + RAIL[1])
    terms, tops, xmax = [], [0.0], 0.0
    mini_xs = []
    imps = []                      # implant boxes of the devices placed
    # every inverter-row device ends at the stage inverters' top, so a
    # taller one (NAND, output inverter) reaches away from the channel
    # and no stub crossing it is longer for its sake
    h_inv = max(fin_w(d) for c in cols if c[1] for d in c[2])
    straps = {}                    # internal net -> pad xs on its strap
    sig_local = []                 # SIG_EM source/drain via1s (x, y)

    def tie(net, pad):
        if net == rail_net:
            rect(top, pad[0], rail_y[1], pad[2], pad[1] + 0.2, M1)
            return True
        return False

    for x, sdv, idevs in cols:
        xi = x
        for dev in idevs:
            sd, nets, g, (xg, yg), comp = ring_place(
                top, draw_fet, dev, xi, h_inv - fin_w(dev), used, imps)
            for net, pad in zip(nets, sd):
                if tie(net, pad):
                    continue
                if net in INTERNAL:
                    via(top, cx(pad), pad[1] + 0.2, "via1", M1, M2)
                    hw, yb = TRK_W / 2, STRAP_Y - TRK_W / 2
                    if net == "ng":
                        hw, yb = SIG_W / 2, STRAP_Y + TRK_W / 2 - 0.2 \
                            - NG_STRAP_W
                    rect(top, cx(pad) - hw, yb, cx(pad) + hw,
                         pad[1] + 0.2, M2)
                    straps.setdefault(net, []).append(cx(pad))
                    if net in SIG_EM:
                        sig_local.append((cx(pad), pad[1] + 0.2))
                else:
                    via(top, cx(pad), pad[3] - 0.2, "via1", M1, M2)
                    terms.append((net, cx(pad), pad[3] - 0.2))
                    if net in SIG_EM:
                        sig_local.append((cx(pad), pad[3] - 0.2))
            terms.append((g, xg, yg))
            if sdv is not None:
                # the starve device's n_k/p_k pad(s) join this strap
                ssd, snets, sg, (sxg, syg), scomp = ring_place(
                    top, draw_fet, sdv, xi, s_bot, used, imps)
                for net, pad in zip(snets, ssd):
                    if tie(net, pad):
                        continue
                    assert net in INTERNAL, (sdv, net)
                    via(top, cx(pad), pad[3] - 0.2, "via1", M1, M2)
                    rect(top, cx(pad) - TRK_W / 2, pad[3] - 0.2,
                         cx(pad) + TRK_W / 2, STRAP_Y + TRK_W / 2, M2)
                    straps.setdefault(net, []).append(cx(pad))
                assert sg in ("vbn_vco", "vbp_vco"), sdv
                rect(top, sxg - RING_LW / 2, syg, sxg + RING_LW / 2,
                     MINI_Y + TRK_W / 2, M2)
                via(top, sxg, MINI_Y, "via2", M2, M3)
                mini_xs.append(sxg)
                xmax = max(xmax, scomp[2], sxg + 0.2)
            tops.append(max(b[3] for b in sd) + 0.9)
            xmax = max(xmax, comp[2], xg + 0.2)
            xi = max(comp[2], xg + TRK_W / 2) + NEXT_XR
    # neighbouring columns sit closer than implant spacing (NP.2/PP.2):
    # one implant fills the gap between two devices that face each other
    for a in imps:
        for b in imps:
            y0, y1 = max(a[1], b[1]), min(a[3], b[3])
            if 0 < b[0] - a[2] < 0.4 and y1 > y0:
                rect(top, a[2], y0, b[0], y1,
                     LY["nplus" if kind == "n" else "pplus"])
    for net, xs in straps.items():
        if net == "ng":
            # moved 0.2 down, clear of the nb pad cuts above it
            yt = STRAP_Y + TRK_W / 2 - 0.2
            rect(top, min(xs) - SIG_W / 2, yt - NG_STRAP_W,
                 max(xs) + SIG_W / 2, yt, M2)
            continue
        rect(top, min(xs) - TRK_W / 2, STRAP_Y - TRK_W / 2,
             max(xs) + TRK_W / 2, STRAP_Y + TRK_W / 2, M2)
    x0 = min(c[0] for c in cols) - 3.0
    rect(top, x0, rail_y[0], xmax + 1.0, rail_y[1], M1)
    tap = layoutlib.psub_tap(TAP) if kind == "n" else layoutlib.nwell_tap(TAP)
    xt = x0 + 0.4
    while xt + TAP <= xmax + 1.0:
        top.add_ref(tap).move((r5(xt), r5(s_bot + RTAP_Y)))
        xt += RTAP_P
    rect(top, min(mini_xs) - TRK_W / 2, MINI_Y - RING_LW / 2,
         max(mini_xs) + TRK_W / 2, MINI_Y + RING_LW / 2, M3)
    bottom = s_bot + (RWELL_Y if kind == "p" else RTAP_Y - 0.2)
    if kind == "p":
        nwb = layoutlib.layer_boxes(top, LY["nwell"])
        rect(top, x0 - 0.8, bottom, xmax + 1.8, max(b[3] for b in nwb),
             LY["nwell"])
    # inverter-row gate pads are the tallest shapes facing the channel
    top.info["sig_local"] = sig_local
    return (terms, max(tops), xmax, (x0, (rail_y[0] + rail_y[1]) / 2),
            (min(mini_xs), MINI_Y), bottom)


def ring_block(top, draw_fet, y0, x0, ntracks, used):
    """The VCO: NMOS half (gates up) under one shared channel, PMOS half
    mirrored above it (gates down). Each stage is one column: inverter
    next to the channel, starve device behind it, so stages are narrow,
    every ring hop is a short metal3 track and the starve gates stay off
    the ring channel. Returns (terms [(net, x, y, side)], channel base y,
    block top y, block bottom y, x end, risers [(net, x0, y, layer)])."""
    import gdsfactory as gf

    ncols, pcols = [], []
    x = x0
    prev_stage = False
    for col in RING_COLS:
        if col[0] == "stage":
            k = col[1]
            w = max(dev_width(draw_fet, d) for d in
                    (f"MN_S{k}", f"MN_I{k}", f"MP_S{k}", f"MP_I{k}"))
            ncols.append((x, f"MN_S{k}", [f"MN_I{k}"]))
            pcols.append((x, f"MP_S{k}", [f"MP_I{k}"]))
            x += w + NEXT_X
            # the stage's power-down hold on p_k sits beside it, on the
            # same p_k strap, gate on pll_en in the shared channel
            pcols.append((x, None, [f"MP_HP{k}"]))
            x += dev_width(draw_fet, f"MP_HP{k}") + NEXT_X
            prev_stage = True
        else:
            _t, ng, pg = col
            x += NEXT_XR - NEXT_X if prev_stage else 0.0
            prev_stage = False
            for i in range(max(len(ng), len(pg))):
                w = max(dev_width(draw_fet, g[i]) for g in (ng, pg)
                        if i < len(g))
                if i < len(ng):
                    ncols.append((x, None, [ng[i]]))
                if i < len(pg):
                    pcols.append((x, None, [pg[i]]))
                x += w + NEXT_XR
    nh = gf.Component()
    nterms, ntop, nxe, nrail, nmini, nbot = ring_half(nh, draw_fet, "n",
                                                      ncols, used)
    ph = gf.Component()
    pterms, ptop, pxe, prail, pmini, pbot = ring_half(ph, draw_fet, "p",
                                                      pcols, used)
    top.add_ref(nh).move((0, r5(y0)))
    base = r5(y0 + ntop + RING_CH_IN)
    ct = base + max(ntracks - 1, 0) * RING_TRK_P + TRK_W / 2
    yp = r5(ct + RING_CH_IN + ptop)
    ref = top.add_ref(ph)
    ref.dmirror_y(0)
    ref.dmove((0, yp))
    SIG_SPOTS.extend((xx, r5(y0 + yy), "via1", M1, M2)
                     for xx, yy in nh.info["sig_local"])
    SIG_SPOTS.extend((xx, r5(yp - yy), "via1", M1, M2)
                     for xx, yy in ph.info["sig_local"])
    terms = [(n, xx, y0 + yy, "below") for n, xx, yy in nterms]
    terms += [(n, xx, yp - yy, "above") for n, xx, yy in pterms]
    risers = [("vss", nrail[0], y0 + nrail[1], "m1"),
              ("vdd", prail[0], yp - prail[1], "m1"),
              ("vbn_vco", nmini[0], y0 + nmini[1], "m3"),
              ("vbp_vco", pmini[0], yp - pmini[1], "m3")]
    return (terms, base, yp - pbot, y0 + nbot, max(nxe, pxe), risers)


# ---------------------------------------------------------------- routing
def plan(chan_terms, x_rows, keepouts, ports):
    """Topological routing plan from each channel's terminals (x only).

    chan_terms: [[(net, x, y_local)], ...] bottom to top.
    keepouts: [(ch_lo, ch_hi, xa, xb)]: no metal4 column in xa..xb for a
      trunk whose channel span meets ch_lo..ch_hi.
    ports: [(key, net, channel, x_pref)]: a metal4 column on the net's own
      track in `channel`, as near x_pref as the keep-outs allow.
    Returns (trunks {net: (x, lo, hi)}, port_x {key: x}, tracks
    [{net: (i, x0, x1)}], ntracks [n], x_right)."""
    nch = len(chan_terms)
    where = {}
    for ci, terms in enumerate(chan_terms):
        for net, x, *_r in terms:
            where.setdefault(net, {}).setdefault(ci, []).append(x)
    occ = []                       # (column k, lo, hi)
    kmax = int((x_rows + 60.0) / TRK_P)

    def column(want, lo, hi, what, hw=TRK_W / 2):
        # hw: the column's half width; two columns clear each other by the
        # 0.4 a pair of TRK_W columns at TRK_P leaves
        k0 = min(max(int(round((want - 0.4) / TRK_P)), 0), kmax)
        for dk in range(0, 2 * kmax + 2):
            k = k0 + (dk + 1) // 2 * (1 if dk % 2 else -1)
            if not 0 <= k <= kmax:
                continue
            x = 0.4 + k * TRK_P
            grow = hw - TRK_W / 2
            if any(xa - grow <= x <= xb + grow and lo <= chi and clo <= hi
                   for clo, chi, xa, xb in keepouts):
                continue
            if all(not (abs(x - ox) < hw + ohw + 0.4 - 1e-6
                        and lo <= ohi + 1 and olo <= hi + 1)
                   for ox, ohw, olo, ohi in occ):
                occ.append((x, hw, lo, hi))
                return r5(x)
        raise layoutlib.LayoutError(f"no metal4 column for {what}")

    port_x = {}
    for key, net, ci, want, *lo in ports:
        if ci not in where.get(net, {}):
            raise layoutlib.LayoutError(
                f"port {key}: {net} has no track in channel {ci}")
        port_x[key] = column(want, lo[0] if lo else ci, ci, key)
    trunks = {}
    # the supply trunks first: they are the widest, and their feet are pins
    for net in sorted(where, key=lambda n: (n not in SUP_NETS,
                                            -len(where[n]), n)):
        chans = sorted(where[net])
        if len(chans) < 2 and net not in BOTTOM_PINS:
            continue
        lo = -1 if net in BOTTOM_PINS else chans[0]
        hi = chans[-1]
        xs = sorted(x for c in chans for x in where[net][c])
        hw = SUP_M4_W / 2 if net in SUP_NETS else TRK_W / 2
        trunks[net] = (column(xs[len(xs) // 2], lo, hi, net, hw), lo, hi)
    x_right = r5(max([x_rows] + [x for x, _l, _h in trunks.values()]
                     + list(port_x.values())) + 1.5)
    tracks, ntracks = [], []
    for ci in range(nch):
        iv = {}
        for net, xs in ((n, w[ci]) for n, w in where.items() if ci in w):
            pts = list(xs)
            if net in trunks:
                pts.append(trunks[net][0])
            pts += [port_x[k] for k, n, c, *_w in ports
                    if (n, c) == (net, ci)]
            if net in RIGHT_PINS and ci == min(where[net]):
                pts.append(x_right)
            iv[net] = [min(pts) - TRK_W / 2, max(pts) + TRK_W / 2]
            if net in SUP_NETS and net in trunks:
                # the track runs the trunk's full width (its via3 array)
                tx = trunks[net][0]
                iv[net] = [min(iv[net][0], tx - SUP_M4_W / 2),
                           max(iv[net][1], tx + SUP_M4_W / 2)]
        sides = [t for t in chan_terms[ci] if len(t) == 4]
        if sides:
            # a shared channel (stubs from below AND above): one track per
            # net, ordered so a stub from below never crosses a stub from
            # above of another net at the same x
            assign = vcg_tracks(sides, iv)
            tracks.append(assign)
            ntracks.append(max(t for t, _a, _b in assign.values()) + 1)
            continue
        last = []
        assign = {}
        for net in sorted(iv, key=lambda n: (iv[n][0], n)):
            a, b = iv[net]
            for t, end in enumerate(last):
                if a >= end + 0.4:
                    last[t] = b
                    break
            else:
                t = len(last)
                last.append(b)
            assign[net] = (t, r5(a), r5(b))
        tracks.append(assign)
        ntracks.append(len(last))
    return trunks, port_x, tracks, ntracks, x_right


def vcg_tracks(terms, iv):
    """Track per net for a two-sided channel: net a's track below net b's
    wherever a stub of a from below and a stub of b from above come
    within metal2 spacing in x. Raises on a cycle."""
    below = [(n, x) for n, x, _y, sd in terms if sd == "below"]
    above = [(n, x) for n, x, _y, sd in terms if sd == "above"]
    succ = {n: set() for n in iv}
    for a, xa in below:
        for b, xb in above:
            if a != b and abs(xa - xb) < TRK_W + 0.3:
                succ[a].add(b)
    indeg = {n: 0 for n in iv}
    for a in succ:
        for b in succ[a]:
            indeg[b] += 1
    # Kahn, ties broken by the net's mean stub side (below-only first)
    side = {n: 0.0 for n in iv}
    for n, _x, _y, sd in terms:
        side[n] += 1 if sd == "above" else -1
    order, ready = [], sorted((n for n in iv if indeg[n] == 0),
                              key=lambda n: (side[n], n))
    while ready:
        n = ready.pop(0)
        order.append(n)
        for b in succ[n]:
            indeg[b] -= 1
            if indeg[b] == 0:
                ready.append(b)
        ready.sort(key=lambda n: (side[n], n))
    if len(order) != len(iv):
        raise layoutlib.LayoutError(
            f"shared channel has a stub conflict cycle among "
            f"{sorted(set(iv) - set(order))}")
    # constrained left-edge: in that order, each net takes the lowest
    # track above all its predecessors' where its span is free, so the
    # channel - and every ring stub crossing it - stays short
    pred = {n: [a for a in succ if n in succ[a]] for n in iv}
    used = []                      # per track: [(x0, x1)]
    got = {}
    for n in order:
        t = max([got[a] + 1 for a in pred[n]] + [0])
        a, b = iv[n]
        while True:
            while t >= len(used):
                used.append([])
            if all(b + 0.4 <= u0 or a >= u1 + 0.4 for u0, u1 in used[t]):
                break
            t += 1
        used[t].append((a, b))
        got[n] = t
    return {n: (got[n], r5(iv[n][0]), r5(iv[n][1])) for n in iv}


def cap_cell(name):
    """The PDK cap_nmos_b cell for one unit of cap `name`, its COMP box and
    its two metal1 terminals: the gate plate over the poly, and the n+
    diffusion's U (a strip each side of the poly, joined under it)."""
    from cells.draw_cap_mos import draw_cap_mos
    _g, _sd, wt, lc, nu = CAPS[name]
    cell = draw_cap_mos(type="cap_nmos_b", lc=lc, wc=r5(wt / nu), volt="3.3V")
    comp = layoutlib.layer_boxes(cell, LY["comp"])[0]
    m1 = layoutlib.layer_boxes(cell, M1)
    if len(m1) != 2:
        raise layoutlib.LayoutError(f"{name}: expected 2 metal1 shapes, got {m1}")
    sd, gate = sorted(m1, key=lambda b: b[0])
    return cell, comp, gate, sd


def build_cap_row(top, items, y0, used):
    """One row of MOS cap units, COMP bottoms at y0, under one nwell (every
    unit's n+ side is vss). Each unit's gate goes up from the top of its
    plate, its n+ side from the top of the U's left strip. Returns (terms,
    top_y, bottom_y, x_end) as build_row does."""
    terms, tops, bots, nws = [], [], [], []
    x = 0.0
    for it in items:
        gnet, sdnet, *_r = CAPS[it]
        cell, comp, gate, sd = cap_cell(it)
        dx, dy = r5(x - comp[0]), r5(y0 - comp[1])
        top.add_ref(cell).move((dx, dy))
        used[it] = used.get(it, 0) + 1
        gate, sd = tbox(gate, dx, dy), tbox(sd, dx, dy)
        xs, ys = r5(sd[0] + 0.5), r5(sd[3] - 0.3)
        via(top, xs, ys, "via1", M1, M2)
        terms.append((sdnet, xs, ys))
        xg, yg = r5(cx(gate)), r5(gate[3] - 0.3)
        via(top, xg, yg, "via1", M1, M2)
        terms.append((gnet, xg, yg))
        bb = cell.dbbox()
        tops.append(max(bb.top + dy, gate[3] + 0.3))
        bots.append(bb.bottom + dy)
        nws += [b for b in (tbox(b, dx, dy) for b in
                            layoutlib.layer_boxes(cell, LY["nwell"]))]
        x = x + (comp[2] - comp[0]) + CAP_GAP
    rect(top, min(b[0] for b in nws), min(b[1] for b in nws),
         max(b[2] for b in nws), max(b[3] for b in nws), LY["nwell"])
    return terms, max(tops), min(bots), x - CAP_GAP


def generate():
    import gdsfactory as gf

    draw_fet, draw_res = layoutlib.gf180_cells()

    # ---- pass 1: terminals (x) and row extents, in a scratch cell ----
    scratch = gf.Component()
    used = {}
    rows1 = []
    for name, kind, items in ROWS:
        if kind == "ring":
            rows1.append(None)
        elif kind == "r":
            rows1.append(build_res_row(scratch, draw_res, 0.0))
        elif kind == "c":
            rows1.append(build_cap_row(scratch, items, 0.0, used))
        else:
            rows1.append(build_row(scratch, draw_fet, name, kind, items,
                                   0.0, used))
    # the ring block goes flush right, under the vco_div2 pin's edge
    x_rows0 = max(r[3] for r in rows1 if r)
    rw = ring_block(gf.Component(), draw_fet, 0.0, 0.0, 0, {})[4]
    ring_x0 = r5(max(x_rows0 - rw, 0.0))
    for ri, (name, kind, items) in enumerate(ROWS):
        if kind == "ring":
            t, b, tp, bt, xe, rails = ring_block(scratch, draw_fet, 0.0,
                                                 ring_x0, 0, used)
            rows1[ri] = (t, b - CH_IN, bt, xe)
            ring_ri, ring_rails = ri, rails
    for dev, nu in [(d, v[6]) for d, v in DEV.items()] + \
            [(c, v[4]) for c, v in CAPS.items()]:
        if used.get(dev, 0) != nu:
            raise layoutlib.LayoutError(
                f"{dev}: {used.get(dev, 0)} units placed, {nu} wanted")
    nch = len(rows1)
    x_rows = max(r[3] for r in rows1)
    keepouts, ports = [], []
    # ring rails: a metal4 riser from each rail's left end up to the
    # first channel above the block that carries the same supply
    for net, rx, _ry, _lay in ring_rails:
        ci = min(c for c in range(ring_ri + 1, nch)
                 if any(t[0] == net for t in rows1[c][0]))
        ports.append((f"ring.{net}", net, ci, rx, ring_ri))
    trunks, port_x, tracks, ntracks, x_right = plan(
        [r[0] for r in rows1], x_rows, keepouts, ports)

    if os.environ.get("PLL_LAYOUT_DEBUG"):
        for ci, tr in enumerate(tracks):
            print("channel", ci, ROWS[ci][0], ntracks[ci],
                  sorted((t, n, round(b - a, 1)) for n, (t, a, b)
                         in tr.items()), file=sys.stderr)
    # ---- pass 2: draw ----
    # the sizing passes above drew rings into scratch cells: their spots
    # are not on this layout
    SIG_SPOTS.clear()
    SIG_STUBS.clear()
    top = gf.Component()
    used = {}
    y0 = 0.0
    row_y0, chan_y, chan_top, bottoms, chan_p = [], [], [], [], []
    sup_band = {}                  # (net, channel) -> (y0, y1) of a wide track
    taps = []                      # supply stubs onto a wide track
    stacks = []                    # supply via stacks: (x, y, cuts)
    for ri in range(nch):
        row_y0.append(y0)
        name, kind, items = ROWS[ri]
        blk_top = None
        if kind == "ring":
            terms, base, blk_top, by, xe, rails2 = ring_block(
                top, draw_fet, y0, ring_x0, ntracks[ri], used)
            ring_xe = xe
        else:
            if kind == "r":
                terms, ty, by, xe = build_res_row(top, draw_res, y0)
            elif kind == "c":
                terms, ty, by, xe = build_cap_row(top, items, y0, used)
            else:
                terms, ty, by, xe = build_row(top, draw_fet, name, kind,
                                              items, y0, used)
            base = r5(ty + CH_IN)
        bottoms.append(by)
        chan_y.append(base)
        pch = RING_TRK_P if kind == "ring" else TRK_P
        lw = RING_LW if kind == "ring" else TRK_W
        chan_p.append(pch)
        done = {}
        for net, x, y, *_sd in terms:
            yt = base + tracks[ri][net][0] * pch
            ya, yb = sorted((y, yt))
            rect(top, x - lw / 2, ya - TRK_W / 2 * (y > yt),
                 x + lw / 2, yb + TRK_W / 2 * (yt > y), M2)
            if kind == "ring" and net in SIG_WIDE:
                SIG_STUBS.append((x, ya, yb))
            # an n stub and a p stub of one net meeting a few 10 nm apart
            # share the first one's via2 (two would merge into a bad cut)
            if any(abs(x - x2) < 0.7 for x2 in done.get(net, [])):
                continue
            done.setdefault(net, []).append(x)
            if net in SUP_NETS and kind != "ring":
                # a supply tap: its via2 array goes in once every stub is
                # drawn (widen_supply_taps)
                taps.append((net, x, r5(yt + TRK_W / 2 - SUP_M3_W),
                             r5(yt + TRK_W / 2)))
                continue
            via(top, x, yt, "via2", M2, M3)
            if kind == "ring" and net in SIG_EM:
                SIG_SPOTS.append((x, yt, "via2", M2, M3))
        for net, (t, a, b) in tracks[ri].items():
            yt = base + t * pch
            if net in SUP_NETS and kind != "ring":
                if t != 0:
                    raise layoutlib.LayoutError(
                        f"{net} is track {t} in channel {name}: a wide "
                        "supply track must be the channel's first")
                band = (r5(yt + TRK_W / 2 - SUP_M3_W), r5(yt + TRK_W / 2))
                sup_band[(net, ri)] = band
                rect(top, a, band[0], b, band[1], M3)
                continue
            rect(top, a, yt - lw / 2, b, yt + lw / 2, M3)
        ch_top = base + max(ntracks[ri] - 1, 0) * pch + TRK_W / 2
        chan_top.append(ch_top)
        if blk_top is not None:
            ch_top = blk_top       # the ring block's PMOS half sits above
        if ri + 1 < nch:
            y0 = r5(ch_top + ROW_SP - rows1[ri + 1][2])
    y_bot = r5(min(bottoms) - 1.5)

    def track_y(net, ci):
        return chan_y[ci] + tracks[ci][net][0] * chan_p[ci]

    # ---- trunks ----
    labels = []
    feet = []
    for net, (x, lo, hi) in trunks.items():
        ys = [track_y(net, ci) for ci in range(max(lo, 0), hi + 1)
              if net in tracks[ci]]
        hw = SUP_M4_W / 2 if net in SUP_NETS else TRK_W / 2
        cis = [ci for ci in range(max(lo, 0), hi + 1) if net in tracks[ci]]
        for ci, y in zip(cis, ys):
            if (net, ci) in sup_band:
                b0, b1 = sup_band[(net, ci)]
                via_array(top, x - hw, b0, x + hw, b1, "via3", M3, M4)
            elif net in SUP_NETS:
                # a narrow supply track (the ring channel's) meets the
                # trunk: an array too, sized in widen_supply_stacks
                stacks.append((x, y, (("via3", M3, M4),)))
            else:
                via(top, x, y, "via3", M3, M4)
        ya = y_bot if lo < 0 else min(ys)
        rect(top, x - hw, ya - TRK_W / 2, x + hw,
             max(ys) + TRK_W / 2, M4)
        if lo < 0:
            # pin: the trunk's foot, stacked down to a metal2 pad (the
            # abstract reads metal1/metal2 pin labels)
            if net in SUP_NETS:
                # widened and given its pad arrays once every column is in
                first = min(ci for ci in cis if (net, ci) in sup_band)
                feet.append((net, x, hw, y_bot - TRK_W / 2,
                             sup_band[(net, first)][1],
                             y_bot - TRK_W / 2 + SUP_FOOT_H))
            else:
                via(top, x, y_bot, "via3", M3, M4)
                via(top, x, y_bot, "via2", M2, M3)
            labels.append((net, x, y_bot, LY["metal2_label"]))
    rail_straps = []
    for net, rx, ry, lay in rails2:
        key = f"ring.{net}"
        if os.environ.get("PLL_LAYOUT_DEBUG"):
            print("riser", net, rx, ry, lay, port_x[key], file=sys.stderr)
        ci = [c for k, _n, c, *_r in ports if k == key][0]
        px = port_x[key]
        if lay == "m1":
            # a supply rail: metal1 out to the riser, via1/2/3 stack; it
            # carries the whole ring's current, so each end is a cut array
            # (widen_supply_stacks)
            if px < rx:
                rect(top, px - TRK_W / 2, ry - 0.3, rx + 0.5, ry + 0.3, M1)
            yt = track_y(net, ci)
            rect(top, px - TRK_W / 2, ry - TRK_W / 2, px + TRK_W / 2,
                 yt + TRK_W / 2, M4)
            stacks.append((px, ry, (("via1", M1, M2), ("via2", M2, M3),
                                    ("via3", M3, M4))))
            rail_straps.append((net, px, ry, -1 if net == "vss" else 1,
                                ring_xe))
            stacks.append((px, yt, (("via3", M3, M4),)))
            continue
        else:
            # a starve-gate track: metal3 out to the riser
            rect(top, min(px, rx) - TRK_W / 2, ry - RING_LW / 2,
                 max(px, rx) + TRK_W / 2, ry + RING_LW / 2, M3)
        via(top, px, ry, "via3", M3, M4)
        yt = track_y(net, ci)
        rect(top, px - TRK_W / 2, ry - TRK_W / 2, px + TRK_W / 2,
             yt + TRK_W / 2, M4)
        via(top, px, yt, "via3", M3, M4)
    for net in RIGHT_PINS:
        ci = min(c for c in range(nch) if net in tracks[c])
        yt = track_y(net, ci)
        via(top, x_right - 0.2, yt, "via2", M2, M3)
        labels.append((net, x_right - 0.2, yt, LY["metal2_label"]))

    labels.sort(key=lambda lbl: PINS.index(lbl[0]))
    # every routed internal net keeps its name through extraction: a non-pin
    # label (metal3 drawing, 42/0, which magic reads as `noport`) on its
    # first channel track. magic's parasitic extraction (extresist) drops
    # the coupling capacitance of a net it has to name itself (a_x_y#): on
    # the ring nodes r1..r5 that was about half their wire C, and the
    # post-layout VCO read 226 MHz at typical where it runs at about 198.
    # The names also let a post-layout bench kick r1 as the pre-layout
    # ones do.
    named = set()
    for ci, tr in enumerate(tracks):
        for net, (_t, a, b) in sorted(tr.items()):
            if net in PINS or net in named:
                continue
            named.add(net)
            labels.append((net, r5((a + b) / 2), track_y(net, ci), M3))
    widen_supply_feet(top, feet)
    widen_supply_taps(top, taps)
    widen_supply_stacks(top, stacks)
    strap_ring_rails(top, rail_straps, feet)
    sig_em_arrays(top, SIG_STUBS, SIG_SPOTS)
    fill_m3_notches(top)
    return layoutlib.finalize(top, CELL, labels)


if __name__ == "__main__":
    comp = generate()
    out_path = sys.argv[1] if len(sys.argv) > 1 else f"{CELL}.gds"
    comp.write_gds(out_path)
    print(f"wrote {out_path} bbox={comp.dbbox()}")
