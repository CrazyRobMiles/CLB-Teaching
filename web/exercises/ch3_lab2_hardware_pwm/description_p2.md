# Lab 2: Using Hardware PWM

The skeleton in the editor sets up the PWM object. Add the two missing lines to set frequency and duty cycle, then **Save & Run**.

---

## Smooth fade — impossible with software PWM

The solution takes hardware PWM further: it loops through every duty level from 0 to 65535 in steps of 512, sleeping 8 ms between steps. That means:

- 128 steps × 8 ms = just over 1 second to fade up
- The CPU only wakes 128 times per second to update the duty value
- Between updates, the hardware sustains the exact waveform with no CPU involvement

Try doing this with software PWM — you'd need to track phase manually, and any other code in the loop would disrupt the timing.

---

## Key values for motor control

For motor speed control you will typically use:

| Duty | `duty_u16` value | Comment |
|------|-----------------|---------|
| 0% | 0 | Motor off |
| 25% | 16384 | Slow |
| 50% | 32768 | Medium |
| 75% | 49151 | Fast |
| 100% | 65535 | Full speed |

A helper function makes this cleaner:

```python
def set_speed(pwm, percent):
    pwm.duty_u16(int(percent * 65535 // 100))
```

---

## Frequency for motors

For DC motors, 1 kHz (`freq(1000)`) is a common starting point. Too low and you hear an audible whine; too high and inductance in the motor coil resists the switching and reduces effective power. In Lab 3 you will use 1 kHz for the L298N enable pin.

In Lab 3 you will wire the PWM output directly to the L298N and control a real motor.
