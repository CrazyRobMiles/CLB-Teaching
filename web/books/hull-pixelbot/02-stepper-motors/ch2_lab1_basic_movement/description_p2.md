## Your task

Open `start.py`. It calls `robot.init()` and includes some movement commands for you to complete.

1. Make the robot move **forward 300 mm**.  Set the pixel **green** before the move and **black** after it.
2. Make the robot move **backward 300 mm** to return to its starting position.  Use a different pixel colour to mark this move.
3. Make the robot turn **90 degrees clockwise**.
4. Make the robot turn **90 degrees anti-clockwise** to return to its original heading.

---

## Checking your work

Observe how the pixel colour changes as the robot moves:
- The colour you set *before* a `move()` call should stay lit for the full duration of the move.
- The colour you set *after* should appear only when the move has finished.

This is how you can tell that `move()` blocks until the robot stops.

---

## Going further

- Try `robot.move(-50)` — does the robot move backward as expected?
- What happens if you call `robot.turn(360)`? Does the robot return to its starting heading?
- Adjust `WHEEL_SPACING_MM` in `config.py` if the turn overshoots or undershoots. Increasing the value makes the robot turn less for the same angle command.
