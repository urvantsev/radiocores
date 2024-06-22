import cocotb
from cocotb.triggers import RisingEdge, Timer, Event, with_timeout
from cocotb.clock import Clock
from radiocores.bin2gray import bin2gray
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="test.log",
    filemode="w",
    force=True,
)

async def supply_input_data(dut, input_data, input_done):
    """Coroutine to supply input data to the DUT"""
    for i in input_data:
        await RisingEdge(dut.clk)
        gray_code = bin2gray(i)
        logging.debug(f"Supplying input: {i}, gray code: {gray_code}")
        dut.i_dv.value = 1  # Set data valid signal
        dut.i_gray_code.value = gray_code
        await RisingEdge(dut.clk)
        dut.i_dv.value = 0  # Clear data valid signal after one cycle

    # Signal that input data supply is done
    input_done.set()


async def read_output_data(dut, output_data, input_data, input_done):
    """Coroutine to read output data from the DUT"""
    while not input_done.is_set():
        await with_timeout(
            RisingEdge(dut.clk), 5000, "ns"
        )  # Increased timeout to 5000 ns
        if dut.o_dv.value == 1:
            output = int(dut.o_binary_code.value)
            output_data.append(output)
            logging.debug(f"Read output: {output}")

    # Continue checking remaining items after all inputs are applied
    while len(output_data) < len(input_data):
        await with_timeout(
            RisingEdge(dut.clk), 1000, "ns"
        )  # Increased timeout to 1000 ns
        if dut.o_dv.value == 1:
            output = int(dut.o_binary_code.value)
            output_data.append(output)
            logging.debug(f"Read remaining output: {output}")


@cocotb.test()
async def gray2bin_simple_test(dut):
    """Test for DUT (design under test)"""

    logging.info("Running test!!!")

    # Create a clock
    clock = Clock(dut.clk, 10, units="ns")  # 100 MHz clock
    cocotb.start_soon(clock.start())  # Start the clock
    logging.debug("Clock started")

    # Reset the DUT
    dut.rst.value = 1
    await Timer(50, units="ns")  # Reset is active for 5 clock cycles
    logging.debug("Reset asserted")
    dut.rst.value = 0
    await Timer(50, units="ns")
    logging.debug("Reset deasserted")

    # Lists to keep track of inputs and outputs
    input_data = list(range(8))  # Example input data
    output_data = []

    # Event to signal the completion of input data supply
    input_done = Event()

    # Start the input and output coroutines
    cocotb.start_soon(supply_input_data(dut, input_data, input_done))
    await read_output_data(dut, output_data, input_data, input_done)

    await Timer(100, units="ns")

    # Compare the input data with the output data
    logging.debug(f"Input data: {input_data}, Output data: {output_data}")
    assert (
        input_data == output_data
    ), f"Expected output {input_data}, but got {output_data}."
