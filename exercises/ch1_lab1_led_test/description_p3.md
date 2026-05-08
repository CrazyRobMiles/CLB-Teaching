# How This Course Works

Before you write any code, it helps to understand how programs are stored and run on the Pico.

---

## The Pico has a filesystem

The Raspberry Pi Pico stores files in its on-board flash memory. You can create, read, and delete files just like on a computer — they survive when the power is removed.

From the MicroPython console you can see what is on the device:

```python
import os
os.listdir('/')
```

This lists all files in the root directory. On a freshly flashed device you will typically see only `['main.py']`, or an empty list.

---

## `main.py` is special

When MicroPython starts up — whether from power-on or a soft reset — it looks for a file called `main.py` in the root directory and runs it automatically. No other filename gets this treatment.

This means:

- A file called `blink.py` does **nothing** on its own at power-on
- A file called `main.py` runs **every time** the device boots

---

## How exercises are stored

Each exercise in this course saves its program file with a unique name that matches the exercise — for example, `ch1_lab3_led_flash.py`. This has two benefits:

1. **Your work is preserved.** Each exercise file stays on the device as you progress. You can always go back and run an earlier exercise.
2. **Exercises don't interfere.** If every exercise wrote to `main.py`, each one would overwrite the previous one.

When you press **Save & Run**, the course tool does two things:

1. Writes your program to the exercise file (e.g., `/ch1_lab3_led_flash.py`)
2. Writes a one-line `main.py` that runs that file:

```python
exec(open('/ch1_lab3_led_flash.py').read())
```

This means your program also runs at the next power-on — the Pico boots, `main.py` runs, and `main.py` immediately hands control to your exercise file.

---

## Running an earlier exercise

If you want to run an exercise file that isn't the current one, type this in the console (replacing the filename as needed):

```python
exec(open('/ch1_lab3_led_flash.py').read())
```

Or select that exercise in the exercise list and press **Save & Run** again.
