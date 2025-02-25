# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_tt_um_boolean(dut):
    dut._log.info("Start")

    # Set the clock period to 10 ns
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)

    dut._log.info("Testing Specific Cases")

    # Define test vectors (A, B) with expected output computation
    test_vectors = [
        (11001100, 10101010),  # Test Case 1: Alternating bit pattern (high bits with interleaved 1s and 0s)
        (11110000, 00001111),  # Test Case 2: Upper half bits are 1s, lower half bits are 0s (and vice versa for B)
        (00000000, 11111111),  # Test Case 3: A is all zeros, B is all ones (edge case)
        (10101010, 01010101)   # Test Case 4: Complementary bit pattern (each bit in A is the opposite of B)
    ]

    for a, b in test_vectors:
        # Assign inputs
        dut.ui_in.value = a
        dut.uio_in.value = b
        await ClockCycles(dut.clk, 1)

        # Compute expected output using logic function
        expected_output = (a & b) | (~a & b)

        # Log expected values
        dut._log.info(f"Testing A={a:08b}, B={b:08b}, Expected Output={expected_output:08b}")

        # Assert correctness
        assert dut.uo_out.value == expected_output, (
            f"Test failed with A={a:08b} B={b:08b} "
            f"Expected={expected_output:08b} Got={dut.uo_out.value:08b}"
        )

        dut._log.info(f"Test Passed: A={a:08b}, B={b:08b}, Output={expected_output:08b}")

    dut._log.info("All Test Cases Passed Successfully")


