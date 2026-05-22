# Lab 5: Movement Sequences

You now have the full movement toolkit: `move()`, `turn()`, `arc()`, `nowait`, `wait()`, and `seconds=`. In this lab you will combine them to make the robot trace geometric shapes.

---

## Driving a square

To trace a square, the robot makes four moves of equal length with a 90-degree turn between each:

```python
for _ in range(4):
    robot.move(200)
    robot.turn(90)
```

The `for _ in range(4)` idiom repeats the indented block four times. The `_` variable is used by convention when the loop counter is not needed.

---

## Adding pixel feedback

Colour the pixels to match each leg:

```python
colours = [robot.RED, robot.GREEN, robot.BLUE, robot.CYAN]

for c in colours:
    robot.colour(c)
    robot.move(200)
    robot.turn(90)

robot.colour(robot.BLACK)
```

Each leg of the square uses a different colour. Because `move()` blocks, the colour changes exactly when the robot starts a new leg.

---

## Equilateral triangle

An equilateral triangle has three sides of equal length and exterior angles of 120 degrees:

```python
for _ in range(3):
    robot.move(250)
    robot.turn(120)
```

---

## Combining arcs and straight lines

More interesting paths combine straight moves with arcs:

```python
robot.move(200)
robot.arc(100, 180)   # U-turn
robot.move(200)       # back along a parallel track
```
