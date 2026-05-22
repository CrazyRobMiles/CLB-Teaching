EXERCISE = {
    "id": "ch1_lab3_pixel_patterns",
    "title": "Pixel Patterns",
    "concept": "individual pixel addressing and chasing animations",

    "objective": (
        "Use robot._pixels.set(index, rgb) to control individual pixels, build "
        "a chasing effect that travels from index 0 to 7 and back using range(), "
        "and wrap the whole thing in while True for continuous animation."
    ),

    "off_limits": [
        "the comet trail effect before the student has the basic bounce working",
        "the range(7, -1, -1) syntax before the student has tried to work it out",
    ],

    "hints": [
        "robot.colour(robot.BLACK) clears all pixels. Call it at the start of each "
        "loop iteration before lighting the next pixel — otherwise old pixels stay lit.",

        "robot._pixels.set(i, rgb) sets pixel number i to a colour tuple. "
        "Pass a colour constant: robot._pixels.set(i, robot.GREEN). "
        "Or pass a tuple directly: robot._pixels.set(i, (0, 255, 0)).",

        "range(8) counts 0, 1, 2, 3, 4, 5, 6, 7. "
        "range(7, -1, -1) counts 7, 6, 5, 4, 3, 2, 1, 0. "
        "The three arguments are start, stop (exclusive), step.",

        "To make the animation smooth, keep time.sleep() short — 0.05 to 0.1 seconds "
        "works well for an 8-pixel strip.",
    ],

    "success_indicators": [
        "single pixel chases from index 0 to 7",
        "pixel bounces back from 7 to 0 using range(7, -1, -1)",
        "animation repeats continuously with while True",
        "student can explain what the three arguments to range() do",
    ],

    "observation_checklist": [
        "Does robot.colour(robot.BLACK) appear at the start of each loop iteration?",
        "Are you passing the loop variable i to robot._pixels.set()?",
        "Is the return loop using range(7, -1, -1) or a similar countdown?",
        "Is time.sleep() small enough to see smooth motion?",
    ],

    "tutor_brief": """
You are a teaching assistant for an embedded programming course using the Hull
Pixelbot robot and the CLB-robot MicroPython library.

This student is working on Lab 3: Pixel Patterns. They are learning to address
individual pixels and build a bouncing chase animation using nested loops.

YOUR ROLE
- Help the student understand that clearing the strip with robot.colour(robot.BLACK)
  before lighting the next pixel is what creates the illusion of motion.
- Guide them to range(7, -1, -1) for the return journey — let them try to
  work out the arguments before revealing the answer.
- Introduce the comet trail idea only after the basic bounce is working.

COMMON PROBLEMS

All pixels stay lit: the student forgot robot.colour(robot.BLACK) at the start of
each iteration. The pixel is being set but previous ones are never cleared.

Pixel jumps to index 0 instead of bouncing back: the return range is missing
or counts in the wrong direction.

Nothing moves: time.sleep() is too large (e.g. 1.0 instead of 0.1), making
each step take a full second. Ask the student how long their sleep is.

TONE
Be encouraging without being sycophantic. Brief is better than verbose.
""",
}
