# Lab 1: LED Test

Before we write any code, we want to prove that our LED hardware works. If the LED is wired up correctly and it lights up, then any problems later on are in our code — not in the circuit.

---

## What you need

- Raspberry Pi Pico
- One LED (any colour)
- One 220 Ω resistor (red–red–brown–gold bands)
- A breadboard
- Two jumper wires
- A USB cable (micro-B or USB-C, depending on your Pico)

---

## About breadboards

A breadboard lets you build circuits without soldering. The holes are connected in rows. On the outer rails (marked + and −) the connections run the full length of the board — use these for power. In the main area, each row of 5 holes forms one connected node; the central gap separates the two sides.

![Breadboard diagram](images/breadboard.jpg)

*Photo: A half-size breadboard. The two long rails on each side run vertically; the numbered rows run horizontally in groups of five across the gap.*

---

## About LEDs

An LED (Light Emitting Diode) only conducts in one direction, so polarity matters. The **anode** is the positive terminal — the longer leg. The **cathode** is the negative terminal — the shorter leg (also marked by a flat edge on the plastic body).

![LED polarity](images/led_polarity.jpg)

*Photo: Two LEDs side by side. The longer leg (anode, +) is on the left; the shorter leg (cathode, −) and the flat edge of the lens body are visible.*
