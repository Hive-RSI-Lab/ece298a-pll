"""Write docs/review/stages.md: every stage of the PLL's flow on one page,
each with what it shows, its recorded result and how to see it work yourself.

    python3 docs/review/stages.py            (writes docs/review/stages.md)
    python3 docs/review/stages.py --check    (exit 3 if stages.md is stale)

It reads only files in this repository: each workspace's state.json (the
gate's last run and when) and its reports/recorded/ (what the run found).
No EDA tool runs here, so it works anywhere with python3. Run it again
after any gate's recorded result changes.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
BLOCK = ROOT / "blocks" / "pll"
OUT = Path(__file__).resolve().parent / "stages.md"

# Re-running a gate: chip-flow's gate.py with the tree's python. In the Hive
# that is `chip-flow gate ...`; elsewhere `$CHIP_FLOW_HOME/bin/eda python
# $CHIP_FLOW_HOME/engine/scripts/gate.py ...`.
WS = {"top": ("blocks/pll", "msde"), "analog": ("blocks/pll/analog", "ade"),
      "digital": ("blocks/pll/digital", "vde")}


def load(p: Path):
    try:
        return json.loads(p.read_text())
    except (OSError, ValueError):
        return None


def f(x, nd=1) -> str:
    return f"{x:.{nd}f}" if isinstance(x, (int, float)) else "?"


# Each headline reads the recorded report's facts: one line saying what it showed.
def h_sim_pvt(r):
    res = r["facts"]["results"]
    return f"{len(res)} bench runs over {len(r['facts']['corners'])} corners, every bound met" \
        if r["status"] == "pass" else ""


def h_sim_tt(r):
    m = {}
    for x in r["facts"]["results"]:
        m.update(x.get("measures") or {})
    return f"tt: Icp up {f(m.get('icp_up_code00_ua'))} uA, Kvco {f(m.get('vco_kvco_mhz_per_v'))} MHz/V" \
        if m.get("icp_up_code00_ua") else ""


def h_bench(r):
    x = r["facts"]
    return f"{x['killed']} of {x['total_mutants']} planted netlist faults caught; " \
        f"{x['below_spread']} too small to see, each ruled on"


def h_cover(r):
    x = r["facts"]
    return f"line {f(x['line_pct'], 0)}%, toggle {f(x['toggle_pct'], 0)}%"


def h_mutate(r):
    x = r["facts"]
    return f"{x['killed']} of {x['scored_mutants']} RTL mutants killed ({x['equivalent']} equivalent, ruled)"


def h_formal(r):
    x = r["facts"]
    return f"{len(x['bounded'])} properties hold to depth {x['depth']}, {len(x['proven'])} proven unbounded, " \
        f"{len(x['cover_points'])} cover points; {len(x['failed'])} fail"


def h_tests(r):
    x = r["facts"]
    return f"{x['tests_passed']} of {len(x['tests_run'])} tests pass"


def h_glsim(r):
    res = r["facts"]["results"]
    return ", ".join(f"{k} {sum(v.values())}/{len(v)}" for k, v in res.items())


def h_synth(r):
    return f"{sum(r['facts']['cells'].values())} cells, {r['facts']['std_cell']['library']}"


def h_harden(r):
    m = r["facts"].get("metrics") or {}
    return f"{m.get('design__instance__count', '?')} instances, setup WNS {f(m.get('timing__setup__ws'), 2)} ns, " \
        f"hold WNS {f(m.get('timing__hold__ws'), 2)} ns"


def h_timing(r):
    c = r["facts"]["corners"]
    worst = min(c.items(), key=lambda kv: kv[1]["setup_ws"])
    return f"worst setup {f(worst[1]['setup_ws'], 2)} ns at {worst[0]}; " \
        f"hold >= {f(min(v['hold_ws'] for v in c.values()), 2)} ns everywhere"


def h_drc(r):
    x = r["facts"]
    if "magic_count" in x:
        return f"magic {x['magic_count']}, klayout {x['klayout_count']} violations"
    return "klayout: 0 violations" if r["status"] == "pass" else ""


def h_lvs(r):
    x = r["facts"]
    if "matched" in x:
        return "layout matches the netlist" if x["matched"] else f"no match: {x.get('final', '')}"
    return "layout matches the netlist" if r["status"] == "pass" else ""


def h_pex_sim(r):
    m = r["facts"]["measured"]
    return f"tt extracted: Icp {f(m['icp_up_code00_ua'])} uA, Kvco {f(m['vco_kvco_mhz_per_v'])} MHz/V, " \
        f"fmax {f(m['vco_fmax_tt_mhz'])} MHz; {r['facts']['parasitics']['c']} parasitic C"


def h_pex_pvt(r):
    x = r["facts"]
    n = len(x["swept"]) if isinstance(x.get("swept"), list) else x.get("swept")
    bad = len(r.get("failing") or [])
    return f"{(n or 0) - bad} of {n} corners pass their post-layout bounds"


def h_cosim(r):
    m = r["facts"]["measures"]
    op = m["operating_point"]
    return f"locks in {f(m['lock_time_us'], 2)} us at {f(op['f_vco_target_hz'] / 1e6, 3)} MHz " \
        f"(P*N={op['p_times_n']}), {m['lock_drops_after_lock']} lock drops, " \
        f"VCO period error {f(m['vco_period_rel_err'], 4)}"


def h_split(r):
    return f"{len(r['facts']['signals'])} signals cross the analog/digital line"


def h_precheck(r):
    return f"{r['facts'].get('checks_run', '?')} Tiny Tapeout checks run"


def h_top_harden(r):
    m = r["facts"].get("metrics") or {}
    return f"{m.get('design__instance__count', '?')} instances around the analog macro, " \
        f"setup WNS {f(m.get('timing__setup__ws'), 2)} ns"


def h_cosim_corners(r):
    x = r["facts"]
    res = {y["corner"]: (y.get("measures") or {}) for y in x.get("results") or []}
    locked = x.get("locked") or x["corners"]
    locks = ", ".join(f"{c} {f(res.get(c, {}).get('lock_time_us'), 2)} us" for c in locked)
    return f"locks at {len(locked)} of {len(x['swept'])} bounding corners on the extracted netlist" \
        + (f" ({locks})" if locks else "") \
        + f"; vctrl within 20 mV p-p at {len(x['corners'])} of them"


# The stages in flow order. Each row: workspace, gate, what it shows, and how
# you see it work yourself besides re-running the gate.
STAGES = [
    ("Spec and split", [
        ("digital", "spec_lint", "the digital requirements are complete and each names its check", None,
         "`blocks/pll/digital/spec/spec.md`"),
        ("analog", "spec_lint", "the analog spec's bounds, corners and benches are well formed", None,
         "`blocks/pll/analog/spec/spec.md`"),
        ("top", "split", "the analog and digital halves agree on every crossing signal", h_split,
         "`blocks/pll/interface.yaml`"),
    ]),
    ("Analog schematic (pre-layout)", [
        ("analog", "netlist_lint", "the netlist parses and every device is a GF180 model", None,
         "`blocks/pll/analog/netlist/pll_analog.cir`"),
        ("analog", "sim_tt", "every bench passes at typical", h_sim_tt,
         "ngspice decks in `blocks/pll/analog/tb/`"),
        ("analog", "sim_pvt", "every bench passes at all 31 PVT corners", h_sim_pvt,
         "`blocks/pll/analog/reports/recorded/gate-sim_pvt.json` (every measure at every corner)"),
        ("analog", "bench_strength", "the benches catch planted faults in the netlist", h_bench,
         "`blocks/pll/analog/log/bench_strength/`"),
    ]),
    ("Digital RTL", [
        ("digital", "lint", "the RTL compiles clean", None, "`blocks/pll/digital/rtl/`"),
        ("digital", "sim", "the cocotb tests of every requirement pass", h_tests,
         "`cd test && make && gtkwave tb.fst` (the Tiny Tapeout test of the top, about a second)"),
        ("digital", "holdout", "tests the RTL was not written against pass", h_tests,
         "`blocks/pll/digital/holdout/`"),
        ("digital", "cover", "the tests reach every line and toggle", h_cover, None),
        ("digital", "mutate", "the tests catch planted RTL faults", h_mutate, None),
        ("digital", "formal", "the requirements' properties hold in the formal model", h_formal,
         "`blocks/pll/digital/formal/`"),
    ]),
    ("Digital standalone hardening", [
        ("digital", "synth", "the RTL synthesises to GF180 standard cells", h_synth, None),
        ("digital", "harden", "the digital half places and routes on its own", h_harden, None),
        ("digital", "timing", "setup and hold meet with the VCO clock at 2.7 ns, every STA corner", h_timing,
         "issue 8 in `blocks/pll/digital/state.json`; GOALS.md's digital issue 8 goal"),
        ("digital", "drc", "the digital layout is DRC clean", h_drc, None),
        ("digital", "lvs", "the digital layout matches its netlist", h_lvs, None),
        ("digital", "glsim", "the tests pass on the gate-level netlist, with and without delays", h_glsim, None),
        ("digital", "precheck", "the standalone digital tile passes Tiny Tapeout's precheck", h_precheck,
         "`blocks/pll/digital/log/precheck_run/precheck/reports/results.md`"),
    ]),
    ("Whole loop (system verification)", [
        ("top", "cosim", "the digital RTL and the transistor-level analog lock together", h_cosim,
         "`blocks/pll/tb/README.md`; all three layers: `chip-flow eda python blocks/pll/tb/run_layers.py` "
         "(about 2.5 min)"),
        ("top", "cosim_corners", "the same loop locks on the extracted analog netlist at the corners that "
         "bound its post-layout range (lowest and highest VCO ceiling and phase margin)", h_cosim_corners,
         "`blocks/pll/tb/README.md`; every corner's measures and vctrl trace: "
         "`blocks/pll/reports/recorded/cosim_corners.json`"),
    ]),
    ("Analog layout", [
        ("analog", "drc", "the analog layout is DRC clean", h_drc,
         "`klayout blocks/pll/analog/layout/pll_analog.gds`"),
        ("analog", "lvs", "the analog layout matches the signed-off netlist", h_lvs,
         "`blocks/pll/analog/layout/gen_pll_analog.py` draws it"),
        ("analog", "pex_sim", "the benches run on the extracted netlist at typical", h_pex_sim, None),
        ("analog", "pex_pvt", "the extracted netlist meets its post-layout bounds at every corner", h_pex_pvt,
         "every measure at every corner: `blocks/pll/analog/reports/recorded/pex_pvt.json`"),
    ]),
    ("Full tile (Tiny Tapeout submission shape)", [
        ("top", "top_harden", "the digital half hardens around the analog macro into one tile", h_top_harden,
         None),
        ("top", "top_drc", "the whole tile is DRC clean", h_drc, None),
        ("top", "top_lvs", "the whole tile matches its netlist, analog macro included", h_lvs,
         "`blocks/pll/log/top_lvs/top_lvs.rpt` after a run"),
        ("top", "precheck", "the tile passes Tiny Tapeout's precheck", h_precheck, None),
    ]),
]


def recorded(ws: str, gate: str):
    d = BLOCK if ws == "top" else BLOCK / ws
    if gate in ("pex_pvt", "cosim_corners"):
        return load(d / "reports" / "recorded" / f"{gate}.json"), d
    return load(d / "reports" / "recorded" / f"gate-{gate}.json"), d


def state_last(d: Path, gate: str):
    st = load(d / "state.json") or {}
    return ((st.get("gates") or {}).get(gate) or {}).get("last") or {}


def waived(d: Path, gate: str) -> str:
    """A waiver chip-flow's release reads (reports/waivers.json), when there is one."""
    w = load(d / "reports" / "waivers.json")
    if isinstance(w, dict):
        w = w.get("waivers") if isinstance(w.get("waivers"), list) else [dict(x, gate=k) for k, x in w.items()
                                                                     if isinstance(x, dict)]
    items = [x for x in w or [] if isinstance(x, dict) and x.get("gate") == gate]
    return f" (waived, pending your review: `{d.relative_to(ROOT)}/reports/waivers.json`)" if items else ""


