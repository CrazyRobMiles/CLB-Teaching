## Your task

Open `start.py`.

1. Move the robot forward **200 mm at full speed**.  Note roughly how long it takes.
2. Move the robot backward **200 mm over 5 seconds** — add `seconds=5` to the move.  Observe the difference in speed.
3. Make the robot turn **90 degrees over 3 seconds**.
4. Add `nowait=True` to the slow turn and use a pixel colour loop to show the robot moving slowly — flash between yellow and black every 0.2 seconds inside a `while robot.moving():` loop.

---

## Checking your work

- The full-speed move should complete in roughly 1–2 seconds.
- The 5-second move should take noticeably longer and move more smoothly.
- During the slow turn with `nowait=True`, the pixel should flash visibly while the robot turns.

---

## Going further

- Try `robot.move(200, seconds=2)` and `robot.move(200, seconds=20)`. What is the slowest speed at which the robot moves smoothly?
- Use `seconds=` on an arc to make the robot slowly trace a gentle curve.
