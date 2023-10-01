from pathlib import Path

import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
from cocotb.runner import get_runner

from radiocores.bin2gray import bin2gray


@cocotb.test()
async def gray2bin_simple_test(dut):
    """Test for DUT (design under test)"""

    # Create a clock
    clock = Clock(dut.clk, 10, units="ns")  # 100 MHz clock
    cocotb.start_soon(clock.start())  # Start the clock

    # Reset the DUT (Optional)
    dut.rst_n.value = 0
    await Timer(50, units="ns")  # reset is active for 5 clock cycles
    dut.rst_n.value = 1

    # Apply stimulus
    for i in range(10):
        dut.i_gray_code <= bin2gray(i)
        await RisingEdge(dut.clk)

    # ... Here, you can check the DUT's outputs using asserts


def test_gray2bin_simple_test():
    proj_path = Path(__file__).resolve().parent

    sources = [proj_path / "gray2bin.sv"]

    runner = get_runner("verilator")
    runner.build(
        verilog_sources=sources,
        hdl_toplevel="gray2bin",
        build_args=["--trace", "--trace-structs", "--coverage"],
        always=True,
    )

    runner.test(hdl_toplevel="gray2bin", test_module="test_gray2bin")


if __name__ == "__main__":
    test_gray2bin_simple_test()
