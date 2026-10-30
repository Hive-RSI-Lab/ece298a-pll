# The PLL in Tiny Tapeout's analog-project shape

Tiny Tapeout's GF180 analog projects (ttgf-analog-template) commit their own
GDS and LEF; the shuttle's flow checks them and never hardens anything itself.
This folder holds what the repository root takes once the tile is hardened,
and `assemble.py` puts it in place:

| Here | Goes to | What |
|---|---|---|
| `src/project.v` | `src/project.v` | the top: the template's ports (VGND, VDPWR, `ua`), the digital core and the analog macro, wired as chip-flow's top_harden wires them |
| `src/pll_analog.v` | `src/pll_analog.v` | the analog macro's port list (a blackbox) |
| `../digital/rtl/*.v` | `src/` | the digital core |
| `test/` | `test/` | the RTL test: the top with `pll_analog_model.v`, a behavioural model of the macro calibrated from the netlist at tt_27c |
| `info.yaml` | `info.yaml` | tiles 1x2, analog_pins 2, ua[0] VCTRL, ua[1] BIAS_REF |
| `workflows/gds.yaml` | `.github/workflows/gds.yaml` | `custom_gds`, precheck and the viewer on the committed GDS |
| `../top/harden/runs/run/final/{gds,lef}` | `gds/`, `lef/` | the hardened tile |

Run, after `top_harden`, `top_drc`, `top_lvs` and `precheck` pass:

    python3 blocks/pll/tt/assemble.py

From then on `tests/check.sh` runs `assemble.py --check`, so `src/` can't
drift from the RTL the tile was hardened from.

The RTL test runs on its own too (Icarus Verilog and cocotb 2.0):

    python3 blocks/pll/tt/assemble.py && cd test && make
