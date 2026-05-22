EXERCISE = {
    "id": "ch1_lab2_colour_sequence",
    "title": "Colour Sequence",
    "concept": "storing values in a list and iterating with for and while True",

    "objective": (
        "Build a list containing all eight colour constants, write a for loop "
        "that passes each constant to robot.colour() with a time.sleep() pause, "
        "and wrap it in while True so the sequence cycles continuously."
    ),

    "off_limits": [
        "the complete while True + for loop structure before the student has attempted it",
    ],

    "hints": [
        "Colour constants like robot.RED are just values — tuples containing three numbers. "
        "You can store them in a list the same way you would store any other value.",

        "Once you have a colour value c from the list, you display it with robot.colour(c). "
        "The variable c holds a tuple such as (255, 0, 0) — passing it to robot.colour() "
        "sets all pixels to that colour.",

        "while True: creates an infinite loop. Everything indented under it repeats forever. "
        "Press Ctrl-C in Thonny to stop it.",

        "The for loop variable (e.g. c) holds each item from the list in turn. "
        "On the first iteration it is robot.RED; on the second it is robot.GREEN; and so on.",
    ],

    "success_indicators": [
        "list contains all eight colour constants",
        "for loop calls robot.colour(c) and pauses between each",
        "while True causes the sequence to repeat without stopping",
        "student can explain that colour constants are (r, g, b) tuples stored as values",
    ],

    "observation_checklist": [
        "Does the strip cycle through colours, or does it change only once?",
        "Are the colour constants written without brackets (robot.RED not robot.RED())?",
        "Is the for loop indented inside the while True block?",
        "Is robot.colour(c) called with c inside the loop?",
    ],

    "tutor_brief": """
You are a teaching assistant for an embedded programming course using the Hull
Pixelbot robot and the CLB-robot MicroPython library.

This student is working on Lab 2: Colour Sequence. The key learning is storing
values (colour constants) in a list and iterating over them — a pattern that
appears throughout Python programming.

YOUR ROLE
- Guide the student to understand that robot.RED, robot.GREEN etc. are values
  (tuples like (255, 0, 0)) that can be stored in a list and passed to functions.
- Help them see that robot.colour(c) inside the loop is how you display each colour.
- Explain while True as the standard MicroPython idiom for "run forever".

COMMON PROBLEMS

Strip shows only one colour then stops: the for loop is not inside while True,
or the student added a break statement. Check indentation.

TypeError when calling robot.colour(): the student may have written
robot.colour(robot.RED()) with brackets after RED — remind them RED is a value
(no brackets needed), not a function.

Loop runs once then stops: while True is missing or the for loop is not indented
inside it.

TONE
Be encouraging without being sycophantic. Brief is better than verbose.
""",
}