def row(ws: str, gate: str, shows: str, head, see) -> tuple[str, str]:
    r, d = recorded(ws, gate)
    last = state_last(d, gate)
    when = (last.get("ts") or (r or {}).get("ts") or "")[:10] or "-"
    if r is None:
        status, line = "not run", ""
    else:
        status = r.get("status", "?")
        try:
            line = head(r) if head else ""
        except (KeyError, TypeError, ValueError, ZeroDivisionError):
            line = ""
        msgs = [str(x.get("msg") or x.get("kind"))[:140].replace("\n", " ").replace("|", "/")
                for x in (r.get("failing") or [])[:1 if line else 2]]
        if status != "pass" and msgs:
            line = "; ".join(m for m in [line] + msgs if m)
    if last.get("status") and r is not None and last["status"] != r.get("status"):
        line += f" (state.json's last run says {last['status']})"
    mark = {"pass": "pass", "fail": "**FAIL**"}.get(status, f"**{status}**")
    mark += waived(d, gate) if status == "fail" else ""
    rel = d.relative_to(ROOT)
    rerun = f"`chip-flow gate --gate {gate} --skill {WS[ws][1]} --workspace {rel}`"
    if gate == "pex_pvt":
        rerun = "`chip-flow eda python blocks/pll/analog/layout/pex_pvt.py " \
            "--workspace blocks/pll/analog --out blocks/pll/analog/reports/recorded/pex_pvt.json`"
    elif gate == "cosim_corners":
        rerun = "`chip-flow eda python blocks/pll/tb/cosim_corners.py`"
    how = "<br>".join(x for x in [see or "", rerun] if x)
    return status, f"| {gate} ({ws}) | {shows} | {mark} | {line} | {when} | {how} |"


