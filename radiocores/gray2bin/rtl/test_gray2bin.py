import os
import pytest
from cocotb.runner import get_runner
from pathlib import Path

# Current working directory, should be root of the repository
cwd = Path.cwd()

# Define rtl sources
rtl_path = cwd / "radiocores" / "gray2bin" / "rtl"

sources = [
    rtl_path / "node.sv",
    rtl_path / "gray2bin.sv",
    rtl_path / "gray2bin_wrapper.sv",
]

# Define includes
includes = [
    cwd / "radiocores" / "include",
]


@pytest.mark.parametrize("test_module", ["tests.tb_gray2bin"])
def test_cocotb_simulation(test_module):
    build_dir = rtl_path / f"sim_build_{test_module.split('.')[-1]}"
    vcd_file = build_dir / f"{test_module.split('.')[-1]}.vcd"

    os.environ["COCOTB_RESULTS_FILE"] = str(vcd_file)

    # Get the simulator runner
    runner = get_runner("verilator")

    # Add the include paths
    include_dirs = [rtl_path]
    include_args = [f"-I{include_dir}" for include_dir in include_dirs]

    # Build the simulation
    runner.build(
        verilog_sources=sources,
        includes=includes,
        hdl_toplevel="gray2bin_wrapper",
        build_dir=build_dir,
        build_args=["--trace", "--trace-structs", "--coverage"] + include_args,
        always=True,
    )

    # Run the test
    runner.test(hdl_toplevel="gray2bin_wrapper", test_module=test_module)


if __name__ == "__main__":
    pytest.main([__file__])
