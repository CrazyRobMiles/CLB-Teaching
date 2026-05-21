# Lab 5: Button-Controlled Motor

You now have a working `MotorDriver` class and experience with button edge detection from Chapter 1. This lab combines them: two buttons control a motor's speed and direction.

---

## Design

```
btn_speed (GP14)  — each press cycles through speed presets: 25% → 50% → 75% → 100% → 25%…
btn_dir   (GP13)  — each press toggles between forward and backward
```

The motor keeps running at the current speed and direction until a button is pressed. Both use falling-edge detection so each press fires exactly once, however long the button is held.

---

## Circuit

Keep the L298N wired as in Lab 3. Add:

| Button | Connect between |
|--------|----------------|
| btn_speed | GP14 and GND |
| btn_dir | GP13 and GND |

Both use `Pin.PULL_UP` — no external resistors needed.

![Motor and buttons circuit](images/lab5_circuit.jpg)

*Photo: L298N module connected to Pico with one DC motor on OUT1/OUT2. Two push buttons on GP13 and GP14.*

---

## State variables

The program needs to remember two things between button presses:

```python copy
SPEEDS    = [25, 50, 75, 100]
speed_idx = 0      # index into SPEEDS
forward   = True   # current direction
```

When a speed button press is detected, increment `speed_idx` with modulo and re-apply the motor. When a direction button press is detected, flip `forward` and re-apply.
