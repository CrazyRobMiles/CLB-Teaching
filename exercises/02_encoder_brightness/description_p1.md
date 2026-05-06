# Exercise 02 — Encoder Brightness

In this exercise you will use a **rotary encoder** to control the brightness of a NeoPixel strip. Turning the encoder clockwise increases brightness; turning it anticlockwise decreases it.

This builds directly on Exercise 01. The same event/service pattern applies — you just have a different input device and a different thing to control.

---

## What is a rotary encoder?

A rotary encoder is a knob that can spin freely in either direction. Unlike a potentiometer it has no stops, so it reports *movement* rather than *position*: each click generates a **clockwise** or **anticlockwise** event.

The CLB rotary encoder manager publishes these events automatically. Your app just subscribes to them.

---

## What you will build

```
Encoder turns CW  →  brightness_moved_clockwise event
                  →  your handler adds 0.05 to self.brightness
                  →  indicator.cmd_brightness(self.brightness)

Encoder turns CCW →  brightness_moved_anticlockwise event
                  →  your handler subtracts 0.05
                  →  indicator.cmd_brightness(self.brightness)
```

Brightness is a float from **0.0** (off) to **1.0** (full). Your handlers must clamp the value so it never goes outside that range.

---

## Hardware

| Component | Pin |
|-----------|-----|
| NeoPixel strip (8 LEDs) | GPIO 18 |
| Encoder CLK | GPIO 16 |
| Encoder DT | GPIO 17 |
