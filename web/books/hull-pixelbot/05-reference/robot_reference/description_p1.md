# Robot Library Reference

All functions are called as `robot.function_name(...)` after `import robot` at the top of your program.

---

## Setup

```python
robot.init()
```

Call **once** at the top of every program. Reads pin and wheel settings from `config.py` automatically.

---

## Colour Constants

Use these names with `robot.colour()`, or write any colour as an `(r, g, b)` tuple where each value is 0–255.

| Constant | Colour |
|----------|--------|
| `robot.RED` | Red |
| `robot.GREEN` | Green |
| `robot.BLUE` | Blue |
| `robot.CYAN` | Cyan |
| `robot.MAGENTA` | Magenta |
| `robot.YELLOW` | Yellow |
| `robot.WHITE` | White |
| `robot.BLACK` | Off |

```python
robot.colour(robot.GREEN)       # named constant
robot.colour((255, 128, 0))     # custom orange as an (r, g, b) tuple
robot.colour(robot.BLACK)       # turn all pixels off
```

---

## Movement

| Function | What it does |
|----------|--------------|
| `robot.move(mm)` | Move forward (positive) or backward (negative) |
| `robot.turn(degrees)` | Turn on the spot — positive = clockwise |
| `robot.arc(radius_mm, angle_deg)` | Drive a curved arc |
| `robot.stop()` | Stop motors immediately and de-energise the coils |
| `robot.wait()` | Block until the current move finishes |
| `robot.moving()` | Return `True` if the motors are currently running |

`move()`, `turn()`, and `arc()` **block by default** — they return only when the move is complete.

### Optional parameters

| Parameter | Default | Effect |
|-----------|---------|--------|
| `seconds=` | Full speed | Spread the move over this many seconds |
| `nowait=True` | — | Return immediately; call `robot.wait()` later |

```python
robot.move(200)                  # forward 200 mm at full speed
robot.move(-100)                 # backward 100 mm
robot.turn(90)                   # clockwise quarter-turn
robot.turn(-180)                 # anti-clockwise half-turn
robot.move(500, seconds=10)      # slow move — 500 mm over 10 seconds
robot.move(200, nowait=True)     # start moving, return immediately
robot.wait()                     # ...then wait for the move to finish
```

### Arc sign conventions

| Sign | Effect |
|------|--------|
| `radius_mm` positive | Arc curves **right** |
| `radius_mm` negative | Arc curves **left** |
| `angle_deg` positive | Travel **clockwise** |
| `angle_deg` negative | Travel **anti-clockwise** |

```python
robot.arc(300, 90)    # quarter-circle curving right, 300 mm radius
robot.arc(-200, 45)   # 45-degree arc curving left, 200 mm radius
```

A large radius gives a gentle curve; a small radius gives a tight curve.

---

## Distance Sensor

```python
mm = robot.distance()
```

Fires one ultrasonic pulse and returns the distance to the nearest object in **millimetres**. Returns **-1** if no echo is received (nothing in range, or no sensor fitted).

Always check for `-1` before using the reading:

```python
mm = robot.distance()
if mm > 0 and mm < 200:
    # something is within 200 mm
    robot.colour(robot.RED)
```

---

## Utilities

| Function | Returns | Description |
|----------|---------|-------------|
| `robot.random_val()` | `int` 1–12 | Random integer — useful for unpredictable behaviour |
| `robot.check()` | — | Stops the robot if a key is pressed in Thonny or mpremote |

`robot.check()` is called automatically inside every blocking move. You only need to call it yourself in loops that do not call any movement functions.

---

## Program Template

Every robot program follows the same pattern:

```python
import time
import robot

robot.init()

# --- your code goes here ---

robot.colour(robot.BLACK)
robot.stop()
```

To run your program **standalone in the arena**, save it as `main.py` on the Pico (**File → Save As → MicroPython device → main.py** in Thonny). It will start automatically every time the Pico powers up.
