"""Shared helpers for the top-level PLL benches (cosim, calibration, linear
model). Not a test module. Paths are resolved from this file, so the benches
run from any working directory."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent          # blocks/pll/tb
WS = HERE.parent                                # blocks/pll
ANALOG = WS / "analog"
NETLIST = ANALOG / "netlist" / "pll_analog.cir"
SIZING = ANALOG / "sizing" / "sizing.yaml"
CAL_JSON = HERE / "pll_analog_cal.json"
BENCH_JSON = HERE / "cosim_bench.json"

VDD = 3.3
F_REF_HZ = 6.25e6          # nominal reference (brief section 2)
N_SEL = 2                  # N = 2, P*N = 16 -> 100 MHz
P = 8


def toolchain_root() -> Path:
    """The eda toolchain root: from LIBNGSPICE_PATH (check_cosim.py sets
    it), else EDA_TOOLCHAIN, else `eda --print-toolchain-root`."""
    lib = os.environ.get("LIBNGSPICE_PATH")
    if lib:
        # <T>/foss/tools/ngspice/lib/libngspice.so.0
        return Path(lib).resolve().parents[4]
    if os.environ.get("EDA_TOOLCHAIN"):
        return Path(os.environ["EDA_TOOLCHAIN"])
    cfh = Path(os.environ.get("CHIP_FLOW_HOME", "/opt/chip-flow"))
    out = subprocess.run([str(cfh / "bin" / "eda"), "--print-toolchain-root"],
                         capture_output=True, text=True, check=True)
    return Path(out.stdout.strip())


def pdk_ngspice_dir() -> Path:
    root = os.environ.get("PDK_ROOT")
    base = Path(root) if root else toolchain_root() / "foss" / "pdks"
    return base / "gf180mcuD" / "libs.tech" / "ngspice"


def sizing_param_line() -> str:
    """sizing/sizing.yaml rendered as one .param line - the same values the
    analog gates simulate (each entry's `value`)."""
    import yaml
    doc = yaml.safe_load(SIZING.read_text(encoding="utf-8")) or {}
    parts = [f"{k}={v['value']}" for k, v in doc.items()
             if isinstance(v, dict) and "value" in v]
    return ".param " + " ".join(parts)


MOSCAP_Q = """* the loop filter's MOS caps: the PDK's cap_nmos_03v3_b (sm141064.spice, .lib
* moscap), written in charge form. The PDK's C(v) = A*(cvar1 + cvar2*tanh(cvar3*v
* + cvar4)) as a voltage-dependent C makes the transient step collapse ("timestep
* too small" on its current probe) at most corners on the extracted netlist;
* Q(v), its integral, is the same device and holds (pex tt_27c: Icp 18.52 vs
* 18.52 uA, Kvco 72.67 vs 72.66 MHz/V, fmax 203.31 vs 203.29 MHz against the
* PDK form under Gear). Its corner factor follows the MIM corner's
* (mim_corner_2p0ff: 1 / 1.1 ss / 0.9 ff, as moscap_<corner> sets it).
.param cap_nmos_03v3_b_corner=mim_corner_2p0ff
.subckt cap_nmos_03v3_b 1 2 c_length=1e-6 c_width=1e-6 dtemp=0
.param cvar1=0.002458 cvar2=0.001533 cvar3=1.515152 cvar4=0.560606
* ln(cosh(x)) written |x| + ln(1+exp(-2|x|)) - ln 2, the same function: cosh
* overflowed on a wild Newton iterate in the op search ('Error: -10030.2 out
* of range for cosh', which the engine reads as an ngspice error; ff_27c_vm10).
C1 1 2 q='cap_nmos_03v3_b_corner*c_length*c_width*(cvar1*v(1,2)+cvar2/cvar3*(abs(cvar3*v(1,2)+cvar4)+ln(1+exp(-2*abs(cvar3*v(1,2)+cvar4)))-ln(2)))'
.ends cap_nmos_03v3_b"""


def model_lines(corner: str = "typical", res: str = "res_typical",
                mim: str = "mimcap_typical") -> list[str]:
    """PDK model includes + the real netlist + its sizing (tt by default)."""
    p = pdk_ngspice_dir()
    return [
        f".include '{p}/design.spice'",
        f".lib '{p}/sm141064.spice' {corner}",
        f".lib '{p}/sm141064.spice' {res}",
        f".lib '{p}/sm141064.spice' {mim}",
        # the loop filter's MOS caps in charge form (the analog benches'
        # comment says why), at the MIM corner's factor
        *MOSCAP_Q.splitlines(),
        f".include '{NETLIST}'",
        sizing_param_line(),
    ]


def ngspice_cmd() -> list[str]:
    cfh = Path(os.environ.get("CHIP_FLOW_HOME", "/opt/chip-flow"))
    eda = cfh / "bin" / "eda"
    if eda.is_file():
        return [str(eda), "ngspice", "-b"]
    return [shutil.which("ngspice") or "ngspice", "-b"]


def load_cal() -> dict:
    return json.loads(CAL_JSON.read_text(encoding="utf-8"))


def bench_meta() -> dict:
    return json.loads(BENCH_JSON.read_text(encoding="utf-8"))
