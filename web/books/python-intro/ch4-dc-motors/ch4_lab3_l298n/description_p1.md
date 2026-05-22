# Lab 3: The L298N

A microcontroller GPIO pin can only source a few milliamps — nowhere near enough to drive a DC motor, which may draw hundreds of milliamps or more. An **H-bridge** circuit solves this by using the GPIO signal to switch power transistors that carry the full motor current.

---

## The H-bridge

The circuit is called an H-bridge because its four switches look like the letter H, with the motor across the middle:

```
+V ──┬──── SW1 ────┬──── SW2 ────┬
     │             │             │
    SW4        [Motor]          SW3
     │             │             │
GND ─┴─────────────┴─────────────┴
```

- **SW1 + SW3 closed:** current flows left-to-right → forward
- **SW2 + SW4 closed:** current flows right-to-left → backward
- **SW1 + SW2 closed:** motor terminals both at +V → active brake
- **All open:** motor coasts to a stop

The **L298N** is a dual H-bridge IC — it contains two complete H-bridges in one package, capable of driving two motors independently.

---

## L298N pins

| Pin | Purpose |
|-----|---------|
| IN1, IN2 | Direction control for motor A |
| IN3, IN4 | Direction control for motor B |
| ENA | Enable / speed (PWM) for motor A |
| ENB | Enable / speed (PWM) for motor B |
| OUT1, OUT2 | Motor A terminals |
| OUT3, OUT4 | Motor B terminals |
| VS | Motor supply voltage (up to 46 V) |
| VSS | Logic supply (5 V) |
| GND | Common ground |

Most L298N **modules** (breakout boards) include a 5 V regulator, so VSS can be drawn from the regulator output and the Pico's 3.3 V GPIO signals are level-shifted to 5 V.
