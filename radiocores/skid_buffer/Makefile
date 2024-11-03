# Variables
DSIM_CMD = dsim
DSIM_FLAGS = -sv +acc -waves waves.mxd
FILELIST = filelist.f    # File containing RTL source list

# File paths
RTL_PATH = rtl/skid_buffer.sv
TB_PATH = uvm/tb/top.sv

# Target to run the simulation
run:
	$(DSIM_CMD) $(DSIM_FLAGS) -f $(FILELIST) $(TB_PATH)

# Clean target to remove generated files
clean:
	rm -rf dsim_work *.log *.mxd *.db dsim.env

.PHONY: run clean