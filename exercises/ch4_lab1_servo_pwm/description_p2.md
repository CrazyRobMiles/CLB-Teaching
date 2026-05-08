# Lab 1: Driving a Servo Directly

You can control a single servo with the Pico's hardware PWM — the same `machine.PWM` from Chapter 3, Lab 2.

---

## Console commands

Connect the servo signal wire to **GP15**. Type these in the Console:

```python
from machine import Pin, PWM

servo = PWM(Pin(15))
servo.freq(50)          # 50 Hz — required for standard servos
```

The `duty_u16` value that corresponds to a pulse width of `t` milliseconds at 50 Hz is:

```
duty = t_ms / 20 × 65535
```

| Angle | Pulse | duty_u16 |
|-------|-------|----------|
| 0° | 1.0 ms | 3277 |
| 90° | 1.5 ms | 4915 |
| 180° | 2.0 ms | 6554 |

```python
servo.duty_u16(3277)    # 0°
servo.duty_u16(4915)    # 90°
servo.duty_u16(6554)    # 180°
```

Try each value and watch the servo move.

---

## The inconvenience

To move to a specific angle you must calculate the duty value each time. It is easy to get the maths wrong, and the numbers are not intuitive. A better interface would be:

```python
servo.angle(90)
```

That is exactly what you will build in Lab 4. But first, in Labs 2 and 3, you will meet the PCA9685 — an intelligent peripheral that generates the PWM signals for up to 16 servos at once, controlled over two wires (I2C).
