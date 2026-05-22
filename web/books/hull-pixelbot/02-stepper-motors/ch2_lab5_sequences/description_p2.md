## Your task

Open `start.py`.

**Part A — Square:**

Complete the square-driving loop.  Add pixel colours so each of the four sides has a different colour.

**Part B — Triangle:**

Add a second loop that drives an equilateral triangle with 200 mm sides.

**Part C — Figure of eight:**

A figure of eight is two circles driven in opposite directions back-to-back:

```python
robot.arc(150, 360)    # first circle clockwise
robot.arc(-150, 360)   # second circle anti-clockwise
```

Add this to your program and observe the path the robot traces.

---

## Checking your work

- The square should return the robot close to its starting position and heading.
- The triangle should also close — the robot should end up where it started.
- The figure of eight should produce two recognisable loops.

Small errors accumulate over many moves.  If shapes do not close correctly, fine-tune `WHEEL_DIAMETER_MM` and `WHEEL_SPACING_MM` in `config.py`.

---

## Going further

- Can you drive a regular hexagon?  What exterior angle does a hexagon need?
- Try a star pattern: five moves with `turn(144)` between each.
- Add `seconds=` to slow all moves down to make the shapes easier to observe.
