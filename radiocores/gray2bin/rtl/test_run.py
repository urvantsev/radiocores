import os
from cocotb.runner import get_runner
from pathlib import Path
import pytest

# Define the project path and sources
proj_path = Path(__file__).resolve().parent
sources = [proj_path / "gray2bin.sv"]

@pytest.mark.parametrize("test_module", ["tests.test_gray2bin"])
def test_cocotb_simulation(test_module):
    build_dir = proj_path / f"sim_build_{test_module.split('.')[-1]}"
    vcd_file = build_dir / f"{test_module.split('.')[-1]}.vcd"

    os.environ["COCOTB_RESULTS_FILE"] = str(vcd_file)

    # Get the simulator runner
    runner = get_runner("verilator")
    # Build the simulation
    runner.build(
        verilog_sources=sources,
        hdl_toplevel="gray2bin",
        build_dir=build_dir,
        build_args=["--trace", "--trace-structs", "--coverage"],
        always=True,
    )
    # Run the test
    runner.test(hdl_toplevel="gray2bin", test_module=test_module)

if __name__ == "__main__":
    pytest.main([__file__])
