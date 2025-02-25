import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_manual_logic(dut):
    dut._log.info("Start Manual Test")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset the DUT
    dut._log.info("Reset")
    dut.ena.value = 1  # Enable the DUT
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0  # Assert reset
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1  # Deassert reset
    await ClockCycles(dut.clk, 5)

    dut._log.info("Starting Manual Test Cases...")

    # Define manual test cases (A, B) and expected output
    test_cases = [
        (0b11001100, 0b10101010),  # Test Case 1
        (0b11110000, 0b00001111),  # Test Case 2
        (0b00000000, 0b11111111),  # Test Case 3
        (0b10101010, 0b01010101),  # Test Case 4
        (0b11111111, 0b11111111),  # Test Case 5 (All bits high)
        (0b00000000, 0b00000000),  # Test Case 6 (All bits low)
        (0b10000000, 0b00000001),  # Test Case 7 (Edge case)
    ]

    for a, b in test_cases:
        # Compute expected values
        not_a = ~a & 0xFF  # Ensuring 8-bit representation
        a_and_b = a & b
        not_a_and_b = not_a & b
        expected_output = a_and_b | not_a_and_b  # (A ∧ B) ∨ (¬A ∧ B)

        # Assign values
        dut.ui_in.value = a
        dut.uio_in.value = b

        # Wait for a few clock cycles to observe changes
        await ClockCycles(dut.clk, 2)

        # Capture and validate the output
        actual_output = dut.uo_out.value.integer
        dut._log.info(
            f"A={a:08b}, B={b:08b}, ¬A={not_a:08b}, A∧B={a_and_b:08b}, ¬A∧B={not_a_and_b:08b}, "
            f"Expected Output={expected_output:08b}, Got={actual_output:08b}"
        )

        assert actual_output == expected_output, (
            f"Test failed for A={a:08b}, B={b:08b}. "
            f"Expected={expected_output:08b}, Got={actual_output:08b}"
        )

        # Extra delay to observe the waveform more clearly
        await ClockCycles(dut.clk, 5)

    dut._log.info("All manual test cases passed successfully!")



