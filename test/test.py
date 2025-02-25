# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0


import cocotb  # Import the cocotb library, a coroutine-based cosimulation library for writing VHDL and Verilog testbenches in Python.
from cocotb.clock import Clock  # Import Clock to manage clock signals.
from cocotb.triggers import RisingEdge, ClockCycles  # Import necessary triggers for simulation events.

# Define a test as a coroutine, marked with the @cocotb.test decorator.
@cocotb.test()
async def test_tt_um_boolean(dut):
    # Setup a clock on the 'clk' signal of the device under test (dut) with a period of 10 ns.
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())  # Start the clock with a soon as possible scheduling.

    # Await a rising edge on the clock to synchronize to the clock period.
    await RisingEdge(dut.clk)
    # Reset the device by setting the 'rst_n' signal to 0 (active low reset).
    dut.rst_n.value = 0
    # Wait for 5 clock cycles with reset asserted to ensure a proper reset.
    await ClockCycles(dut.clk, 5)
    # De-assert the reset signal to allow normal operation.
    dut.rst_n.value = 1
    # Wait another 5 clock cycles after reset before starting the tests.
    await ClockCycles(dut.clk, 5)

    # Define test vectors as tuples of input values for A (ui_in) and B (uio_in).
    test_vectors = [(0x55, 0xAA), (0xF0, 0x0F), (0x00, 0xFF), (0xAA, 0x55)]
    # Iterate over each tuple in the test_vectors list.
    for a, b in test_vectors:
        # Assign the first element of the tuple to 'ui_in' and the second to 'uio_in'.
        dut.ui_in.value = a
        dut.uio_in.value = b
        # Wait for a rising edge on the clock before checking the output.
        await RisingEdge(dut.clk)
        # Calculate the expected output using the provided logic function.
        expected_output = (a & b) | (~a & b)
        # Assert to check if the actual device output matches the expected output.
        # If the assertion fails, the test will fail with the message showing the mismatch details.
        assert dut.uo_out.value == expected_output, f"Test failed with A={a:08b} B={b:08b} Expected={expected_output:08b} Got={dut.uo_out.value:08b}"

