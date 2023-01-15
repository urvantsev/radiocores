# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

# Makefile

# defaults
#SIM ?= icarus
SIM ?= verilator
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(PWD)/gray2bin.sv
#VERILOG_SOURCES += $(PWD)/synth.v
# use VHDL_SOURCES for VHDL files

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = gray2bin

# MODULE is the basename of the Python test file
MODULE = test_gray2bin

# Verilator VCD dump
EXTRA_ARGS += --trace --trace-structs

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
