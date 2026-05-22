# Lab 4: Curving

The **curving** tactic moves the robot in arcs rather than straight lines. Instead of going directly at the opponent, a curving robot sweeps diagonally across the arena, approaching from the side where the distance sensor is less likely to see it coming.

---

## Why Curves?

A robot moving in a straight line is easy to track with a forward-facing sensor. If your opponent is always looking ahead, a robot that approaches from the side only enters their sensor's view at the last moment — giving less time to react.

A curving path also covers more of the arena's width, which can be useful if the opponent is not in the centre.

---

## Arc Reminder

`robot.arc(radius_mm, angle_deg)` moves the robot along a circular arc:

| Value | Effect |
|-------|--------|
| Positive radius | Arc curves right |
| Negative radius | Arc curves left |
| Large radius | Gentle curve, nearly straight |
| Small radius | Tight curve |

A sequence of alternating arcs produces a weaving path across the arena:

```
start →  ↗  →  ↘  →  ↗  → end
```

---

## The Program Structure

```python
import time
import robot

GAME_S      = 30    # game duration in seconds
ARC_RADIUS  = 300   # mm — large = gentle curve
ARC_ANGLE   = 40    # degrees per arc segment

robot.init()

# Countdown
for _ in range(3):
    robot.colour(robot.BLUE)
    time.sleep(0.5)
    robot.colour(robot.BLACK)
    time.sleep(0.5)

start = time.time()
robot.colour(robot.BLUE)

direction = 1   # start curving right

while time.time() - start < GAME_S:
    mm = robot.distance()

    if mm > 0 and mm < 150:
        # Very close — straighten up and push through
        robot.colour(robot.RED)
        robot.move(100)
        robot.colour(robot.BLUE)
    else:
        # Curve across the arena
        robot.arc(ARC_RADIUS * direction, ARC_ANGLE)
        direction = -direction   # alternate left and right

robot.colour(robot.BLACK)
```

Each iteration drives one arc segment, then flips the direction so the robot weaves left-right as it advances. The net forward progress per weave depends on `ARC_RADIUS` and `ARC_ANGLE`.

---

## Tuning the Weave

| Parameter | Too small | Too large |
|-----------|-----------|-----------|
| `ARC_RADIUS` | Tight zigzag — covers width but moves slowly forward | Near-straight — similar to charging |
| `ARC_ANGLE` | Fine weave, many segments | Wide sweep, may reach arena wall |

A radius of 200–400 mm and an angle of 30–50 degrees per segment gives a balanced weave for a 400 mm wide arena.

---

## Combining With Dodging

A curving robot can also check the sensor and switch to a straight charge when the opponent is detected directly ahead — curving to approach unseen, then charging through on contact:

```python
if mm > 0 and mm < 200:
    robot.colour(robot.RED)
    robot.move(200)          # charge through
    robot.colour(robot.BLUE)
else:
    robot.arc(ARC_RADIUS * direction, ARC_ANGLE)
    direction = -direction
```
