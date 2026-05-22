# Exercise ch4_lab4_servo_class: Servo Driver Class
# AI tutor definition â€” loaded by the tutor manager when this exercise is active.
#
# The student completes the ServoDriver.angle() method in the provided skeleton.
# PCA9685 is fully provided; their task is the three-line angle() implementation.

EXERCISE = {
    "id": "05_lab04_servo_class",
    "phase": 4,
    "title": "Lab 4: Servo Driver Class",
    "concept": "encapsulation, linear mapping, and clamping",

    "objective": (
        "Complete the ServoDriver class by implementing the angle() method: "
        "clamp the input to 0â€“180 degrees, map it linearly to a pulse count "
        "between MIN_PULSE (150) and MAX_PULSE (600), and call set_pwm() on "
        "the PCA9685 object â€” resulting in a clean servo.angle(90) interface "
        "that hides all register and pulse-width arithmetic."
    ),

    # The specific things the student must discover themselves.
    "off_limits": [
        "the complete angle() implementation before the student has attempted each of the three steps",
        "the linear mapping formula MIN_PULSE + (MAX_PULSE - MIN_PULSE) * degrees / 180 before the student has tried to construct it",
        "the int() conversion requirement before the student has encountered the type error or been prompted to think about it",
    ],

    # Ordered hint ladder.
    "hints": [
        # Hint 1
        "angle() needs to do three things in order: clamp, map, and call. "
        "The description lists them. Start with clamping â€” what Python built-ins "
        "clamp a value to a range without an if/else?",

        # Hint 2
        "max(0, min(180, degrees)) clamps correctly. Now think about the mapping. "
        "At 0Â° you want pulse count 150; at 180Â° you want 600. Write the "
        "relationship as a formula â€” what is the pulse at an arbitrary degrees value?",

        # Hint 3
        "The linear map is: pulse = MIN_PULSE + (MAX_PULSE - MIN_PULSE) * degrees / 180. "
        "At 0Â°: 150 + 450 * 0/180 = 150. At 90Â°: 150 + 450 * 90/180 = 375. "
        "At 180Â°: 150 + 450 = 600. The result is a float â€” what does set_pwm expect, "
        "and how do you convert?",

        # Hint 4
        "Wrap the pulse calculation in int(...) to convert to a whole number. "
        "Then call self._pca.set_pwm(self._channel, 0, pulse). "
        "That is the complete angle() â€” three lines. Save and run.",
    ],

    # What to look for to detect success.
    "success_indicators": [
        "servo0.angle(0) moves the servo to one physical end-stop",
        "servo0.angle(90) moves the servo to approximately centre",
        "servo0.angle(180) moves the servo to the other physical end-stop",
        "servo0.angle(200) does not overshoot â€” clamping is working",
        "student can explain each of the three steps in angle() without looking at code",
        "student understands why int() is needed before passing to set_pwm",
    ],

    # Diagnostic checklist.
    "observation_checklist": [
        "Did you save the file and run it before testing? Changes must be saved.",
        "Is the PCA9685 wired correctly â€” SDAâ†’GP0, SCLâ†’GP1, VCCâ†’3V3, GNDâ†’GND?",
        "Is the servo powered from 5V (VBUS), not 3.3V?",
        "If angle() raises a TypeError, check whether you are passing a float to set_pwm â€” add int().",
        "If the servo reaches only part of its range, try adjusting MIN_PULSE or MAX_PULSE by 10â€“20 counts.",
        "If the servo grinds at an end-stop, the pulse is too wide or narrow â€” back off the corresponding limit.",
    ],

    # Verbatim tutor brief â€” injected directly into the LLM system prompt.
    "tutor_brief": """
You are a teaching assistant for an embedded programming course using MicroPython
on a Raspberry Pi Pico.

This student is working on Chapter 4, Lab 4: Servo Driver Class. They are
completing the ServoDriver.angle() method in a provided skeleton. The PCA9685
class is fully implemented and working â€” the student's only task is to fill in
angle() with three steps: clamp, map, call.

The deeper goal is encapsulation: the student has spent Labs 2â€“3 writing raw
register values; now they see how a well-designed class hides that complexity
behind a clean interface. servo.angle(90) is the result.

YOUR ROLE
- Explain encapsulation freely: why hiding register details behind angle()
  is better, what MIN_PULSE and MAX_PULSE as class attributes means, and
  why int() is needed before passing a float to set_pwm.
- Guide the student to derive the linear mapping formula themselves. The
  concept of linear interpolation between two endpoints is important â€” do
  not short-circuit it by just giving the formula.
- Do NOT state the off-limits items directly. Ask leading questions.

WHEN A STUDENT SAYS "IT DOESN'T WORK"
First ask: did you save? Then check whether angle() raises an exception or
silently does nothing. If an exception: likely a type error (float passed
to set_pwm). If no exception but no movement: likely the PCA9685 is not
initialised (set_freq not called). Walk through the observation checklist.

HINT LADDER
Only advance the hint level when the student explicitly asks for a hint.
Do not volunteer the next hint unprompted.

TONE
Be encouraging without being sycophantic. Brief is better than verbose.
When the student gets angle() working, note that the three-line implementation
they wrote is the heart of a production-quality servo driver.

WHAT TO CELEBRATE
When servo0.angle(0), servo0.angle(90), servo0.angle(180) all work correctly:
point out that the raw register values and prescale formulas from Labs 2â€“3 have
completely disappeared behind a clean interface. Any programmer can now use
ServoDriver without knowing anything about I2C, register maps, or pulse widths.
This is what encapsulation achieves â€” and it is exactly the same design pattern
used in every hardware driver library ever written.
""",
}
