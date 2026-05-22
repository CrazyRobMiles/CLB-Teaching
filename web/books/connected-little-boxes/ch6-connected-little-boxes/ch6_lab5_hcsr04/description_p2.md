# Lab 5: Wiring

The HC-SR04 has four pins. Three are straightforward; one requires attention.

| HC-SR04 pin | Connect to |
|-------------|------------|
| VCC | VBUS (Pico pin 40, 5 V) |
| GND | Any GND pin |
| TRIG | GPIO 5 (direct) |
| ECHO | GPIO 18 **via voltage divider** (see below) |

---

## The ECHO voltage problem

The HC-SR04 runs on 5 V and its ECHO pin outputs a **5 V logic signal**. A Pico GPIO input is rated for a maximum of 3.3 V. Connecting ECHO directly risks damaging the Pico.

The simplest fix is a resistor voltage divider between ECHO and GPIO:

```
HC-SR04                    Pico
  ECHO ──── 1 kΩ ──┬──── GPIO 18
                   │
                 2 kΩ
                   │
                  GND
```

The divider output is 5 V × 2/(1+2) = **3.33 V** — within the Pico's rated input range.

Use any standard resistor values that give approximately a 2:1 ratio. 1 kΩ + 2 kΩ is the most common choice. Exact values are not critical; anything from 1 kΩ + 2 kΩ to 4.7 kΩ + 10 kΩ works fine.

The TRIG pin does not need a divider — it is an input to the sensor and the Pico drives it. A 3.3 V signal is accepted by the HC-SR04 without issue.

---

## If you have an HC-SR04P

The **HC-SR04P** (note the P) is a 3.3 V compatible variant. Its ECHO pin outputs 3.3 V when powered from 3.3 V, so no voltage divider is needed. Connect VCC to the Pico's **3V3** pin (pin 36) instead of VBUS, and wire ECHO directly to GPIO 18.

Check the markings on your sensor board — both variants look nearly identical.

---

## Wiring summary

```
Pico pin 40  (VBUS 5V)  ────  HC-SR04 VCC
Pico pin 38  (GND)      ────  HC-SR04 GND
Pico GP5                ────  HC-SR04 TRIG
Pico GP18               ────  1 kΩ ─── HC-SR04 ECHO
                                │
                              2 kΩ
                                │
Pico GND                ────────┘
```

---

## Verifying the wiring

Before enabling the manager, confirm the trigger pin works from the REPL:

```python copy
from machine import Pin
import time

trig = Pin(5, Pin.OUT)
trig.value(0)
time.sleep_us(5)
trig.value(1)
time.sleep_us(10)
trig.value(0)
```

You should hear a faint click from the sensor when the trigger fires. You will not hear an echo at this point — the echo pin needs an interrupt handler to be useful, which the manager provides.
