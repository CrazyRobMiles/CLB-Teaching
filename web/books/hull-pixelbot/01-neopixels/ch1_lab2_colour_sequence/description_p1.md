# Lab 2: Colour Sequence

In the previous lab you passed one colour constant at a time to `robot.colour()`. In this lab you will store colour constants in a **list** and use a **loop** to cycle through them automatically.

---

## Storing colours in a list

Colour constants are just values — tuples like `(255, 0, 0)`. You can store them in a list exactly like numbers or strings:

```python
colours = [robot.RED, robot.GREEN, robot.BLUE]
```

You can then pass each one to `robot.colour()` inside a loop:

```python
for c in colours:
    robot.colour(c)
    time.sleep(0.5)
```

On each iteration `c` holds the next colour from the list. The loop is simple, consistent, and easy to extend — just add more constants to the list.

---

## Pacing with time.sleep

`time.sleep(seconds)` pauses the program for the given number of seconds. You can use a decimal for fractions:

| Call | Pause |
|------|-------|
| `time.sleep(1)` | 1 second |
| `time.sleep(0.5)` | half a second |
| `time.sleep(0.1)` | one tenth of a second |

Experiment with the sleep value to change how fast the colours cycle.

---

## Looping forever

Wrapping the loop inside `while True` makes it run until you stop the program:

```python
while True:
    for c in colours:
        robot.colour(c)
        time.sleep(0.5)
```
