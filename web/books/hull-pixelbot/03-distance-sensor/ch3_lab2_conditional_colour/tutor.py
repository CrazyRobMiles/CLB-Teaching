EXERCISE = {
    "id": "ch3_lab2_conditional_colour",
    "title": "Conditional Colour",
    "concept": "if/elif/else chains and reactive behaviour using sensor readings",

    "objective": (
        "Use an if/elif/else chain inside a while True loop to set the pixel colour "
        "based on the current distance reading, producing a three-zone colour display "
        "that updates continuously."
    ),

    "off_limits": [
        "the complete if/elif/else solution before the student has attempted it",
        "the fourth blue zone before the student has the three-zone version working",
    ],

    "hints": [
        "Test conditions in the if/elif chain from most-specific to least-specific. "
        "Check mm < 0 first, then mm < 100, then mm < 300, then use else for everything else.",

        "Each elif is only reached if all preceding conditions were False. So elif mm < 300 "
        "is only reached when mm >= 0 and mm >= 100.",

        "The while True loop will run as fast as the sensor allows. The time taken by the "
        "colour function call provides sufficient recovery time between readings.",

        "If the pixel flickers unexpectedly between colours, the reading is near a threshold. "
        "This is normal — try adjusting the threshold values.",
    ],

    "success_indicators": [
        "pixel shows correct colour for each distance zone",
        "pixel updates smoothly as hand moves toward/away from sensor",
        "white (or black) appears correctly for -1 readings",
        "student can explain why elif rather than if is used for each subsequent condition",
    ],

    "observation_checklist": [
        "Does the pixel change colour at all when you move your hand?",
        "Is the sensor returning valid readings (not always -1)?",
        "Are the elif conditions in the right order (smallest threshold first)?",
        "Is the distance read inside the while loop, not outside it?",
    ],

    "tutor_brief": """
You are a teaching assistant for an embedded programming course using the Hull
Pixelbot robot and the CLB-robot MicroPython library.

This student is working on Lab 2: Conditional Colour. They are building their first
reactive behaviour: reading a sensor and changing an output based on the value.

YOUR ROLE
- Help the student understand that elif conditions are tested in order, and each
  is only reached if all preceding conditions were False.
- The most common mistake is putting conditions in the wrong order — ask the student
  to trace through the chain manually with mm=50, mm=150, mm=500.
- Encourage them to adjust threshold values to match their physical setup.

COMMON PROBLEMS

Pixel always shows the same colour: conditions are in the wrong order, or mm < 0
check is missing and -1 is being treated as a valid distance.

Pixel never shows red (or never shows yellow): the threshold values are too large
or too small. Ask the student to print mm alongside the colour to see what readings
they are actually getting.

Pixel does not update: the distance call is outside the while loop. Ask the student
to check where in the code mm is assigned.

TONE
Be encouraging without being sycophantic. Brief is better than verbose.
""",
}
