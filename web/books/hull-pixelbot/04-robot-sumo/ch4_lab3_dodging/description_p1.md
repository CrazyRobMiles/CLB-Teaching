# Lab 3: Dodging

The **dodging** tactic uses the distance sensor to detect the opponent and swerve sideways before making contact. The goal is to slip past the charging opponent, reach the opponent's end, and win outright.

---

## The Core Idea

Instead of pushing through the opponent, a dodging robot steers around them:

1. Advance toward the opponent.
2. When the opponent is within a set distance, turn to one side.
3. Move past the opponent's position.
4. Turn back to the original heading and resume advancing.

```
  Robot A (dodger) →   →  ↓
                          ↓  ← opponent
                          ↓
                         →→ (continues past)
```

---

## The Program Structure

```python
import time
import robot

GAME_S       = 30    # game duration in seconds
DODGE_MM     = 250   # dodge when opponent is closer than this
DODGE_ANGLE  = 40    # degrees to turn sideways
DODGE_STEP   = 150   # mm to travel while turned

robot.init()

# Countdown
for _ in range(3):
    robot.colour(robot.YELLOW)
    time.sleep(0.5)
    robot.colour(robot.BLACK)
    time.sleep(0.5)

start = time.time()
robot.colour(robot.GREEN)

while time.time() - start < GAME_S:
    mm = robot.distance()

    if mm > 0 and mm < DODGE_MM:
        # Opponent detected — dodge left
        robot.colour(robot.YELLOW)
        robot.turn(-DODGE_ANGLE)     # turn left
        robot.move(DODGE_STEP)       # travel sideways
        robot.turn(DODGE_ANGLE)      # straighten up
        robot.colour(robot.GREEN)
    else:
        robot.move(50)               # advance

robot.colour(robot.BLACK)
```

The pixel turns yellow during a dodge and green during normal advance. This lets you see exactly when the sensor triggers.

---

## Choosing the Dodge Threshold

`DODGE_MM` controls how early the dodge triggers:

- **Too large** (e.g. 400 mm) — the robot dodges before it has made any progress into the opponent's half.
- **Too small** (e.g. 80 mm) — the robot is nearly touching the opponent before it reacts; there may not be enough room to swerve.
- **Good starting point**: 200–300 mm gives room to manoeuvre while still advancing well into the opponent's half first.

---

## Dodge Direction

The example always dodges left. A more advanced version randomises the direction:

```python
import random
direction = 1 if robot.random_val() > 6 else -1
robot.turn(DODGE_ANGLE * direction)
robot.move(DODGE_STEP)
robot.turn(-DODGE_ANGLE * direction)
```

A random dodge is harder for the opponent to predict and counter.

---

## The -1 Reading

`robot.distance()` returns -1 when no echo is received (the opponent is out of range or the sensor misfired). Always check `mm > 0` before comparing to a threshold — treating -1 as "obstacle at 0 mm" would cause the robot to dodge immediately on startup.
