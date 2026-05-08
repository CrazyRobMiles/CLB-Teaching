# Lab 1: NeoPixel Test

NeoPixels (technically WS2812B LEDs) are individually-addressable RGB LEDs that chain together in a strand. Each pixel contains a red, green, and blue LED element plus a tiny control chip. You send colour data in at one end of the chain, and each chip reads its own value and passes the rest on to the next pixel.

This means a single GPIO pin can control a strand of any length.

---

## Hardware

You need:
- A NeoPixel strand (8 pixels recommended — shorter is fine)
- Raspberry Pi Pico
- A 300 Ω resistor (protects the first pixel from signal spikes)
- Three jumper wires

### Wiring

| NeoPixel wire | Connect to |
|---------------|-----------|
| +5V or VCC | Pico pin 36 (3V3) |
| GND | Pico GND (pin 38) |
| DIN (data in) | 300 Ω resistor → GP15 (pin 20) |

> **Note:** Running the strand on 3.3 V instead of 5 V makes it slightly dimmer but keeps the wiring simple and safe — no separate power supply needed for short strands. For strands longer than 30 pixels you would want 5 V and a dedicated power supply.

![NeoPixel wiring](images/lab1_wiring.jpg)

*Photo: A NeoPixel strand connected to a Pico. The data line runs via a 300 Ω resistor to GP15; VCC connects to the 3V3 pin; GND to GND.*

---

## How the chain works

Each NeoPixel reads the first colour value off the data line, stores it, then forwards all subsequent values to the next pixel. The Pico sends the full list of colours in one burst every time you call `np.write()`.

![NeoPixel chain diagram](images/lab1_chain.jpg)

*Diagram: Three NeoPixels in series. The Pico sends colours [A, B, C] on the data line; pixel 0 keeps A and forwards [B, C]; pixel 1 keeps B and forwards [C]; pixel 2 keeps C.*
