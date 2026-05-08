# Lab 1: Software PWM

To control a motor's speed you need to vary the amount of power delivered to it. You could use a variable resistor, but that wastes energy as heat. The efficient alternative is **Pulse Width Modulation**.

---

## What is PWM?

PWM works by switching the output on and off very rapidly. The motor (or LED, or any load) experiences the average of those pulses.

```
100% duty:  ████████████████████  full power
 75% duty:  ███████████░░░░░░░░░  three-quarters power
 50% duty:  ██████████░░░░░░░░░░  half power
 25% duty:  █████░░░░░░░░░░░░░░░  quarter power
  0% duty:  ░░░░░░░░░░░░░░░░░░░░  off
```

The **duty cycle** is the percentage of each cycle the signal is HIGH. The **frequency** is how many complete cycles happen per second.

---

## Why does averaging work?

A motor has inertia — it cannot instantly change speed. An LED has persistence of vision to the human eye. If the switching is fast enough (above ~50 Hz for an LED, above ~1 kHz for a small motor), the device responds to the average power, not the individual pulses.

---

## Software PWM on a Pico

The simplest way to create a PWM signal is to toggle a GPIO pin manually:

```python
from machine import Pin
import time

led = Pin(15, Pin.OUT)

FREQ = 100    # Hz
DUTY = 50     # %

period   = 1.0 / FREQ       # 0.01 s = 10 ms total cycle
on_time  = period * DUTY / 100   # 5 ms on
off_time = period - on_time      # 5 ms off

while True:
    led.value(1)
    time.sleep(on_time)
    led.value(0)
    time.sleep(off_time)
```

This is called **software PWM** because the CPU itself is doing all the timing work.
