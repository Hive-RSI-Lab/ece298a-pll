![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg) ![](../../workflows/check/badge.svg)

# Charge-pump PLL for Tiny Tapeout (GF180)

The ECE 298A term project: a charge-pump phase-locked loop on one Tiny Tapeout
GF180 tile. A current-starved ring VCO is locked to the reference on `clk`, at
8 × N times the reference (N = 1 to 5), with a lock detector.

- **To review it** (where it stands, pictures, the decisions waiting for
  you): [docs/review/README.md](docs/review/README.md). Every stage's recorded
  result, and the command to see it work yourself:
  [docs/review/stages.md](docs/review/stages.md)
- The datasheet: [docs/info.md](docs/info.md)
- Goals and their status: [GOALS.md](GOALS.md)

## Where things are

| Path | What |
|---|---|
| `blocks/pll/analog` | the analog half: netlist, spec, benches, the layout generator and its GDS |
| `blocks/pll/digital` | the digital half: RTL, formal, testbenches, the standalone harden |
| `blocks/pll/interface.yaml` | every signal between the two halves, and the two analog pads |
| `blocks/pll/tb` | the whole loop: linear model, RTL with a behavioural analog model, and the co-simulation with the transistor-level analog |
| `src/`, `test/`, `info.yaml` | what the Tiny Tapeout flow reads |
| `tests/check.sh` | the fast check every pull request passes |
| `tests/score.sh` | the share of GOALS.md's checkable done-lines that pass |

The design is built with [chip-flow](https://github.com/Hive-RSI-Lab/hive-chip-flow)
and the IIC-OSIC-TOOLS tree (ngspice, magic, netgen, klayout, LibreLane).

## What is Tiny Tapeout?

Tiny Tapeout is an educational project that makes it easier and cheaper to get
digital and analog designs manufactured on a real chip. See
https://tinytapeout.com and, for analog projects, https://tinytapeout.com/specs/analog/.
