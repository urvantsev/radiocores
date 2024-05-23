import os
import platform
import cocotb
from cocotb.triggers import RisingEdge, Timer, Event, with_timeout
from cocotb.clock import Clock
from cocotb.runner import get_runner
from pathlib import Path
import logging
from radiocores.bin2gray import bin2gray

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info("Environment Information")
logger.info(f"Platform: {platform.platform()}")
logger.info(f"Python version: {platform.python_version()}")
logger.info(f"Verilator version: {os.popen('verilator --version').read().strip()}")


async def supply_input_data(dut, input_data, input_done):
    """Coroutine to supply input data to the DUT"""
    for i in input_data:
        await RisingEdge(dut.clk)
        gray_code = bin2gray(i)
        logger.debug(f"Supplying input: {i}, gray code: {gray_code}")
        dut.i_dv.value = 1  # Set data valid signal
        dut.i_gray_code.value = gray_code
        await RisingEdge(dut.clk)
        dut.i_dv.value = 0  # Clear data valid signal after one cycle

    # Signal that input data supply is done
    input_done.set()
    logger.debug("Input data supply done")


async def read_output_data(dut, output_data, input_data, input_done):
    """Coroutine to read output data from the DUT"""
    while not input_done.is_set():
        await with_timeout(
            RisingEdge(dut.clk), 1000, "ns"
        )  # Increased timeout to 1000 ns
        if dut.o_dv.value == 1:
            output = int(dut.o_binary_code.value)
            output_data.append(output)
            logger.debug(f"Read output: {output}")

    # Continue checking remaining items after all inputs are applied
    while len(output_data) < len(input_data):
        await with_timeout(
            RisingEdge(dut.clk), 1000, "ns"
        )  # Increased timeout to 1000 ns
        if dut.o_dv.value == 1:
            output = int(dut.o_binary_code.value)
            output_data.append(output)
            logger.debug(f"Read remaining output: {output}")


@cocotb.test()
async def gray2bin_simple_test(dut):
    """Test for DUT (design under test)"""

    # Create a clock
    clock = Clock(dut.clk, 10, units="ns")  # 100 MHz clock
    cocotb.start_soon(clock.start())  # Start the clock
    logger.debug("Clock started")

    # Reset the DUT
    dut.rst.value = 1
    await Timer(50, units="ns")  # Reset is active for 5 clock cycles
    logger.debug("Reset asserted")
    dut.rst.value = 0
    await Timer(50, units="ns")
    logger.debug("Reset deasserted")

    # Lists to keep track of inputs and outputs
    input_data = list(range(10))  # Example input data
    output_data = []

    # Event to signal the completion of input data supply
    input_done = Event()

    # Start the input and output coroutines
    cocotb.start_soon(supply_input_data(dut, input_data, input_done))
    await read_output_data(dut, output_data, input_data, input_done)

    await Timer(100, units="ns")

    # Compare the input data with the output data
    logger.debug(f"Input data: {input_data}, Output data: {output_data}")
    assert (
        input_data == output_data
    ), f"Expected output {input_data}, but got {output_data}."


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
