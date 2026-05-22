EXERCISE = {
    "id": "ch3_lab4_explore",
    "title": "Explore",
    "concept": "open-ended behaviour design combining all robot library functions",

    "objective": (
        "Design and implement an original robot behaviour using any combination of "
        "move(), turn(), arc(), distance(), pixel functions, time.sleep(), random_val(), "
        "nowait=True, and wait(). Describe the intended behaviour in a comment before "
        "writing any code."
    ),

    "off_limits": [],

    "hints": [
        "Start by writing a comment describing what you want the robot to do. "
        "A clear description makes the code much easier to write.",

        "Think in states: what are the distinct situations the robot can be in, "
        "and what should it do in each?  Use pixel colours to show which state is active.",

        "Always handle the -1 case from distance(). Decide what the robot should do "
        "when it cannot get a reading.",

        "Use robot.random_val() (returns 1–12) to add unpredictability. "
        "Multiply by a step size: robot.random_val() * 20 gives 20–240 mm.",

        "If the robot gets into trouble (stuck, driving in circles), add print() "
        "statements to log what it is doing — console output is your debugging tool.",

        "The CLB framework solves the problem of reading the sensor while moving. "
        "If you find yourself wanting that capability, make a note — that is exactly "
        "what the next book covers.",
    ],

    "success_indicators": [
        "program has a comment describing the intended behaviour",
        "pixel colours reflect robot state throughout",
        "-1 readings are handled explicitly",
        "behaviour is demonstrably different from the Lab 3 avoidance loop",
        "student can explain a design decision they made and why",
    ],

    "observation_checklist": [
        "Is there a description comment at the top of the program?",
        "Does the pixel show what state the robot is in?",
        "Does the robot handle -1 readings without crashing or behaving unexpectedly?",
        "Is there any state the robot could get permanently stuck in?",
    ],

    "tutor_brief": """
You are a teaching assistant for an embedded programming course using the Hull
Pixelbot robot and the CLB-robot MicroPython library.

This student is working on Lab 4: Explore. This is an open-ended design lab —
there is no single correct answer. The student has the full robot API available
and should produce an original behaviour.

YOUR ROLE
- Encourage the student to describe their intended behaviour in words before
  writing code. A clear mental model makes implementation much easier.
- Help them think in terms of states and transitions.
- Guide them to make the pixel show the current state — this is both good design
  and a useful diagnostic.
- If they ask about reading the sensor while moving, acknowledge that this is a
  real limitation of the sequential library and mention that the CLB framework
  (next book) addresses it with managers and events.
- Do not impose a specific behaviour — support whatever the student chooses.

GOOD BEHAVIOURS TO SUGGEST (if the student is stuck)

Patrol: drive back and forth between two walls using distance readings to detect
each wall and reverse.

Stalker: maintain a fixed distance from a moving object in front of the sensor.

Random explorer: combine obstacle avoidance with random turn angles.

Mood indicator: the robot sits still but changes colour based on how close the
nearest object is, reacting to people approaching and retreating.

TONE
Be encouraging without being sycophantic. Celebrate creative choices.
Questions about what they want the robot to do are more valuable than
prescriptive advice about how to write the code.
""",
}
