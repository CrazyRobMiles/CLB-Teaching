EXERCISE = {
    "id": "ch4_lab3_dodging",
    "title": "Dodging",
    "concept": "reactive behaviour using the distance sensor to avoid head-on collision",

    "objective": (
        "Implement a dodging sumo program that advances toward the opponent, "
        "detects when the opponent is within DODGE_MM, swerves sideways to avoid "
        "contact, and resumes advancing. Use pixel colours to distinguish advancing "
        "from dodging."
    ),

    "off_limits": [
        "adding curving movement before the basic dodge-and-advance loop is working",
        "the random direction extension before the student has a fixed-direction dodge working",
    ],

    "hints": [
        "The dodge sequence is: turn sideways, move forward (which is now sideways "
        "relative to the arena), turn back. Use DODGE_ANGLE and -DODGE_ANGLE for "
        "the two turns.",

        "Always check mm > 0 before mm < DODGE_MM. A reading of -1 should not "
        "trigger a dodge — it just means the opponent is out of range.",

        "If the robot dodges but ends up facing the arena wall, reduce DODGE_ANGLE "
        "or DODGE_STEP so it does not swing too far off course.",

        "robot.random_val() returns 1–12. Values > 6 are about 50% likely, "
        "giving a roughly equal chance of dodging left or right.",

        "After a dodge the robot's heading has changed. Two equal and opposite turns "
        "(DODGE_ANGLE then -DODGE_ANGLE) bring it back to the original heading.",
    ],

    "success_indicators": [
        "robot advances when no opponent is detected",
        "robot dodges when opponent is within DODGE_MM",
        "pixel changes colour during dodge vs advance",
        "mm > 0 check prevents -1 from triggering a false dodge",
        "robot resumes forward heading after the dodge",
    ],

    "observation_checklist": [
        "Does the robot advance at all in clear conditions?",
        "Does the pixel turn yellow when the dodge triggers?",
        "Does the robot return to its original heading after dodging?",
        "Is the mm > 0 check present before the mm < DODGE_MM comparison?",
    ],

    "tutor_brief": """
You are a teaching assistant for an embedded programming course using the Hull
Pixelbot robot and the CLB-robot MicroPython library.

This student is working on Lab 3: Dodging. They are using the distance sensor to
make reactive decisions in the sumo game loop.

YOUR ROLE
- Help the student understand the turn-move-turn dodge sequence before they code it.
- Remind them that the sensor only reads between moves (blocking moves). This is
  intentional — the robot commits to the full dodge before checking again.
- Guide them to test first with a stationary opponent (robot switched off in the
  middle of the arena) before testing against a live opponent.
- Once the fixed-direction dodge works, suggest the random direction extension.

COMMON PROBLEMS

Robot keeps dodging even when arena is empty: mm > 0 check is missing — -1 is
triggering the dodge condition. Add the check.

Robot dodges but ends up facing the wrong way: the compensating turn at the end
has the wrong sign. Draw the sequence on paper: turn right → move → turn left.

Robot advances but never dodges: DODGE_MM is too small, or the sensor is not
reading correctly. Test the sensor reading by printing mm before the if statement.

Robot dodges repeatedly without advancing: DODGE_STEP is large enough that the
robot moves a long way sideways, and the next iteration finds the opponent still
within DODGE_MM (now to the side). Reduce DODGE_STEP or increase DODGE_ANGLE.

TONE
Be encouraging without being sycophantic. Brief is better than verbose.
""",
}
