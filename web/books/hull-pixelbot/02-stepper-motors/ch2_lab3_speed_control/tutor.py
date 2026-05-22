EXERCISE = {
    "id": "ch2_lab3_speed_control",
    "title": "Speed Control",
    "concept": "controlling movement speed with the seconds= parameter",

    "objective": (
        "Use the seconds= parameter on move() and turn() to control how long a movement "
        "takes, combine it with nowait=True to flash a pixel while the robot moves slowly, "
        "and observe that seconds= cannot make the robot move faster than its maximum speed."
    ),

    "off_limits": [
        "the minimum useful speed limit before the student has experimented with it",
    ],

    "hints": [
        "seconds= specifies the total time for the whole move, not the time per step. "
        "robot.move(200, seconds=10) means 200 mm in 10 seconds.",

        "If you give seconds= a value that would require stepping faster than the "
        "hardware minimum (1200 µs per step), the motor simply runs at maximum speed. "
        "You cannot go faster than maximum.",

        "Combining seconds= with nowait=True is very useful: you can do other things "
        "(like updating pixels) while the robot moves slowly.",

        "Very slow moves (e.g. seconds=30 for 200 mm) may produce stuttering because "
        "the gear train needs a minimum amount of torque to move reliably.",
    ],

    "success_indicators": [
        "slow move visibly takes longer than full-speed move",
        "seconds= + nowait=True + while moving() loop all work together",
        "student can explain why seconds= cannot make the robot move faster",
    ],

    "observation_checklist": [
        "Is seconds= being passed as a keyword argument: move(200, seconds=5)?",
        "Is nowait=True also present when using while robot.moving()?",
        "Does the pixel flash stop when the move finishes?",
    ],

    "tutor_brief": """
You are a teaching assistant for an embedded programming course using the Hull
Pixelbot robot and the CLB-robot MicroPython library.

This student is working on Lab 3: Speed Control. They are learning to use the
seconds= parameter to spread a move over a longer time, and to combine it with
nowait=True to do other things while the robot moves slowly.

YOUR ROLE
- Help the student understand that seconds= controls duration, not speed directly.
- Explain why the motor cannot go faster than its hardware minimum step rate.
- Guide them to combine seconds= with nowait=True and while robot.moving().

COMMON PROBLEMS

seconds= has no effect: the student is passing it as a positional argument.
It must be a keyword argument: move(200, seconds=5) not move(200, 5).

Robot stutters at very slow speeds: the gear train needs minimum torque. Suggest
increasing the speed slightly — seconds=20 for 200 mm is about the practical limit.

TONE
Be encouraging without being sycophantic. Brief is better than verbose.
""",
}
