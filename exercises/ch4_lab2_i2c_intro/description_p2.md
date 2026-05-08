# Lab 2: I2C on the Pico

## Pico I2C pins

The Pico has two I2C controllers (I2C0 and I2C1), each available on multiple pin pairs:

| Controller | SDA options | SCL options |
|------------|-------------|-------------|
| I2C0 | GP0, GP4, GP8, GP12, GP16, GP20 | GP1, GP5, GP9, GP13, GP17, GP21 |
| I2C1 | GP2, GP6, GP10, GP14, GP18, GP26 | GP3, GP7, GP11, GP15, GP19, GP27 |

For Chapter 4 we use **GP0 (SDA)** and **GP1 (SCL)** on I2C0.

---

## Setting up I2C in MicroPython

```python
from machine import I2C, Pin

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
```

`freq=400000` is 400 kHz — "Fast Mode". Most devices support this; some older ones need 100 kHz.

---

## Scanning the bus

`i2c.scan()` sends every possible address and returns a list of those that respond:

```python
devices = i2c.scan()
print([hex(d) for d in devices])
```

Connect the PCA9685 breakout board (SDA→GP0, SCL→GP1, VCC→3V3, GND→GND) and run this. You should see `['0x40']`.

If nothing appears, check:
- SDA and SCL are not swapped
- The device has power (its LED or indicator should be on)
- The pull-up resistors are present (most breakout boards include them)

---

## Reading and writing registers

```python
# Write one byte to register 0x00 of device 0x40
i2c.writeto_mem(0x40, 0x00, bytes([0x20]))

# Read one byte from register 0x00
val = i2c.readfrom_mem(0x40, 0x00, 1)
print(hex(val[0]))
```

On the next page you will use exactly these calls to bring the PCA9685 to life.
