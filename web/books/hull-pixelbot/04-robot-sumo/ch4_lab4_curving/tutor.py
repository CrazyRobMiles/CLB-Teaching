EXERCISE = {
    "id": "ch4_lab4_curving",
    "title": "Curving",
    "concept": "using arc() to approach the opponent from an angle rather than head-on",

    "objective": (
        "Implement a curving sumo program that uses alternating arc() calls to weave "
        "across the arena, switches to a straight charge when the opponent is detected "
        "at close range, and uses pixel colours to distinguish curving from charging."
    ),

    "off_limits": [
        "complex multi-phase strategies before the basic weave is working",
    ],

    "hints": [
        "arc(radius, angle) with alternating sign on radius produces a weave. "
        "Store the sign in a variable called direction (1 or -1) and flip it "
        "with direction = -direction after each arc.",

        "ARC_RADIUS controls how curved the path is. 300 mm radius with 40-degree "
        "segments gives a gentle weave that still makes net forward progress.",

        "The robot's heading changes with every arc segment. After many alternating "
        "arcs the net heading should be roughly forward — check this by observing "
        "the robot in an empty arena.",

        "For the close-range charge: use mm > 0 and mm < 150. When the sensor reads "
        "this low the opponent is directly ahead and very close — arc moves would "
        "steer away from them, so a straight move is better.",
    ],

    "success_indicators": [
        "robot weaves left-right across the arena while advancing",
        "robot switches to straight move when opponent is within 150 mm",
        "pixel is blue during weave and red during close-range charge",
        "robot ends within the game time limit",
    ],

    "observation_checklist": [
        "Does the robot trace a visible weave path in an empty arena?",
        "Does the direction variable flip after each arc?",
        "Does the pixel turn red when the close-range condition triggers?",
        "Does the robot make net forward progress (not just oscillate in place)?",
    ],

    "tutor_brief": """
You are a teaching assistant for an embedded programming course using the Hull
Pixelbot robot and the CLB-robot MicroPython library.

This student is working on Lab 4: Curving. They are using arc() to create an
unpredictable approach path in the sumo arena.

YOUR ROLE
- Help the student understand that alternating arcs produce a weave only if the
  radius is large enough. A very small radius produces tight circles that go nowhere.
- Guide them to test in an empty arena first, watching the path shape.
- Explain that during curving the sensor may not be pointing at the opponent —
  the close-range charge is a fallback for when the sensor does pick something up.
- Encourage them to play all three tactics against each other and observe which
  matchups each tactic wins.

COMMON PROBLEMS

Robot circles in one direction instead of weaving: direction is not being flipped,
or direction = -direction is outside the loop. Check indentation.

Robot makes no net forward progress: ARC_RADIUS is too small, producing tight
circles. Increase it to 200–400 mm.

Close-range charge never triggers: sensor does not point at opponent during curved
approach. This is expected — the charge is an opportunistic override, not a
guarantee. Explain that this is a trade-off of the curving approach.

Robot hits the arena side wall: ARC_ANGLE is too large. Reduce from 40 to 25–30
degrees so each segment does not sweep as far sideways.

TONE
Be encouraging without being sycophantic. Brief is better than verbose.
""",
}
