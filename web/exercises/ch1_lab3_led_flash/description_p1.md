# Lab 3: LED Flashing

Typing commands one at a time works for testing, but it's not practical for anything that needs to happen repeatedly or at speed. In this lab you'll write your first MicroPython program — a loop that flashes the LED automatically.

---

## Programs vs the console

When you type in the console, MicroPython runs each line immediately and then waits. A **program** is a file of code that runs from top to bottom on its own. On the Pico, a file called `main.py` runs automatically every time the board starts up.

The editor above the console already has a `main.py` skeleton open. You'll fill in the missing lines.

---

## `while True`

```python
while True:
    do_something()
```

`while True` creates an **infinite loop** — the body repeats forever (or until you interrupt it with Ctrl+C). This is the standard pattern for embedded programs that should run continuously.

---

## `time.sleep`

```python
import time
time.sleep(0.5)
```

`time.sleep(seconds)` pauses execution for the given number of seconds. You can use decimal values: `0.5` is half a second, `0.1` is a tenth of a second.

---

## The flashing pattern

```
turn LED on
wait 0.5 s
turn LED off
wait 0.5 s
(repeat forever)
```

Each pass through the loop takes 1 second, so the LED flashes once per second.
