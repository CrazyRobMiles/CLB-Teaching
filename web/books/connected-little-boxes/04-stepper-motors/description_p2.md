# Lab 4: Wiring

The robot has two motors, each connected through its own ULN2003 board to the Pico. The two boards are independent — they do not share control pins, only power and ground.

---

## Left motor

| ULN2003 board | Pico |
|---------------|------|
| IN1 | GPIO 15 |
| IN2 | GPIO 14 |
| IN3 | GPIO 13 |
| IN4 | GPIO 12 |
| VCC | VBUS (pin 40, 5 V) |
| GND | Any GND pin |

---

## Right motor

| ULN2003 board | Pico |
|---------------|------|
| IN1 | GPIO 8 |
| IN2 | GPIO 9 |
| IN3 | GPIO 10 |
| IN4 | GPIO 11 |
| VCC | VBUS (pin 40, 5 V) |
| GND | Any GND pin |

Both VCC pins can share the same VBUS wire. Both GND pins must share the same ground as the Pico.

> **Important:** Connect motor VCC to **VBUS** (5 V), not to **3V3** (3.3 V). The motors draw up to 200 mA per coil and will not run reliably from the 3.3 V rail.

---

## Why the left motor's pins are in reverse order

The two motors are mounted facing opposite directions on the robot chassis. If both stepped through the same coil sequence, one wheel would drive forward and the other backward.

The fix is to reverse the pin order for one motor in the settings. With `[15, 14, 13, 12]` for the left and `[8, 9, 10, 11]` for the right, the half-step sequence fires the coils in opposite physical directions, so both wheels move forward when `move()` is called with a positive value.

---

## Power supply note

Each motor draws up to 200 mA per coil; with up to two coils active at once that is 400 mA per motor, 800 mA total at peak. A standard USB port is rated for 500 mA.

In practice the average current is much lower because only one or two coils fire at a time and they share an 8-step cycle. Most USB ports handle this without issue. If the Pico resets unexpectedly during fast movement, use a powered USB hub or a 5 V wall adapter.

---

## Verifying the wiring before enabling the manager

With the stepper manager disabled, test each ULN2003 board from the REPL. The IN pin LEDs should light and the motor should make a faint click as the coil energises:

```python copy
from machine import Pin

# Test left motor IN1 (GPIO 15)
p = Pin(15, Pin.OUT)
p.value(1)    # LED on ULN2003 board lights
p.value(0)    # LED goes off

# Test right motor IN1 (GPIO 8)
p = Pin(8, Pin.OUT)
p.value(1)
p.value(0)
```

Repeat for each IN2–IN4 pin on both boards. If all eight LEDs respond, the control wiring is correct.
