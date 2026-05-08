# Lab 1: Servo Motors

A **servo motor** is a DC motor combined with a gearbox and a position sensor. The sensor feeds back to a small control circuit that drives the motor until the shaft reaches the commanded position, then holds it there. This makes servos fundamentally different from the DC motors in Chapter 3:

| | DC motor | Servo |
|--|----------|-------|
| Control | Speed and direction | Position (angle) |
| Command | PWM duty cycle | PWM pulse width |
| Feedback | None (open loop) | Built-in position sensor |
| Typical use | Drive wheels, fans, pumps | Steering, arms, pan/tilt |

---

## PWM control for servos

Servos use a very specific PWM format: a **50 Hz** signal (20 ms period) where the **width of the high pulse** determines the angle. The duty cycle matters only indirectly — it is the absolute pulse time in milliseconds that counts.

```
Period = 20 ms (50 Hz)

  1.0 ms pulse → ~0°
  1.5 ms pulse → ~90°
  2.0 ms pulse → ~180°

  |← 1.5 ms →|←─── 18.5 ms ───→|
  ████████████░░░░░░░░░░░░░░░░░░░░
```

Most hobby servos use the 1–2 ms range, though the exact limits vary. Some servos respond to 0.5–2.5 ms.

---

## Wiring a servo

A standard hobby servo has three wires:

| Wire colour | Function |
|-------------|----------|
| Brown / Black | GND |
| Red | 5 V supply |
| Orange / Yellow / White | Signal (PWM) |

The signal wire connects to a Pico GPIO pin. The 5 V supply comes from VBUS (physical pin 40).

> Servos draw significant current (100–600 mA under load). For more than one or two servos, use a separate 5 V supply rather than drawing from VBUS.
