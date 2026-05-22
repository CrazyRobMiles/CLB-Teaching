EXERCISE = {
    "id": "ch2_lab1_basic_movement",
    "title": "Basic Movement",
    "concept": "blocking move() and turn() commands and using pixel colour to observe execution order",

    "objective": (
        "Use robot.move() and robot.turn() to drive the robot forward 300 mm, backward "
        "300 mm, turn 90 degrees clockwise, and turn 90 degrees anti-clockwise, with "
        "pixel colours set before and after each move to show when each statement runs."
    ),

    "off_limits": [
        "the nowait=True parameter — that is the subject of the next lab",
        "the seconds= parameter — that is the subject of Lab 3",
        "the full solution before the student has successfully made the robot move at all",
    ],

    "hints": [
        "move() and turn() both block — they do not return until the robot has stopped. "
        "Any code you put after a move() runs only when that move is complete.",

        "Use pixel colours to make the blocking behaviour visible: set a colour before "
        "the move and a different colour after. The second colour will only appear when "
        "the move finishes.",

        "Negative distances move backward: robot.move(-300) reverses 300 mm.",

        "Negative angles turn anti-clockwise: robot.turn(-90) turns left.",

        "If the robot turns more or less than expected, adjust WHEEL_SPACING_MM in "
        "config.py. A larger value reduces the actual turn angle for a given command.",
    ],

    "success_indicators": [
        "robot moves forward and stops at approximately 300 mm",
        "robot returns to approximately its starting position",
        "robot turns 90 degrees clockwise then returns to original heading",
        "pixel colour changes correspond to the start and end of each move",
        "student can explain why the pixel does not change during a move",
    ],

    "observation_checklist": [
        "Do the ULN2003 indicator LEDs light up during a move command?",
        "Are both motors running? If only one runs, check the pin assignments in config.py.",
        "Does the robot move in the right direction? If it goes backward instead of forward, "
        "reverse the pin order for one motor in config.py.",
        "Is the pixel colour changing at all? Have you called robot.init() first?",
    ],

    "tutor_brief": """
You are a teaching assistant for an embedded programming course using the Hull
Pixelbot robot and the CLB-robot MicroPython library.

This student is working on Lab 1: Basic Movement. They are learning to use move()
and turn() and observing that these functions block until the robot stops.

YOUR ROLE
- Help the student understand that move() and turn() do not return until the robot
  has stopped. Use the pixel colour analogy: the colour you set before a move stays
  lit for the full duration.
- Guide them to use negative values for backward and left-turn.
- If the robot does not move: check ULN2003 LEDs, check pin assignments in config.py,
  check that VBUS (5 V) is connected to motor VCC.
- Do NOT introduce nowait=True or seconds= — those are covered in later labs.

COMMON PROBLEMS

Only one motor moves: pin assignment for one motor is wrong in config.py.
Ask the student to check which motor responds and compare its pins to config.py.

Robot spins instead of going straight: the pin ORDER for one motor is wrong.
Reversing the pins list for that motor in config.py reverses its direction.

Motors click but do not turn: VBUS is not connected to ULN2003 VCC — the motors
are running on 3.3 V which is insufficient. They need 5 V.

Robot moves wrong direction: swap the sign on the mm argument, or swap the motors
in config.py.

TONE
Be encouraging without being sycophantic. Brief is better than verbose.
""",
}
