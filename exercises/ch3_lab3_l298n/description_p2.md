# Lab 3: Wiring and Power

## Circuit

| L298N pin | Connect to |
|-----------|-----------|
| IN1 | Pico GP2 |
| IN2 | Pico GP3 |
| ENA | Pico GP6 (PWM) |
| IN3 | Pico GP4 |
| IN4 | Pico GP5 |
| ENB | Pico GP7 (PWM) |
| VSS (logic) | Pico 5V (VBUS, pin 40) |
| GND | Common ground with Pico |
| VS (motor) | External battery (6–12 V) |
| OUT1, OUT2 | Motor A terminals |
| OUT3, OUT4 | Motor B terminals |

> **Important:** The motor supply (VS) and the logic supply (VSS) must share a common ground with the Pico. Never connect the motor battery directly to Pico power pins.

![L298N wiring](images/lab3_wiring.jpg)

*Diagram: Pico connected to L298N module. Direction pins from GP2–GP5; PWM enable from GP6 and GP7; motor power from a separate battery pack; grounds joined.*

---

## Power supply note

Motors draw large transient currents when starting or changing direction. Use a battery pack (4× AA = 6 V, or a 9 V regulated supply) rather than a USB power bank, which may current-limit. A 100 µF capacitor across the motor terminals reduces electrical noise fed back to the Pico.
