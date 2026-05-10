# Lab 4: Implementing and Testing

The skeleton in the editor has the class structure and all the method signatures. Fill in each method body — most are two or three lines.

---

## What to implement

**`forward(speed)`** — set IN1 high, IN2 low, call `_set_speed(speed)`

**`backward(speed)`** — set IN1 low, IN2 high, call `_set_speed(speed)`

**`stop()`** — set both direction pins low, call `_set_speed(0)`

**`brake()`** — set both direction pins high, call `_set_speed(100)`

**`_set_speed(percent)`** — `self._pwm.duty_u16(int(percent * 65535 // 100))`

---

## Testing from the console

Once **Save & Run** completes, the two test lines at the bottom of the file will run: motor A forward at 50%, motor B backward at 75%. Then test interactively:

```python
motor_a.forward(25)     # slow forward
motor_a.brake()         # immediate stop
motor_b.forward(100)    # full speed
motor_b.stop()          # coast
```

---

## Using it as a module

In Lab 5 you will copy this class into the top of the next file. In a real project you would save the class as `motor.py` on the device and import it:

```python
from motor import MotorDriver

left  = MotorDriver(2, 3, 6)
right = MotorDriver(4, 5, 7)
```

This is the same pattern used in the Connected Little Boxes framework — each capability lives in its own file and is imported where needed.