def human(ws: str) -> list[str]:
    d = BLOCK if ws == "top" else BLOCK / ws
    h = (load(d / "state.json") or {}).get("human") or {}
    out = []
    for k, v in sorted(h.items()):
        if v.get("status") == "approved":
            out.append(f"- {ws} {k} (`{v.get('challenge')}`): **approved** {str(v.get('ts', ''))[:10]}, "
                       f"{v.get('answer', '')}")
        else:
            out.append(f"- {ws} {k} (`{v.get('challenge')}`): **{v.get('status')}** "
                       f"{str(v.get('presented', ''))[:10]}, waiting for your answer")
    return out


def render() -> str:
    lines = [
        "# The PLL, stage by stage",
        "",
        "Every stage of the flow from spec to the Tiny Tapeout tile, each with what it",
        "shows, its last recorded result, and how to see it work yourself. Written by",
        "`python3 docs/review/stages.py` from each gate's report in `reports/recorded/`",
        "and its workspace's `state.json`; don't edit it by hand. A result here is what",
        "the last committed run of that gate found.",
        "",
        "To re-run a gate you need chip-flow and the IIC-OSIC-TOOLS tree: in the Hive",
        "the commands work as written. Elsewhere, put `$CHIP_FLOW_HOME/bin/eda python",
        "$CHIP_FLOW_HOME/engine/scripts/gate.py` in place of `chip-flow gate`. The",
        "commands without chip-flow (the RTL test, klayout, gtkwave) need only those",
        "tools. Run them from the repository's root.",
        "",
    ]
    tally = {}
    body = []
    for title, rows in STAGES:
        body += [f"## {title}", "",
                 "| gate | shows | result | what it found | run | see it yourself |",
                 "|---|---|---|---|---|---|"]
        for spec in rows:
            status, line = row(*spec)
            tally[status] = tally.get(status, 0) + 1
            body.append(line)
        body.append("")
    signs = human("analog") + human("digital") + human("top")
    total = sum(tally.values())
    lines += [f"**{tally.get('pass', 0)} of {total} gates pass on their last recorded run.** "
              + ", ".join(f"{n} {s}" for s, n in sorted(tally.items()) if s != "pass") + ".", ""]
    lines += body
    lines += ["## Your sign-offs", "",
              "The engine stops at each sign-off for you. A pending one is not taken as",
              "approved: the work went ahead on it pending your review, as you asked on",
              "2026-10-29. `GOALS.md` says where each goal stands.", ""]
    lines += (signs or ["- none recorded"]) + [""]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv[1:]:
        if not OUT.exists() or OUT.read_text() != text:
            print("stages: docs/review/stages.md is stale; run python3 docs/review/stages.py", file=sys.stderr)
            return 3
        return 0
    OUT.write_text(text)
    print(f"stages: wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
