

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles




@cocotb.test()
async def test_exhaustive_logic(dut):
    dut._log.info("Start")


    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
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


    dut._log.info("Starting exhaustive test cases...")


    # Iterate through all 256 × 256 combinations of A and B
    for a in range(256):  # 0 to 255 (0b00000000 to 0b11111111)
        for b in range(256):  
            # Compute expected values based on the logic table
            not_a = ~a & 0xFF  # Ensuring 8-bit representation
            a_and_b = a & b
            not_a_and_b = not_a & b
            expected_output = a_and_b | not_a_and_b  # (A ∧ B) ∨ (¬A ∧ B)


            # Assign values
            dut.ui_in.value = a
            dut.uio_in.value = b


            # Wait for one clock cycle
            await ClockCycles(dut.clk, 1)


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


    dut._log.info("All exhaustive test cases passed successfully!")




