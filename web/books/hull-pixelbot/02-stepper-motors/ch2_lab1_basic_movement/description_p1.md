# Lab 1: Basic Movement

The Hull Pixelbot uses two **28BYJ-48 stepper motors** — one for each wheel. A stepper motor moves in discrete steps rather than spinning freely, which means you can tell it to move exactly the number of steps that corresponds to a given distance or angle without needing any additional sensors.

---

## How the stepper driver works

Each motor is driven by a **ULN2003 board** that connects four GPIO pins from the Pico to the four coils inside the motor. The robot library's stepper driver sends an 8-step half-step sequence to the coils using a hardware timer interrupt. The interrupt fires every 200 microseconds and advances each motor by one step when the motor's individual timing says it is due.

Because the stepping happens in the timer interrupt, the motors run completely independently of your program code. When a move finishes, the driver de-energises the coils automatically — your program does not need to do anything.

---

## Movement commands

```python
robot.move(mm)       # move forward (positive) or backward (negative) in mm
robot.turn(degrees)  # turn clockwise (positive) or anti-clockwise (negative)
```

Both commands **block by default** — they do not return until the move is complete. This makes it easy to write sequential programs:

```python
robot.colour(robot.GREEN)
robot.move(200)    # robot travels 200 mm — pixel stays green the whole time
robot.colour(robot.RED)   # pixel changes to red only when the move finishes
```

The pixel colour in this example tells you exactly when each statement runs. While the robot is moving, the pixel stays green. The moment `move()` returns, the pixel turns red.

---

## Distance and accuracy

The library converts millimetres to motor steps using the wheel geometry in `config.py`:

```
steps = (distance_mm / (π × wheel_diameter_mm)) × steps_per_rev
```

The default wheel diameter is 69 mm (circumference ≈ 217 mm). Moving 200 mm requires about 3770 half-steps per wheel. Movement accuracy depends on how well `WHEEL_DIAMETER_MM` and `WHEEL_SPACING_MM` match your actual robot — you can tune these values in `config.py`.
