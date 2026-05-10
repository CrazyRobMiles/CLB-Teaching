# Lab 2: LED Control

Now we'll move the LED from the constant 3.3 V supply to a **GPIO pin**, so our program can turn it on and off.

---

## What is GPIO?

GPIO stands for **General Purpose Input/Output**. These are pins that your program can control: set them HIGH (3.3 V) to switch something on, or LOW (0 V) to switch it off. The Pico has 26 usable GPIO pins, labelled GP0 to GP28 on the board.

> **Important:** When you use `machine.Pin(15, ...)`, the number 15 refers to **GP15** — the GPIO number — not the physical pin number on the board. GP15 happens to be physical pin 20.

![Pico pinout diagram](images/pico_pinout.png)

*Diagram: The Raspberry Pi Pico pinout. GPIO numbers (GP0, GP1 … GP28) label each signal pin; physical pin numbers run 1–40 around the outside. GP15 is on the left edge, physical pin 20.*

---

## Update the circuit

Move the resistor from the 3V3 pin (physical pin 36) to **GP15 (physical pin 20)**. Everything else stays the same.

```
Pico GP15 (pin 20) ── resistor ── LED anode (+) ── LED cathode (−) ── GND
```

The LED will go off when you unplug and replug USB now, because GPIO pins start as inputs (floating) at boot. That is exactly what we want.

![Updated circuit](images/lab2_circuit.jpg)

*Photo: Same breadboard as Lab 1, but the resistor now connects to GP15 (physical pin 20) instead of the 3V3 pin.*
