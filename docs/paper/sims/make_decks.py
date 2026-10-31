"""Write post-layout ngspice decks for the paper's VCO figures.

    python3 docs/paper/sims/make_decks.py   # then run_sims.sh

Starts from the vco bench as sim_pvt filled it for a corner
(blocks/pll/analog/log/sim/pll_analog_vco_tb__<corner>.cir), swaps the
schematic netlist for the layout's extraction, and
  * vco_<corner>.cir: 13-point vctrl sweep 0.3..vdd-0.3 V plus vdd, echoing
    "PT <vctrl> <f_hz>" per point;
  * wave_tt_27c.cir: one 60 ns transient at vctrl = 1.6 V, writing vco_out
    and vco_div2 (the TSPC /2) to wave_tt_27c.txt.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AN = ROOT / "blocks/pll/analog"
PEX = AN / "log/pex_pvt/pll_analog.pex.ordered.spice"
OUT = Path(__file__).resolve().parent / "run"
OUT.mkdir(exist_ok=True)
CORNERS = sys.argv[1:] or ["tt_27c", "ss_125c_vm10", "ff_m40c_vm10", "ff_pss"]


def base(corner: str) -> str:
    d = (AN / f"log/sim/pll_analog_vco_tb__{corner}.cir").read_text()
    d = re.sub(r"\.include '[^']*/netlist/pll_analog\.cir'", f".include '{PEX}'", d)
    assert str(PEX) in d
    return d.replace("pulse(0 1u 1n", "pulse(0 200u 1n")


for c in CORNERS:
    d = base(c).replace("let npt = 6", "let npt = 12").replace("let kmid = 3", "let kmid = 6")
    d = d.replace("  let fk = $fks\n", "  let fk = $fks\n  echo \"PT $&vc $&fk\"\n", 1)
    (OUT / f"vco_{c}.cir").write_text(d)

d = base("tt_27c")
head, _ = d.split(".control", 1)
head = head.replace("vvc      vctrl    0 0.3", "vvc      vctrl    0 1.6")
ctrl = f""".control
set noaskquit
tran 5p 60n 0 5p
set wr_singlescale
wrdata {OUT}/wave_tt_27c.txt v(xdut.vco_out) v(vco_div2)
.endc
.end
"""
(OUT / "wave_tt_27c.cir").write_text(head + ctrl)
print("decks in", OUT)
