# Lab 3: Obstacle Avoidance

You now have all the pieces needed to make the robot react autonomously to its environment: `distance()` to sense what is ahead, `move()` to drive forward, `turn()` to change direction, and the pixel to show the robot's state.

---

## The avoidance loop

A simple obstacle-avoidance behaviour works like this:

1. Read the distance sensor.
2. If something is close, back up and turn.
3. Otherwise, move forward a small amount.
4. Repeat.

In code:

```python
robot.colour(robot.GREEN)
while True:
    mm = robot.distance()
    if mm > 0 and mm < 200:
        # obstacle detected
        robot.colour(robot.RED)
        robot.move(-100)      # back up 100 mm
        robot.turn(90)        # turn right
        robot.colour(robot.GREEN)
    else:
        # path clear — inch forward
        robot.move(50)
```

The `mm > 0` check filters out -1 (no echo) readings — a -1 should not be treated as "obstacle at 0 mm".

---

## Blocking moves inside the avoidance loop

Notice that `move()` and `turn()` in the avoidance routine are **blocking** — the robot backs up completely and turns completely before reading the sensor again. This keeps the behaviour simple and predictable. The sensor is only checked between moves, not during them.

This is a deliberate design choice for a first avoidance program. Later (in the Connected Little Boxes book) you will learn how to read the sensor *while* the robot is moving.

---

## Tuning the behaviour

- **Avoidance threshold** — the distance at which the robot detects an obstacle. Start with 200 mm and adjust based on your robot's speed and the environment.
- **Backup distance** — how far the robot reverses before turning. Too small and it may still be facing the obstacle after turning; too large and it wastes time.
- **Turn angle** — 90 degrees gives a reliable direction change; smaller angles may not clear the obstacle.
