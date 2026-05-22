EXERCISE = {
    "id": "ch4_lab2_charging",
    "title": "Charging",
    "concept": "maximum forward progress using a timed game loop",

    "objective": (
        "Implement a charging sumo program that advances the robot forward in the game "
        "loop for the full game duration, uses the pixel to show the robot is running, "
        "and optionally detects the instant-win condition by watching for a very short "
        "distance reading."
    ),

    "off_limits": [
        "adding sensor-based dodging before the basic charge is working",
        "using nowait=True until the student understands why blocking moves are simpler here",
    ],

    "hints": [
        "The simplest charge is just robot.move(100) inside the while loop. "
        "Each call moves 100 mm and blocks until done. The loop re-checks the time "
        "after each move.",

        "robot.colour(robot.RED) before the loop and robot.colour(robot.BLACK) after "
        "makes it obvious when the game is running and when it has ended.",

        "For the instant-win check: mm < 50 means the sensor is reading the far wall "
        "at close range. Use break to exit the game loop immediately.",

        "If the robot stalls against the opponent (steppers skip steps), "
        "the move() call still completes — the robot just does not travel as far. "
        "This is acceptable behaviour; the motors are not damaged by stalling.",
    ],

    "success_indicators": [
        "robot advances forward for the full game duration",
        "pixel is lit during the game and off at the end",
        "robot stops at the end of the game duration",
        "optional: robot breaks out of loop on mm < 50 (instant win)",
    ],

    "observation_checklist": [
        "Does the robot move at all after the countdown?",
        "Does the pixel turn off when time expires?",
        "How far does the robot travel in 30 seconds in an empty arena?",
        "What happens when it collides head-on with a stationary opponent?",
    ],

    "tutor_brief": """
You are a teaching assistant for an embedded programming course using the Hull
Pixelbot robot and the CLB-robot MicroPython library.

This student is working on Lab 2: Charging. This is the simplest sumo tactic —
drive forward for the whole game. The key teaching points are the timed game loop
pattern and using the pixel as a state indicator.

YOUR ROLE
- Help the student get a working charge program running before discussing optimisations.
- Explain that stalling the stepper motors (pushing against the opponent) does not
  cause damage — the motors just skip steps.
- Once the basic charge works, guide the student to add the instant-win sensor check.
- Encourage the student to test both against an empty arena and against a stationary
  opponent before moving on.

COMMON PROBLEMS

Robot does not move: the while condition is wrong, or move() is outside the loop.
Check that move() is indented inside the while block.

Robot moves once then stops: pass is still inside the loop — the student did not
replace it with move().

Robot charges past the game duration: time.time() is not being checked correctly.
Confirm that `start = time.time()` is before the loop, not inside it.

Instant-win check never triggers: the sensor is not reading < 50 mm at the far wall.
Adjust the threshold or check whether the sensor is working at close range.

TONE
Be encouraging without being sycophantic. Brief is better than verbose.
""",
}
