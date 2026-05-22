EXERCISE = {
    "id": "ch2_lab2_nowait_wait",
    "title": "Nowait and Wait",
    "concept": "background motor movement with nowait=True, wait(), and moving()",

    "objective": (
        "Add nowait=True to a move() call, observe that subsequent code runs while "
        "the motors are still moving, use wait() to synchronise before the next command, "
        "and use a while robot.moving() loop to flash a pixel during movement."
    ),

    "off_limits": [
        "the moving() function before the student has used wait() successfully",
        "the double-nowait override behaviour before the student has asked about it",
    ],

    "hints": [
        "nowait=True tells move() to queue the motion and return immediately. "
        "The motors start running, but your program moves on to the next line at once.",

        "robot.wait() blocks until _moving is False. Use it when you need to be "
        "certain the robot has stopped before issuing the next command.",

        "If you issue a second move() before the first has finished, the second "
        "move overrides the first. This can cause surprising behaviour — use wait() "
        "between moves unless you intend to override.",

        "robot.moving() returns True or False. You can test it in a while loop: "
        "while robot.moving(): — the loop body runs once per 10ms approximately.",
    ],

    "success_indicators": [
        "pixel changes colour while robot is still moving (confirms nowait works)",
        "wait() prevents second move from overriding first",
        "while robot.moving() loop flashes pixel during movement and stops when robot stops",
        "student can explain the difference between move(mm) and move(mm, nowait=True)",
    ],

    "observation_checklist": [
        "Does the pixel change colour before the robot has stopped?",
        "Without wait(), does the second move override the first?",
        "Does the flashing stop when the robot stops?",
    ],

    "tutor_brief": """
You are a teaching assistant for an embedded programming course using the Hull
Pixelbot robot and the CLB-robot MicroPython library.

This student is working on Lab 2: Nowait and Wait. The key learning is the
difference between blocking and non-blocking motor commands.

YOUR ROLE
- Help the student observe the difference concretely: pixel colour changing while
  the robot moves is the clearest demonstration that nowait=True worked.
- Explain that the stepper timer ISR handles stepping independently — the main
  program thread does not need to do anything to keep the motors moving.
- Guide them to use wait() before any command that must not run while the robot
  is still in motion.
- Introduce moving() only after wait() is understood.

COMMON PROBLEMS

Pixel does not change colour before robot stops: the student forgot nowait=True
or placed the colour change after wait().

Second move overrides first unexpectedly: the student issued two moves without
wait() between them. Use this as a teaching moment about the importance of wait().

while robot.moving() loop runs forever: the student forgot to issue a move()
before the while loop, or the move has already finished before the loop starts.
Ask them to check the order of their statements.

TONE
Be encouraging without being sycophantic. Brief is better than verbose.
""",
}
