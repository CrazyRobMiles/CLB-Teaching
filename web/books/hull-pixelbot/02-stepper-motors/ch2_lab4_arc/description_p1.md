# Lab 4: Arc Movement

`move()` and `turn()` are special cases of a more general motion: the **arc**. An arc moves the robot along a circular path by running the two wheels at different speeds.

---

## The arc() function

```python
robot.arc(radius_mm, angle_deg)
```

| Parameter | Meaning |
|-----------|---------|
| `radius_mm` | Radius of the arc in mm. Positive = centre to the right. 0 = rotate on the spot. |
| `angle_deg` | Angular distance to travel. Positive = clockwise. |

The centre point of the arc is on a line drawn sideways through the robot, at a distance of `radius_mm` from the midpoint between the wheels.

---

## Examples

```python
robot.arc(200, 90)    # quarter-circle arc, 200 mm radius, turning right
robot.arc(-200, 90)   # quarter-circle arc, 200 mm radius, turning left
robot.arc(0, 180)     # rotate 180° on the spot (same as turn(180))
robot.arc(200, 360)   # complete circle of 200 mm radius
```

The library calculates the distance each wheel must travel:

```
inner wheel distance = 2π × (radius − spacing/2) × angle/360
outer wheel distance = 2π × (radius + spacing/2) × angle/360
```

The outer wheel travels farther, so it steps faster. Both wheels start and stop at the same time.

---

## Special cases

- `arc(0, angle)` is equivalent to `turn(angle)` — both wheels travel equal distances in opposite directions.
- A very large radius produces nearly straight-line motion.
- A negative radius mirrors the arc to the other side.
