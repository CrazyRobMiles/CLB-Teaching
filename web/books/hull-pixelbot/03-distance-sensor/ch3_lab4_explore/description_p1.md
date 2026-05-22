# Lab 4: Explore

In this lab there is no single correct answer. You have a complete toolkit:

| Function | What it does |
|----------|-------------|
| `robot.colour(robot.RED)` … `robot.colour(robot.BLACK)` | Set all pixels to a named colour |
| `robot.colour((r, g, b))` | Set pixels to any RGB colour |
| `robot._pixels.set(i, (r, g, b))` | Set a single pixel by index |
| `robot.move(mm)` | Move forward or backward |
| `robot.turn(degrees)` | Turn on the spot |
| `robot.arc(radius, angle)` | Curve |
| `robot.move(mm, nowait=True)` | Start a move and continue |
| `robot.wait()` | Wait for motors to stop |
| `robot.moving()` | Check if motors are running |
| `robot.distance()` | Read the distance sensor in mm |
| `robot.random_val()` | Random integer 1–12 |
| `time.sleep(seconds)` | Pause |

Your goal is to design and program a behaviour of your own choosing.

---

## Ideas to get you started

**Patrol** — the robot drives back and forth between two walls, using the distance sensor to detect each wall and reverse direction.

**Stalker** — the robot tries to maintain a fixed distance from an object in front of it: if the object gets closer, the robot backs away; if the object moves further away, the robot follows.

**Mood indicator** — use `robot.moving()` and `robot.distance()` to display different pixel colours based on what the robot is currently doing (moving, stopped, obstacle detected, clear path).

**Geometric explorer** — combine random turn angles from `random_val()` with obstacle avoidance to produce unpredictable exploration paths.

---

## What makes a good behaviour?

A good robot behaviour is:

- **Observable** — you can tell what the robot is "thinking" by watching it.
- **Robust** — it handles edge cases (no echo, very close obstacles, walls).
- **Interesting** — it does something that would be hard to predict in advance.
