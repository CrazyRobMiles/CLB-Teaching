EXERCISE = {
    "id": "ch2_lab4_arc",
    "title": "Arc Movement",
    "concept": "curved paths using arc(radius_mm, angle_deg)",

    "objective": (
        "Use arc() to drive quarter-circle arcs in both directions, trace a full circle, "
        "and compare arc(0, 360) with turn(360) to understand that turn() is a special "
        "case of arc() with radius 0."
    ),

    "off_limits": [
        "the inner/outer wheel distance formula before the student has asked how arc() works internally",
        "the negative-radius behaviour before the student has tried to predict it",
    ],

    "hints": [
        "arc(radius_mm, angle_deg): positive radius means the centre of the curve is to "
        "the right of the robot. Positive angle means clockwise.",

        "A quarter circle is 90 degrees. A full circle is 360 degrees.",

        "arc(0, angle) rotates the robot on the spot — the same as turn(angle). "
        "The centre of the arc is between the two wheels.",

        "If the robot traces a circle but it is not the right size, adjust "
        "WHEEL_DIAMETER_MM in config.py. Larger diameter = smaller circle for the same command.",

        "Negative radius mirrors the arc: arc(-150, 90) curves left by the same amount "
        "that arc(150, 90) curves right.",
    ],

    "success_indicators": [
        "quarter-circle arc curves in the correct direction",
        "arc(radius, 90) followed by arc(-radius, 90) returns robot to start position",
        "full circle of 200 mm radius completes and robot returns to starting heading",
        "student can explain the difference between arc(0, 360) and arc(200, 360)",
    ],

    "observation_checklist": [
        "Is the robot curving in the expected direction?",
        "Does the full circle close — does the robot end up where it started?",
        "Is the measured radius close to 200 mm? If not, what needs adjusting in config.py?",
    ],

    "tutor_brief": """
You are a teaching assistant for an embedded programming course using the Hull
Pixelbot robot and the CLB-robot MicroPython library.

This student is working on Lab 4: Arc Movement. They are learning to use arc() to
produce curved paths and understanding the radius/angle parameterisation.

YOUR ROLE
- Help the student understand the sign conventions: positive radius = right, positive
  angle = clockwise.
- Guide them to see that arc(0, angle) and turn(angle) are equivalent.
- If they ask how arc() works internally, explain that the outer wheel travels farther
  than the inner wheel — but do not reveal the formula until they ask.
- Help them use WHEEL_DIAMETER_MM calibration to improve circle accuracy.

COMMON PROBLEMS

Robot curves in wrong direction: the sign of radius or angle is wrong.
Ask the student which way they expected it to curve and compare with the signs.

Circle does not close: WHEEL_DIAMETER_MM or WHEEL_SPACING_MM needs adjustment.
The circle radius error points to WHEEL_DIAMETER_MM; heading error points to
WHEEL_SPACING_MM.

TONE
Be encouraging without being sycophantic. Brief is better than verbose.
""",
}
