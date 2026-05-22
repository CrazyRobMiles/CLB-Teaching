# Lab 3: Pixel Patterns

So far `robot.colour()` has set **all** pixels to the same colour. The robot library also lets you set **individual pixels** by index, which makes it possible to display patterns and chasing effects.

---

## Setting individual pixels

```python
robot.colour(robot.GREEN)          # sets all pixels
robot._pixels.set(index, rgb)      # sets one pixel by index
```

Pixels are numbered from 0 at one end of the strip to `pixel_count - 1` at the other. For an 8-pixel strip the indices are 0–7.

Pass any colour constant or tuple as the second argument:

```python
robot.colour(robot.BLACK)                      # clear the strip first
robot._pixels.set(0, robot.RED)                # pixel 0 → red
robot._pixels.set(3, robot.GREEN)              # pixel 3 → green
robot._pixels.set(7, robot.BLUE)               # pixel 7 → blue
```

---

## Building a chasing effect

A chasing effect lights one pixel at a time and moves it along the strip:

```python
import time
import robot

robot.init()

while True:
    for i in range(8):
        robot.colour(robot.BLACK)          # clear all pixels
        robot._pixels.set(i, robot.GREEN)  # light pixel i
        time.sleep(0.1)
```

Each iteration clears the strip, lights the next pixel, waits a short time, then moves on.

---

## Custom colours

Any `(r, g, b)` tuple works wherever a colour constant does:

```python
robot._pixels.set(3, (255, 128, 0))   # pixel 3 orange
robot._pixels.set(5, (128, 0, 128))   # pixel 5 purple
```

Values must be integers in the range 0–255.
