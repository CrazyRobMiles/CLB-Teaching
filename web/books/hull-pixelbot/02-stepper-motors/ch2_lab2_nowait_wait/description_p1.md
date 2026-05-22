# Lab 2: Nowait and Wait

By default `move()` and `turn()` block until the robot stops. This is convenient for sequential programs, but sometimes you want your code to keep running while the robot is moving — for example, to change the pixel colour mid-move, or to check a sensor.

---

## Starting a move without waiting

Adding `nowait=True` tells the move to start the motors and return immediately:

```python
robot.colour(robot.GREEN)
robot.move(400, nowait=True)   # motors start, function returns at once
robot.colour(robot.BLUE)       # this runs while the motors are still moving
robot.wait()                   # block here until the move finishes
robot.colour(robot.BLACK)
```

In this program:
- The pixel turns green before the move starts.
- `move(400, nowait=True)` queues 400 mm of forward travel and returns immediately.
- The pixel turns blue — while the robot is still moving.
- `wait()` blocks until the motors stop.
- The pixel turns black when the move is done.

---

## The wait() function

`robot.wait()` blocks until there is no movement in progress. It does nothing if the robot is already stationary.

```python
robot.move(500, nowait=True)
# ... do other things here ...
robot.wait()           # guarantee motors are stopped before continuing
robot.turn(90)
```

---

## The moving() function

`robot.moving()` returns `True` if the motors are currently running and `False` if not. You can use it to make decisions based on whether the robot is still moving:

```python
robot.move(1000, nowait=True)
while robot.moving():
    robot.colour(robot.GREEN)
robot.colour(robot.RED)
```

---

## Why nowait can cause surprises

```python
robot.move(1000, nowait=True)
robot.move(200)           # overrides the first move immediately
```

The second `move()` cancels the first — the robot never travels 1000 mm. Be careful when issuing a new move command before the previous one has finished.
