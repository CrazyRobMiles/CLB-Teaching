## Your task

Open `start.py`.

**Part A — Observe blocking behaviour:**

Run the provided code as-is and watch when the pixel colours change. Notice that each colour appears only when the preceding move has finished.

**Part B — Add nowait:**

1. Change the first `move()` call to use `nowait=True`.
2. Add a line *after* the move that sets the pixel to a different colour.
3. Add `robot.wait()` before the next move to prevent it from overriding the first.
4. Run the program and observe the difference: the pixel should change colour while the robot is still moving.

**Part C — Use moving():**

5. Replace the `wait()` call with a `while robot.moving():` loop that flashes the pixel between two colours (use `time.sleep(0.1)` inside the loop).

---

## Checking your work

In Part B: you should see the pixel change colour before the robot has stopped moving. This confirms that code after `nowait=True` runs immediately.

In Part C: the pixel should flash while the robot moves and stop flashing when the robot stops.

---

## Going further

What happens if you issue two `nowait=True` moves one after the other without a `wait()` between them? Try it and observe the result.
