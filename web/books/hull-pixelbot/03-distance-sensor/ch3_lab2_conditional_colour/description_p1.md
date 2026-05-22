# Lab 2: Conditional Colour

Now that you can read the distance sensor, you can use the reading to control the robot's pixels. This is the first step toward reactive behaviour — the robot responds to its environment.

---

## Distance zones

A useful pattern divides the sensor range into zones and assigns a colour to each:

```python
mm = robot.distance()

if mm < 0:
    robot.colour(robot.WHITE)    # error — no reading
elif mm < 100:
    robot.colour(robot.RED)      # very close
elif mm < 300:
    robot.colour(robot.YELLOW)   # moderate distance
else:
    robot.colour(robot.GREEN)    # far away
```

The `if / elif / else` chain tests each condition in order and runs the first block whose condition is True. Only one block runs per reading.

---

## Polling in a loop

To make the display update continuously, put the reading and the colour logic inside a `while True` loop:

```python
while True:
    mm = robot.distance()
    if mm < 0:
        robot.colour(robot.WHITE)
    elif mm < 100:
        robot.colour(robot.RED)
    elif mm < 300:
        robot.colour(robot.YELLOW)
    else:
        robot.colour(robot.GREEN)
```

Each pass through the loop takes one distance reading and updates the pixels accordingly. The HC-SR04 needs a short recovery time between readings, but the time taken by the colour function call is generally sufficient.

---

## Why the pixel is a useful diagnostic

In subsequent labs the robot will be moving. A pixel colour that changes based on sensor readings gives you immediate visual feedback about what the robot is "seeing" — even when it is moving away from you and you cannot read the console.
