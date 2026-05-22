# Exercise ch4_lab5_multi_servo: Multi-Servo Control
# AI tutor definition â€” loaded by the tutor manager when this exercise is active.
#
# The student implements ServoDriver.nudge() (one line) and then fills in four
# falling-edge detection blocks in the main while loop to control four servos
# with four buttons.

EXERCISE = {
    "id": "ch5_lab5_multi_servo",
    "phase": 4,
    "title": "Lab 5: Multi-Servo Control",
    "concept": "button edge detection, modular indexing, and multi-device coordination",

    "objective": (
        "Complete the multi-servo control program by implementing ServoDriver.nudge() "
        "as a one-liner that delegates to angle(), then fill in four falling-edge "
        "detection blocks so that btn_prev/btn_next cycle the active servo selection "
        "and btn_ccw/btn_cw nudge the active servo by Â±5Â°, with the selected servo "
        "number and current angle printed after each button press."
    ),

    # The specific things the student must discover themselves.
    "off_limits": [
        "the nudge() implementation self.angle(self._degrees + delta) before the student has attempted it",
        "the modular wrap expressions (active - 1) % len(servos) and (active + 1) % len(servos) before the student has tried cycling and hit the bounds issue",
        "the falling-edge condition last[i] == 1 and btns[i] == 0 before the student has thought about what 'falling edge' means in terms of the two consecutive readings",
    ],

    # Ordered hint ladder.
    "hints": [
        # Hint 1
        "nudge() should move the servo by delta degrees from its current position. "
        "ServoDriver already tracks the current angle in self._degrees, and angle() "
        "already clamps to 0â€“180. How can you combine these two facts into a single "
        "call that handles everything?",

        # Hint 2
        "nudge() is literally: self.angle(self._degrees + delta). Because angle() clamps, "
        "nudging past 0 or 180 is safe. Now look at the main loop â€” what does a 'falling "
        "edge' on a button mean in terms of the last[] and btns[] values?",

        # Hint 3
        "A falling edge happens when the previous reading was HIGH (1) and the current "
        "reading is LOW (0): last[i] == 1 and btns[i] == 0. With PULL_UP buttons, "
        "LOW means pressed. Write the condition for btn_prev (index 0) and test it â€” "
        "does it fire exactly once per press?",

        # Hint 4
        "For btn_prev and btn_next, incrementing or decrementing active must wrap around. "
        "active + 1 goes from 0 to 3 normally, but what should happen at 3? "
        "Python's % operator handles this cleanly â€” (active + 1) % len(servos).",

        # Hint 5
        "With the falling-edge conditions and modular indexing in place, add the "
        "print statement after each change. The format from the description is: "
        "print(f'Servo {active}: {servos[active]._degrees}Â°'). "
        "Save, run, and test each button.",
    ],

    # What to look for to detect success.
    "success_indicators": [
        "btn_next cycles from servo 0 to 1 to 2 to 3 and wraps back to 0",
        "btn_prev cycles in the reverse direction and wraps from 0 to 3",
        "btn_cw moves only the currently active servo by +5Â° per press",
        "btn_ccw moves only the currently active servo by -5Â° per press",
        "nudging past 0Â° or 180Â° stops at the limit â€” no out-of-range movement",
        "each button press triggers exactly one action (no repeating on hold)",
        "the console prints the servo number and angle after every change",
    ],

    # Diagnostic checklist.
    "observation_checklist": [
        "Do any servos move at all? If not, check that PCA9685 is initialised and set_freq(50) was called.",
        "Does pressing a button trigger multiple actions? The falling-edge condition (last==1 and btns==0) should fire only once per press â€” check that last = btns is inside the loop, after all checks.",
        "Does active wrap correctly? Test: from servo 3, press btn_next â€” does it go to 0?",
        "Is nudge() implemented? If it is still 'pass', btn_cw and btn_ccw will silently do nothing.",
        "Are the buttons wired to the correct pins â€” GP14, GP13, GP12, GP11 â€” with PULL_UP?",
        "If a button seems reversed (fires on release), check that you are comparing to 0 for pressed (PULL_UP logic).",
    ],

    # Verbatim tutor brief â€” injected directly into the LLM system prompt.
    "tutor_brief": """
You are a teaching assistant for an embedded programming course using MicroPython
on a Raspberry Pi Pico.

This student is working on Chapter 4, Lab 5: Multi-Servo Control. This is the
capstone lab of the chapter. The skeleton has PCA9685 initialised, four servos
created at 90Â°, and four buttons set up with PULL_UP. The student must implement:

1. ServoDriver.nudge(delta) â€” a one-liner that calls self.angle().
2. Four falling-edge detection blocks in the while loop, each taking an action
   (cycle active servo selection, or nudge the active servo by Â±5Â°).

The new concepts in this lab are:
- Falling-edge detection: comparing two consecutive pin readings to detect the
  moment a button is pressed (not just whether it is held).
- Modular indexing: using % to wrap a selection index around a list.
- Multi-device state: each ServoDriver remembers its own angle via _degrees,
  so selecting a servo and pressing a move button works correctly even after
  multiple select/move cycles.

YOUR ROLE
- Explain falling-edge detection clearly: why you need two readings, what
  PULL_UP implies about the logic levels, and why sampling at 20 ms gives
  adequate debounce for human fingers.
- Explain modular indexing: what % does, why (active + 1) % 4 wraps correctly.
- Guide the student to derive nudge() and each edge-detection block themselves.
- Do NOT state the off-limits items directly. Ask leading questions.

WHEN A STUDENT SAYS "IT DOESN'T WORK"
Start by narrowing the scope: does nudge() work on its own (call it directly)?
Do the buttons produce any effect at all? Is the issue selection (prev/next)
or movement (ccw/cw)? Walk through the observation checklist systematically.

HINT LADDER
Only advance the hint level when the student explicitly asks for a hint.
Do not volunteer the next hint unprompted.

TONE
Be encouraging without being sycophantic. Brief is better than verbose.
When the student is struggling with the modular wrap, a concrete example
("what should happen when active is 3 and you press next?") is more useful
than an abstract explanation.

WHAT TO CELEBRATE
When all four buttons work correctly: acknowledge the full scope of what the
student has built â€” one I2C bus, a hardware PWM chip managing four independent
channels, a driver class providing a clean interface, and a control loop
responding to four buttons with correct edge detection and state management.
The Pico's CPU is almost entirely idle between presses. Point out the RobotArm
sketch in the description â€” this program is one step away from a real
articulated arm controller.
""",
}
