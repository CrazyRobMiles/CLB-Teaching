EXERCISE = {
    "id": "ch1_lab1_pixel_colours",
    "title": "Pixel Colours",
    "concept": "NeoPixel control using colour constants and the colour() function",

    "objective": (
        "Import the robot library, call robot.init() to set up the hardware from "
        "config.py, and use the eight colour constants (RED, GREEN, BLUE, CYAN, "
        "MAGENTA, YELLOW, WHITE, BLACK) with robot.colour() and time.sleep() to "
        "produce a timed colour sequence on the pixel strip."
    ),

    "off_limits": [
        "passing a custom (r, g, b) tuple before the student has tried all eight constants",
        "the full solution before the student has made at least one colour change work",
    ],

    "hints": [
        "robot.init() with no arguments reads pin numbers and pixel count from config.py. "
        "You should not need to pass any arguments unless your wiring differs from the defaults.",

        "robot.colour(robot.RED) sets ALL pixels on the strip to red and returns "
        "immediately — there is no delay built in. You need time.sleep() to make the colour "
        "visible for a useful amount of time.",

        "robot.colour(robot.BLACK) turns all pixels off. Use it at the end of your program "
        "so the strip does not stay lit after the program finishes.",

        "If nothing lights up, check that PIXEL_PIN in config.py matches the GPIO pin your "
        "data wire is connected to.",
    ],

    "success_indicators": [
        "strip changes colour visibly in response to each robot.colour() call",
        "pauses between colour changes are clearly visible",
        "strip ends dark after the program completes",
        "student can explain that colour constants are (r, g, b) tuples",
    ],

    "observation_checklist": [
        "Does the strip light at all when you call robot.colour(robot.RED)?",
        "Is the data wire connected to the correct GPIO pin listed in config.py?",
        "Is PIXEL_COUNT in config.py set to the correct number of LEDs on your strip?",
        "Have you called robot.init() before any robot.colour() call?",
    ],

    "tutor_brief": """
You are a teaching assistant for an embedded programming course using the Hull
Pixelbot robot and the CLB-robot MicroPython library.

This student is working on Lab 1: Pixel Colours. They are learning to import the
robot library, initialise the hardware, and set the NeoPixel strip to solid colours
using the eight colour constants and the robot.colour() function.

YOUR ROLE
- Help the student understand that robot.init() reads from config.py — they should
  not need to pass arguments unless their wiring differs from the defaults.
- Explain that robot.colour() sets all pixels at once and returns immediately — there
  is no built-in delay.
- Guide them to use time.sleep() to pace colour changes.
- Once they have used all eight constants, mention that any (r, g, b) tuple works too.

COMMON PROBLEMS

Nothing lights up: PIXEL_PIN in config.py is wrong, or robot.init() has not been
called yet. Ask the student to check config.py and confirm init() is at the top.

Strip lights immediately with no delay: the student has forgotten time.sleep().
Ask them what they think will happen if there is no pause between colour calls.

Only some pixels light: PIXEL_COUNT is set lower than the actual strip length.

TONE
Be encouraging without being sycophantic. Brief is better than verbose.
A well-placed question beats a paragraph of explanation.
""",
}
