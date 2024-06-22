import os
import pytest
from cocotb.runner import get_runner
from pathlib import Path

# Define the project path and sources
proj_path = Path(__file__).resolve().parent
sources = [
    proj_path / "gray2bin_if.svh",
    proj_path / "node_if.svh",
    proj_path / "node.sv",
    proj_path / "gray2bin.sv",
    proj_path / "gray2bin_wrapper.sv",
]


@pytest.mark.parametrize("test_module", ["tests.tb_gray2bin"])
def test_cocotb_simulation(test_module):
    build_dir = proj_path / f"sim_build_{test_module.split('.')[-1]}"
    vcd_file = build_dir / f"{test_module.split('.')[-1]}.vcd"

    os.environ["COCOTB_RESULTS_FILE"] = str(vcd_file)

    # Get the simulator runner
    runner = get_runner("verilator")

    # Add the include paths
    include_dirs = [proj_path]
    include_args = [f"-I{include_dir}" for include_dir in include_dirs]

    # Build the simulation
    runner.build(
        verilog_sources=sources,
        hdl_toplevel="gray2bin_wrapper",
        build_dir=build_dir,
        build_args=["--trace", "--trace-structs", "--coverage"] + include_args,
        always=True,
    )

    # Run the test
    runner.test(hdl_toplevel="gray2bin_wrapper", test_module=test_module)


if __name__ == "__main__":
    pytest.main([__file__])
