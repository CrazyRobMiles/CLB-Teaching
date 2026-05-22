## Your task

Open `start.py`.

1. Drive the robot in a **quarter-circle arc** of 150 mm radius, turning right.
2. Drive a second **quarter-circle arc** of 150 mm radius, turning left, to undo the first.
3. Drive a **full circle** of 200 mm radius.  The robot should return close to its starting position.
4. Try `arc(0, 360)` — what does this do?  How does it compare to `turn(360)`?

---

## Checking your work

- After steps 1 and 2 the robot should be back where it started (approximately).
- After step 3 the robot should have traced a circle and be facing the same direction it started.

Measure the radius of the circle the robot traces.  Compare it with the 200 mm you specified.  If it is consistently different, adjust `WHEEL_DIAMETER_MM` in `config.py`.

---

## Going further

- What arc radius produces a path that looks like a straight line to the eye?
- Try combining arcs with different signs: `arc(150, 90)` then `arc(-150, 90)`.  What shape does the robot trace?
- Add `seconds=` to make arcs slow enough to observe clearly.
