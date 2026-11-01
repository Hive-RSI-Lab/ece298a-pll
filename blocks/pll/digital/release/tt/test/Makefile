# Staged by chip-flow release (engine/lib/ttship.py): the block's tb/ suite on
# the gate-level netlist, as the glsim gate's functional pass runs it.
SIM ?= icarus
TOPLEVEL_LANG ?= verilog
COCOTB_HDL_TIMEUNIT = 1ns
COCOTB_HDL_TIMEPRECISION = 1ps

ifneq ($(GATES),yes)
$(error this tile ships a hardened netlist: run with GATES=yes)
endif

SIM_BUILD = sim_build/gl
COMPILE_ARGS += -DGL_TEST
COMPILE_ARGS += -DFUNCTIONAL
COMPILE_ARGS += -DUSE_POWER_PINS
VERILOG_SOURCES += $(PWD)/glsim_harness.v
VERILOG_SOURCES += $(PDK_ROOT)/gf180mcuD/libs.ref/gf180mcu_fd_sc_mcu7t5v0/verilog/primitives.v
VERILOG_SOURCES += $(PDK_ROOT)/gf180mcuD/libs.ref/gf180mcu_fd_sc_mcu7t5v0/verilog/gf180mcu_fd_sc_mcu7t5v0.v
# copied in by the workflow from tt_submission
VERILOG_SOURCES += $(PWD)/gate_level_netlist.v

TOPLEVEL = ihsan_sa_pll
COCOTB_TEST_MODULES = test_pll

include $(shell cocotb-config --makefiles)/Makefile.sim
