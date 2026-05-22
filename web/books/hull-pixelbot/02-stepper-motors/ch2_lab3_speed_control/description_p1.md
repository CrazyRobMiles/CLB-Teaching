# Lab 3: Speed Control

By default the robot moves at maximum speed — one half-step every 1200 microseconds. You can slow a move down by telling the library how many seconds the move should take.

---

## The seconds= parameter

```python
robot.move(300, seconds=10)    # travel 300 mm over 10 seconds
robot.turn(90, seconds=5)      # turn 90 degrees over 5 seconds
robot.arc(200, 180, seconds=8) # arc over 8 seconds
```

The library calculates the step interval needed to spread the required number of steps across the given time:

```
step_interval = (seconds × 1_000_000) / total_steps
```

If the requested interval would be faster than the minimum (1200 µs), the motor simply runs at maximum speed. You cannot make the motors go faster than their maximum.

---

## Why speed control is useful

- **Smooth, controlled moves** — a slow approach to a target looks more intentional than a full-speed dash.
- **Combining with nowait** — starting a slow move with `nowait=True` gives you time to do other things (such as updating pixels) while the robot creeps forward.
- **Demonstrating execution order** — a slow move makes it much easier to observe exactly when blocking and non-blocking code runs.

---

## Speed and accuracy

Slower moves are generally *more* accurate than fast ones, because the motor has more time to develop torque at each step. If you find the robot's movements are inconsistent at full speed, try adding a modest `seconds=` value.

The minimum useful speed is limited by the gear train — at very long step intervals the robot stutters rather than moving smoothly. Stay above about `seconds=30` for a 300 mm move.
