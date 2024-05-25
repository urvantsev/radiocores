import cocotb
from cocotb.triggers import Timer, RisingEdge, Event
from cocotb.clock import Clock
import logging
from radiocores.bin2gray import bin2gray
from pyuvm import (
    uvm_sequence,
    uvm_driver,
    uvm_monitor,
    uvm_env,
    uvm_test,
    ConfigDB,
    uvm_root,
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Gray2BinSequence(uvm_sequence):
    async def body(self):
        dut = self.dut
        input_data = ConfigDB().get(self, "", "input_data")
        for i in input_data:
            await RisingEdge(dut.clk)
            gray_code = bin2gray(i)
            logger.debug(f"Supplying input: {i}, gray code: {gray_code}")
            dut.i_dv.value = 1
            dut.i_gray_code.value = gray_code
            await RisingEdge(dut.clk)
            dut.i_dv.value = 0


class Gray2BinDriver(uvm_driver):
    async def run_phase(self):
        while True:
            seq = await self.seq_item_port.get_next_item()
            await seq.body()
            self.seq_item_port.item_done()


class Gray2BinMonitor(uvm_monitor):
    async def run_phase(self):
        dut = self.dut
        output_data = ConfigDB().get(self, "", "output_data")
        input_data = ConfigDB().get(self, "", "input_data")
        input_done = ConfigDB().get(self, "", "input_done")
        while not input_done.is_set():
            await RisingEdge(dut.clk)
            if dut.o_dv.value == 1:
                output = int(dut.o_binary_code.value)
                output_data.append(output)
                logger.debug(f"Read output: {output}")
        while len(output_data) < len(input_data):
            await RisingEdge(dut.clk)
            if dut.o_dv.value == 1:
                output = int(dut.o_binary_code.value)
                output_data.append(output)
                logger.debug(f"Read remaining output: {output}")


class Gray2BinEnv(uvm_env):
    def build_phase(self):
        self.driver = Gray2BinDriver("driver", self)
        self.monitor = Gray2BinMonitor("monitor", self)

    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seq_item_export)


class Gray2BinTest(uvm_test):
    async def run_phase(self):
        self.raise_objection()
        dut = self.dut
        clock = Clock(dut.clk, 10, units="ns")
        cocotb.start_soon(clock.start())
        logger.debug("Clock started")
        dut.rst.value = 1
        await Timer(50, units="ns")
        logger.debug("Reset asserted")
        dut.rst.value = 0
        await Timer(50, units="ns")
        logger.debug("Reset deasserted")

        input_data = list(range(10))
        output_data = []
        input_done = Event()

        ConfigDB().set(None, "*", "input_data", input_data)
        ConfigDB().set(None, "*", "output_data", output_data)
        ConfigDB().set(None, "*", "input_done", input_done)

        seq = Gray2BinSequence("seq")
        seq.dut = dut
        await seq.start()

        self.env = Gray2BinEnv("env", self)
        self.env.build_phase()
        self.env.connect_phase()
        self.env.run_phase()

        await Timer(100, units="ns")

        logger.debug(f"Input data: {input_data}, Output data: {output_data}")
        assert (
            input_data == output_data
        ), f"Expected output {input_data}, but got {output_data}."
        self.drop_objection()


@cocotb.test()
async def test_uvm_gray2bin(dut):
    uvm_root().run_test("Gray2BinTest")
