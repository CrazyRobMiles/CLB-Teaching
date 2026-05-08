# Lab 4: Servo Driver Class

In Lab 3 you controlled a servo by writing directly to PCA9685 registers. This works, but it is fragile — the register addresses, the prescale formula, and the pulse-count arithmetic are all details you don't want to repeat everywhere.

Two classes solve this cleanly:

- **`PCA9685`** — handles all I2C communication with the chip (already provided in the skeleton)
- **`ServoDriver`** — wraps one channel and exposes a single `angle()` method

---

## The PCA9685 class (provided)

The skeleton contains a complete `PCA9685` implementation. Read it — it is a good example of how to encapsulate a hardware protocol:

- The constructor wakes the chip and enables auto-increment
- `set_freq(hz)` handles the prescale calculation and the sleep/wake sequence
- `set_pwm(channel, on, off)` uses `ustruct.pack` to write 4 bytes in one transaction
- `_write` and `_read` are private helpers to keep the other methods readable

You will not need to change this class.

---

## The ServoDriver class (your task)

`ServoDriver.__init__` takes the `PCA9685` object and a channel number (0–15). It stores both.

`ServoDriver.angle(degrees)` needs to:

1. Clamp `degrees` to the range 0–180
2. Map it linearly to a pulse count between `MIN_PULSE` (150) and `MAX_PULSE` (600)
3. Call `self._pca.set_pwm(self._channel, 0, pulse)`

---

## The mapping

```
pulse = MIN_PULSE + (MAX_PULSE − MIN_PULSE) × degrees / 180
```

At 0°: `150 + 450 × 0 / 180 = 150`  
At 90°: `150 + 450 × 90 / 180 = 375`  
At 180°: `150 + 450 × 180 / 180 = 600`

Use `int(...)` to convert to a whole number before passing to `set_pwm`.
