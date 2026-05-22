# Lab 1: The Sumo Game

Robot Sumo is a two-robot competition where each robot tries to push as far into the opponent's territory as possible before time runs out.

---

## The Arena

The arena is a rectangle built from toy construction bricks. The bricks form a low wall around the perimeter that acts as a physical boundary.

A line across the middle marks each robot's **home half**. Each robot starts at its own end of the arena, touching the end wall, facing the opponent.

```
  ┌─────────────────────────────┐
  │  [Robot A]                  │
  │                             │
  │ - - - - centre line - - - - │
  │                             │
  │                  [Robot B]  │
  └─────────────────────────────┘
```

Both robots are switched on at the same time, run their programs independently, and never communicate with each other.

---

## Rules

1. **Starting position** — each robot is placed at its own end, facing the opponent.
2. **Start signal** — both robots are switched on at approximately the same time.
3. **Game duration** — the game runs for a fixed time (30 seconds is a good starting point).
4. **Scoring** — when time runs out, the robot that has advanced furthest into the opponent's half wins.
5. **Instant win** — if a robot reaches the far end wall (the opponent's starting position) before time expires, that robot wins immediately.
6. **Robots are autonomous** — no remote control; the program runs entirely on the Pico.

---

## The Distance Sensor

Each robot has an HC-SR04 distance sensor pointing forward. At the start of the game the two robots are facing each other across the full length of the arena, so the initial reading will be roughly the arena length minus the two robot lengths — typically 400–500 mm.

As the robots approach each other the reading falls. A robot can use this to decide when the opponent is close enough to dodge around or to know when a direct charge is about to make contact.

---

## Coding Approach

A sumo program has three phases:

1. **Countdown** — a short pause (3 seconds is typical) to give time for both robots to be switched on. Flash the pixels so you know the countdown is running.
2. **Game loop** — a `while` loop that runs for the game duration. Each iteration reads the sensor and decides what to do.
3. **End** — when the time limit expires, turn off the pixels and stop.

```python
import time
import robot

GAME_S = 30   # game duration in seconds

robot.init()

# Phase 1: countdown
for _ in range(3):
    robot.colour(robot.RED)
    time.sleep(0.5)
    robot.colour(robot.BLACK)
    time.sleep(0.5)

# Phase 2: game loop
start = time.time()
while time.time() - start < GAME_S:
    # --- your tactic goes here ---
    pass

# Phase 3: end
robot.colour(robot.BLACK)
```

The three tactics covered in the next labs all use this same skeleton — only the code inside the game loop changes.
