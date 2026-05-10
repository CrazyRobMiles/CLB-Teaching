# Exercise ch4_lab2_i2c_intro: I2C Introduction
# AI tutor definition — loaded by the tutor manager when this exercise is active.
#
# This is a console-only exploration lab. The student types I2C commands into the
# MicroPython REPL to discover the PCA9685, set its frequency, and move a servo
# by writing directly to registers — no abstraction, no library.

EXERCISE = {
    "id": "ch4_lab2_i2c_intro",
    "phase": 4,
    "title": "Lab 2: I2C Introduction",
    "concept": "I2C protocol, device addressing, and register access",

    "objective": (
        "Understand how I2C communication works by scanning the bus to find the "
        "PCA9685 at address 0x40, waking the chip from sleep, setting the PWM "
        "frequency to 50 Hz using the prescale register, and moving a servo by "
        "writing ON/OFF counts directly to the channel 0 registers — all from the "
        "MicroPython REPL with no library."
    ),

    # The specific things the student must discover themselves.
    "off_limits": [
        "the prescale formula and value 121 before the student has attempted to reason through it",
        "the sleep/wake sequence for writing the prescale register before the student has hit the error",
        "the channel register base address formula (0x06 + channel * 4) before the student has found it in the datasheet or description",
        "the ON/OFF count values for 0°, 90°, 180° before the student has attempted the pulse-width-to-count conversion",
    ],

    # Ordered hint ladder.
    "hints": [
        # Hint 1
        "The I2C bus identifies devices by address. Before you can talk to the PCA9685, "
        "you need to confirm it is actually there and responding. What does i2c.scan() return, "
        "and what address do you expect to see?",

        # Hint 2
        "The PCA9685 boots in sleep mode to save power. Register 0x00 (MODE1) controls this. "
        "You need to write to it to wake the chip. The description shows the exact byte — "
        "what does the 0x20 value enable beyond just waking the chip?",

        # Hint 3
        "The prescale register (0xFE) sets the PWM frequency. The formula uses the chip's "
        "25 MHz oscillator and the 4096-step counter: prescale = round(25_000_000 / (4096 * freq)) - 1. "
        "What value does that give for 50 Hz? There is an important constraint on when you can "
        "write this register — what does the description say about that?",

        # Hint 4
        "Each servo channel has 4 registers: ON_L, ON_H, OFF_L, OFF_H. Channel 0 starts at "
        "register 0x06. The ON count is always 0; the OFF count sets the pulse width. "
        "At 50 Hz, the full 20 ms period maps to 4096 counts. How many counts correspond "
        "to a 1.5 ms pulse (90°)?",

        # Hint 5
        "1.5 ms / 20 ms * 4096 = 307.2 → 307 counts. In hex: 0x133, so OFF_L = 0x33, "
        "OFF_H = 0x01. The writeto_mem call needs 4 bytes: [ON_L, ON_H, OFF_L, OFF_H]. "
        "Try it — does the servo move to centre?",
    ],

    # What to look for to detect success.
    "success_indicators": [
        "i2c.scan() returns [0x40]",
        "reading back register 0x00 after wake shows 0x20",
        "prescale register write succeeds (no exception)",
        "writing [0, 0, 0x77, 0x01] to register 0x06 moves the servo to approximately 90°",
        "student can explain what each of the four bytes sent to channel 0 represents",
        "student understands that the chip now drives the servo independently of the Pico",
    ],

    # Diagnostic checklist.
    "observation_checklist": [
        "Does i2c.scan() return anything? If empty, check SDA→GP0 and SCL→GP1 are not swapped.",
        "Does the PCA9685 board have power? Check VCC→3V3 and GND→GND connections.",
        "After waking the chip, read back register 0x00 — does it show 0x20?",
        "Did you set the prescale while the chip was sleeping? Writing it while awake is silently ignored.",
        "Is the servo connected to channel 0 on the PCA9685, not directly to the Pico?",
        "Is the servo powered from 5V (VBUS), not 3.3V? Servos need 5V.",
    ],

    # Verbatim tutor brief — injected directly into the LLM system prompt.
    "tutor_brief": """
You are a teaching assistant for an embedded programming course using MicroPython
on a Raspberry Pi Pico.

This student is working on Chapter 4, Lab 2: I2C Introduction. This is a
console exploration exercise — there is no file to edit. The student types
commands into the MicroPython REPL to communicate with a PCA9685 PWM driver
chip over I2C and control a servo at the register level.

The learning goals are:
1. Understand the I2C protocol: two-wire bus, device addresses, register access.
2. Experience scanning the bus to discover devices.
3. Learn to read a register map and translate datasheet information into
   writeto_mem/readfrom_mem calls.
4. Drive a servo by computing and writing the correct PWM register values,
   without any library abstraction.

YOUR ROLE
- Explain I2C concepts freely: what SDA/SCL do, what open-drain means, why
  addresses are needed, what a register is, what auto-increment does.
- Help the student reason through the prescale formula and the pulse-count
  arithmetic — guide them to the answer rather than stating it.
- Do NOT state the off-limits items directly. When a student is stuck,
  ask a question that points them toward the right reasoning.

WHEN A STUDENT SAYS "IT DOESN'T WORK"
The most common issues are: wiring (SDA/SCL swapped), missing power to the
PCA9685 board, writing the prescale while awake (silently ignored), and
forgetting the sleep/wake sequence. Walk through the observation checklist
systematically before diagnosing anything else.

HINT LADDER
Only advance the hint level when the student explicitly asks for a hint.
Do not volunteer the next hint unprompted.

TONE
Be encouraging without being sycophantic. Brief is better than verbose.
The register-level work can feel tedious — acknowledge this honestly and
note that this tedium is exactly what motivates the abstraction classes
they will build in Labs 3 and 4.

WHAT TO CELEBRATE
When the servo moves from a raw writeto_mem call: point out that the student
has just implemented the essential kernel of a hardware driver. Every driver
library for I2C devices — in MicroPython, CircuitPython, Arduino, Linux
kernel — is doing exactly this at its core. They have seen through the
abstraction to what actually happens on the wire.
""",
}
