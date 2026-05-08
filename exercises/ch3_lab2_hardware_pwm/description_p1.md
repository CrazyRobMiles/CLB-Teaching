# Lab 2: Hardware PWM

The Raspberry Pi Pico contains dedicated **PWM hardware**: eight independent PWM slices, each with two output channels (A and B), giving 16 PWM-capable pins in total. The hardware generates the waveform on its own — the CPU sets the parameters once and the slice runs continuously with no further intervention.

---

## The Pico PWM slices

Each slice has one counter that runs from 0 up to a **wrap** value at a fixed clock rate, then resets. Each channel (A or B) has a **compare** value: the output is HIGH while the counter is below the compare value and LOW otherwise.

```
counter:  0 ──────────── compare ──────── wrap ──── (restart)
output:   HIGH ──────────────────|  LOW  |
                    on time            off time
```

Changing the compare value changes the duty cycle instantly and precisely, with no jitter.

---

## machine.PWM in MicroPython

```python
from machine import Pin, PWM

led = PWM(Pin(15))   # attach hardware PWM to GP15
led.freq(1000)       # 1 kHz
led.duty_u16(32768)  # 50%  (32768 / 65535 ≈ 0.5)
```

`duty_u16()` takes a 16-bit value: **0** is fully off, **65535** is fully on.

---

## Pico PWM pins

Any GPIO pin can be used for PWM. The slice assignment is fixed:

| Slice | Channel A | Channel B |
|-------|-----------|-----------|
| 0 | GP0 | GP1 |
| 1 | GP2 | GP3 |
| 2 | GP4 | GP5 |
| 3 | GP6 | GP7 |
| … | … | … |

Two pins sharing a slice share the same frequency but can have independent duty cycles.
