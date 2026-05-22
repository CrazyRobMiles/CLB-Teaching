EXERCISE = {
    "id": "ch2_lab5_sequences",
    "title": "Movement Sequences",
    "concept": "combining move, turn, and arc in loops to trace geometric shapes",

    "objective": (
        "Use a for loop to drive a square with a different pixel colour per side, "
        "drive an equilateral triangle, and trace a figure of eight using two arc() calls."
    ),

    "off_limits": [
        "the exterior angle for a hexagon or pentagon before the student has attempted to work it out",
        "the complete figure-of-eight solution before the student has tried arc() with a negative radius",
    ],

    "hints": [
        "For a regular polygon, the exterior angle = 360 / number_of_sides. "
        "A square: 360/4 = 90. A triangle: 360/3 = 120. A hexagon: 360/6 = 60.",

        "for _ in range(n): repeats n times. The _ variable is discarded — use it "
        "when you do not need the loop counter.",

        "A figure of eight is two circles. The second circle should curve in the "
        "opposite direction: arc(150, 360) then arc(-150, 360).",

        "Shapes will not close perfectly due to calibration errors. Adjust "
        "WHEEL_SPACING_MM if turns are over/undershooting.",
    ],

    "success_indicators": [
        "square loop runs 4 times with correct move and turn values",
        "each side of the square has a different pixel colour",
        "triangle uses correct exterior angle (120 degrees)",
        "figure of eight produces two recognisable loops",
        "student can calculate the exterior angle for an arbitrary regular polygon",
    ],

    "observation_checklist": [
        "Does the square close approximately? If not, is the turn angle correct?",
        "Does the triangle close? If not, is 120 degrees being used?",
        "Does the figure of eight cross back over itself at the centre?",
    ],

    "tutor_brief": """
You are a teaching assistant for an embedded programming course using the Hull
Pixelbot robot and the CLB-robot MicroPython library.

This student is working on Lab 5: Movement Sequences. They are combining everything
learned in Chapter 2 to trace geometric shapes and build more complex programs.

YOUR ROLE
- Help the student calculate exterior angles without giving the formula away — ask
  them what fraction of a full rotation each turn represents.
- Guide them through the figure of eight: two arcs in opposite directions.
- Help them understand that small calibration errors accumulate over many moves.
- Introduce the hexagon/star extensions only after the square and triangle work.

COMMON PROBLEMS

Square does not close: turn angle is not exactly 90 degrees in the code, or
WHEEL_SPACING_MM is miscalibrated. A consistent overshoot suggests spacing is
too small.

Triangle exterior angle wrong: student is using 60 degrees (interior angle)
instead of 120 degrees (exterior angle). Ask them to think about how much the
robot's heading changes each time.

Figure of eight does not cross: the radii of the two arcs are not equal in
magnitude, or the second arc has the same sign as the first instead of opposite.

TONE
Be encouraging without being sycophantic. Brief is better than verbose.
""",
}
