# Lab 5: Completing the Program

The skeleton has the `MotorDriver` class, pins, state variables, and the main loop structure. Fill in the two `TODO` blocks inside `while True`.

---

## What to write

**Speed button (falling edge on `btn_speed`):**

```python
if last_speed == 1 and s == 0:
    speed_idx = (speed_idx + 1) % len(SPEEDS)
    if forward:
        motor.forward(SPEEDS[speed_idx])
    else:
        motor.backward(SPEEDS[speed_idx])
```

**Direction button (falling edge on `btn_dir`):**

```python
if last_dir == 1 and d == 0:
    forward = not forward
    if forward:
        motor.forward(SPEEDS[speed_idx])
    else:
        motor.backward(SPEEDS[speed_idx])
```

Or factor the common action into a small helper function (see the solution).

---

## Experiment

**Add a print:** `print(f"Speed: {SPEEDS[speed_idx]}%  Direction: {'fwd' if forward else 'rev'}")` after each state change — watch the console as you press the buttons.

**Add a third button for brake:** Wire a button to GP12. On press, call `motor.brake()` and set `forward = True; speed_idx = 0` to reset state.

**Four-motor robot:** Instantiate four `MotorDriver` objects. For a differential-drive robot (two driven wheels):

```python
left  = MotorDriver(2, 3, 6)
right = MotorDriver(4, 5, 7)

# Drive straight
left.forward(60)
right.forward(60)

# Turn left
left.backward(40)
right.forward(40)
```

In Chapter 5 you will see how the Connected Little Boxes framework manages this kind of multi-component coordination through its event and service system.
