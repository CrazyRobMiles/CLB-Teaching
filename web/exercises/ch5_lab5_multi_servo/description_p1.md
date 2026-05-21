# Lab 5: Multi-Servo Control

This lab brings together everything in the chapter: the PCA9685 driver, the ServoDriver class, and button edge detection. Four servos are connected to channels 0–3 of the PCA9685. Four buttons let you select which servo to control and nudge it left or right by 5° per press.

---

## Hardware

| Component | Connection |
|-----------|-----------|
| PCA9685 SDA | GP0 |
| PCA9685 SCL | GP1 |
| Servo 0–3 signal | PCA9685 channels 0–3 |
| Servo power (5V) | Separate 5 V supply or VBUS (pin 40) |
| btn_prev | GP14 → GND |
| btn_next | GP13 → GND |
| btn_ccw | GP12 → GND |
| btn_cw | GP11 → GND |

All buttons use `Pin.PULL_UP` — no external resistors needed.

---

## Design

```
btn_prev  — select previous servo (wraps: 0 → 3)
btn_next  — select next servo    (wraps: 3 → 0)
btn_ccw   — rotate active servo −5°
btn_cw    — rotate active servo +5°
```

The `active` variable tracks which servo the rotate buttons affect. Servos remember their current angle via `self._degrees` in `ServoDriver`, so selecting a servo and pressing a rotate button works correctly even if the servo was moved earlier.

---

## The nudge method

`ServoDriver.nudge(delta)` in the skeleton is a one-liner: call `self.angle()` with the new position. Because `angle()` already clamps to 0–180, nudging past the end of travel is safe — the servo just stays at the limit.

```python copy
def nudge(self, delta):
    self.angle(self._degrees + delta)
```
