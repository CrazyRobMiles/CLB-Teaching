# Lab 2: Console Exercise — Talk to the PCA9685

With the PCA9685 wired up (SDA→GP0, SCL→GP1, VCC→3V3, GND→GND) and a servo connected to **channel 0**, open the MicroPython REPL and work through each step.

---

## Step 1: Find the device

```python copy
from machine import I2C, Pin
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
print([hex(d) for d in i2c.scan()])
```

Expected output: `['0x40']`

If the list is empty, check that SDA and SCL are not swapped and the board has power. If you see extra addresses, those are other devices sharing the bus — the PCA9685 is always `0x40` unless its address pins are changed.

---

## Step 2: Wake the chip

The PCA9685 boots in sleep mode. Register `0x00` (MODE1) controls the oscillator. Writing `0x20` sets the auto-increment bit and clears the sleep bit:

```python copy
i2c.writeto_mem(0x40, 0x00, bytes([0x20]))
```

Read it back to confirm:

```python copy
print(hex(i2c.readfrom_mem(0x40, 0x00, 1)[0]))
```

Expected: `0x20`

---

## Step 3: Set 50 Hz

Servos need a 50 Hz PWM signal. The chip's internal oscillator runs at 25 MHz and divides by `(prescale + 1) × 4096`:

```
prescale = round(25_000_000 / (4096 × 50)) − 1 = 121
```

The prescale register can only be written while the oscillator is sleeping, so the sequence is: **sleep → write prescale → wake → restart**.

```python copy
import time

i2c.writeto_mem(0x40, 0x00, bytes([0x30]))   # sleep  (bit 4 set)
i2c.writeto_mem(0x40, 0xFE, bytes([121]))    # prescale = 121
i2c.writeto_mem(0x40, 0x00, bytes([0x20]))   # wake   (bit 4 clear)
time.sleep_ms(5)
i2c.writeto_mem(0x40, 0x00, bytes([0xA0]))   # restart (bit 7 set)
```

---

## Step 4: Move the servo

Channel 0 registers start at `0x06`. There are four bytes per channel: ON_L, ON_H, OFF_L, OFF_H. The ON count is always 0; the OFF count sets the pulse width.

The mapping from degrees to counts:

```
pulse = 150 + (600 − 150) × degrees / 180
```

For **90°**: `150 + 450 × 90/180 = 375` → `0x0177` → OFF_L = `0x77`, OFF_H = `0x01`

```python copy
i2c.writeto_mem(0x40, 0x06, bytes([0, 0, 0x77, 0x01]))   # 90°
```

The servo should move to centre. Try the endpoints:

```python copy
i2c.writeto_mem(0x40, 0x06, bytes([0, 0, 0x96, 0x00]))   # 0°  (count 150 = 0x0096)
i2c.writeto_mem(0x40, 0x06, bytes([0, 0, 0x58, 0x02]))   # 180° (count 600 = 0x0258)
```

---

## What you just did

Four `writeto_mem` calls over two wires moved a servo motor. You drove the chip directly at the register level — no library, no abstraction. This is exactly the kind of sequence that belongs inside a class, which is what Labs 3 and 4 are about.
