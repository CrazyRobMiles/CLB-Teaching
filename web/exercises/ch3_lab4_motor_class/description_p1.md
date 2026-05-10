# Lab 4: Motor Driver Class

Every time you want to run the motor forward you write three lines: set IN1, set IN2, set ENA duty cycle. When you have two motors — or four — this quickly becomes error-prone and hard to read. A class solves this by naming the concept and hiding the pin details.

---

## Requirements

A `MotorDriver` should:

- Accept the pin numbers in its constructor (so it works for any motor wired to any pins)
- Expose `forward(speed)`, `backward(speed)`, `stop()`, and `brake()` methods
- Accept `speed` as a percentage (0–100) so callers never deal with `duty_u16` values
- Default to stopped when created

This is the **interface design** step: decide what the class looks like to the user before writing any implementation.

---

## The direction logic

| Method | IN1 | IN2 | Speed |
|--------|-----|-----|-------|
| `forward(s)` | 1 | 0 | s% |
| `backward(s)` | 0 | 1 | s% |
| `stop()` | 0 | 0 | 0% |
| `brake()` | 1 | 1 | 100% |

---

## _set_speed helper

Converting a percentage to `duty_u16`:

```python
def _set_speed(self, percent):
    self._pwm.duty_u16(int(percent * 65535 // 100))
```

Integer arithmetic (`//`) avoids floating-point drift. `100 * 65535 // 100` gives exactly 65535; `100 * 65535 / 100` might give 65534.9999… and truncate to 65534.
