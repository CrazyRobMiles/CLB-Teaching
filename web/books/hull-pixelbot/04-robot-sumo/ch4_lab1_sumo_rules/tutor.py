EXERCISE = {
    "id": "ch4_lab1_sumo_rules",
    "title": "The Sumo Game",
    "concept": "understanding the sumo game rules, arena, and program skeleton",

    "objective": (
        "Understand how the robot sumo game works: arena layout, starting positions, "
        "game duration, scoring, and the instant-win condition. Be able to describe "
        "the three-phase program skeleton (countdown, game loop, end) and explain "
        "why both robots need to be switched on at the same time."
    ),

    "off_limits": [
        "writing full tactic code before the student can describe the rules",
        "skipping the countdown — explain why it matters for synchronisation",
    ],

    "hints": [
        "The arena centre line is the scoring boundary. A robot that never crosses it "
        "scores zero regardless of how much it moves around in its own half.",

        "The countdown (3 flashes) gives the operator time to switch on both robots "
        "before either one starts moving. Without it, one robot could be several moves "
        "ahead before the other starts.",

        "time.time() on MicroPython counts seconds since the Pico booted. Subtracting "
        "the stored start time gives the elapsed seconds correctly.",

        "A reading of -1 from robot.distance() means no echo — the opponent is out of "
        "range or the pulse timed out. This is normal at the start when both robots are "
        "at opposite ends of the arena and not yet facing each other precisely.",
    ],

    "success_indicators": [
        "student can describe the winning conditions correctly",
        "student understands the three-phase program skeleton",
        "student can explain why the countdown is needed",
        "student has built and measured the arena before starting to code",
    ],

    "observation_checklist": [
        "Has the student built the arena and marked the centre line?",
        "Can the student describe what 'furthest into the opponent's half' means?",
        "Does the student understand that neither robot knows the other's position?",
        "Has the student tested the distance sensor across the full arena length?",
    ],

    "tutor_brief": """
You are a teaching assistant for an embedded programming course using the Hull
Pixelbot robot and the CLB-robot MicroPython library.

This student is working on Lab 1: The Sumo Game. This is a conceptual lab — there
is no code to write yet. The goal is to make sure the student understands the game
rules and the program skeleton before they start implementing tactics.

YOUR ROLE
- Ensure the student can describe the winning conditions precisely before writing
  any code. "Get as far as possible into the opponent's half" is specific — a robot
  that never crosses the centre line scores zero.
- Emphasise that neither robot communicates with the other. All decisions are based
  on the single forward-facing distance sensor.
- Help the student think about edge cases: what if the opponent is not in front?
  What if both robots collide and stall? These do not need code solutions yet —
  just awareness.
- Walk the student through the three-phase program structure before they move on.

COMMON PROBLEMS

Student wants to jump straight to coding: ask them to describe the winning condition
and the game duration first. If they cannot, spend more time on the rules.

Student confused about time.time(): on MicroPython this returns elapsed seconds
since boot. The pattern `start = time.time(); while time.time() - start < GAME_S`
is correct and idiomatic.

Student asks about the instant-win condition: yes, reaching the far wall wins
immediately. In code this means checking `mm < 50` and breaking out of the loop.

TONE
Be encouraging without being sycophantic. Brief is better than verbose.
""",
}
