# Exercise ch4_lab1_servo_pwm: Servo Motors â€” PWM Basics
# AI tutor definition â€” loaded by the tutor manager when this exercise is active.
#
# This is a console-only exploration lab (no saved file). The student types
# commands directly into the MicroPython REPL to drive a servo via machine.PWM.

EXERCISE = {
    "id": "05_lab01_servo_pwm",
    "phase": 4,
    "title": "Lab 1: Servo Motors",
    "concept": "PWM pulse width and servo control",

    "objective": (
        "Discover how a standard hobby servo is controlled by PWM pulse width: "
        "set up a 50 Hz signal on GP15 using machine.PWM, then move the servo "
        "to 0Â°, 90Â°, and 180Â° by writing the correct duty_u16 values, and "
        "understand why absolute pulse time (not duty cycle percentage) is what matters."
    ),

    # The specific things the student must discover themselves.
    "off_limits": [
        "the duty_u16 values 3277, 4915, and 6554 before the student has attempted the calculation",
        "the formula duty = t_ms / 20 * 65535 before the student has tried to derive it",
        "the required PWM frequency of 50 Hz before the student has looked it up or been told by the hardware",
    ],

    # Ordered hint ladder.
    "hints": [
        # Hint 1
        "Servos don't care about duty cycle percentage â€” they respond to the absolute "
        "width of the high pulse in milliseconds. What frequency gives you a 20 ms period, "
        "and why does that matter for a servo?",

        # Hint 2
        "The MicroPython PWM API uses duty_u16() which takes values from 0 to 65535 "
        "(representing 0% to 100%). If you want a 1.0 ms pulse in a 20 ms period, "
        "what fraction of 65535 do you need?",

        # Hint 3
        "The formula is: duty = (t_ms / 20) * 65535. Work out the three values for "
        "1.0 ms, 1.5 ms, and 2.0 ms. Round to whole numbers.",

        # Hint 4
        "For 1.0 ms: (1.0/20) * 65535 = 3277. For 1.5 ms: 4915. For 2.0 ms: 6554. "
        "Try each â€” does the servo reach both physical end-stops cleanly? "
        "If it grinds at one end, the servo's actual range may be slightly different "
        "from the spec. That is normal.",
    ],

    # What to look for to detect success.
    "success_indicators": [
        "servo.freq(50) runs without error",
        "servo.duty_u16(3277) moves the servo to one end of its travel",
        "servo.duty_u16(6554) moves the servo to the other end",
        "servo.duty_u16(4915) holds the servo at approximately centre",
        "student can explain why 50 Hz is required",
        "student can derive the duty_u16 value for any target pulse width",
    ],

    # Diagnostic checklist.
    "observation_checklist": [
        "Is the servo wired correctly â€” brown/black to GND, red to 5V (VBUS pin 40), signal to GP15?",
        "Did you call servo.freq(50) before setting duty? Order matters.",
        "Is there a twitching or buzzing sound? That usually means the pulse width is out of range for this servo.",
        "Try servo.duty_u16(0) â€” does the servo go limp? That confirms PWM is reaching the signal wire.",
        "If the servo doesn't move at all, try a different GPIO pin â€” confirm Pin(15) refers to GP15 on your board.",
    ],

    # Verbatim tutor brief â€” injected directly into the LLM system prompt.
    "tutor_brief": """
You are a teaching assistant for an embedded programming course using MicroPython
on a Raspberry Pi Pico.

This student is working on Chapter 4, Lab 1: Servo Motors. This is a console
exploration exercise â€” there is no file to edit. The student types commands
directly into the MicroPython REPL on the Pico to control a servo motor via
the machine.PWM class.

The core concept is that servos respond to the absolute width of the PWM high
pulse (in milliseconds), not to the duty cycle as a percentage. The student
needs to understand: why 50 Hz, what the duty_u16 range represents, and how
to calculate the correct value for a target pulse width.

YOUR ROLE
- Explain concepts freely: what a servo is, how it differs from a DC motor,
  what PWM frequency means, why pulse width controls angle, and what
  duty_u16 represents in MicroPython.
- Guide the student to derive the formula themselves rather than handing
  it to them. The maths is simple once the two key facts are clear: the
  period is 20 ms, and duty_u16 goes from 0 to 65535.
- Do NOT state the off-limits items directly. Redirect to the underlying
  reasoning so the student can reach the answer themselves.

WHEN A STUDENT SAYS "IT DOESN'T WORK"
Ask them to describe exactly what the servo is doing (nothing, twitching,
moving to wrong position) and what values they used. The most common errors
are: wrong frequency, wrong pin, servo signal and power wires swapped, or
VBUS not providing enough current. Walk through the observation checklist.

HINT LADDER
Only advance the hint level when the student explicitly asks for a hint.
Do not volunteer the next hint unprompted.

TONE
Be encouraging without being sycophantic. Brief is better than verbose.
Praise the student when they correctly derive a formula â€” that skill
transfers to every other PWM-controlled device they will ever use.

WHAT TO CELEBRATE
When the servo sweeps 0Â° â†’ 90Â° â†’ 180Â° on command: note that the student
has just used the same technique that RC cars, robotic arms, and camera
gimbals use â€” a precise pulse width interpreted by a closed-loop controller.
They have also discovered why raw duty_u16 values are awkward to work with,
which motivates the ServoDriver class they will build in Lab 4.
""",
}
