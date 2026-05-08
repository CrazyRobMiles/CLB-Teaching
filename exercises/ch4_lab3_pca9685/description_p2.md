# Lab 3: Initialising the PCA9685

Type these commands in the **Console** to bring up the PCA9685 step by step.

---

## Set up I2C and wake the chip

```python
from machine import I2C, Pin

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
print([hex(d) for d in i2c.scan()])   # should show ['0x40']

# Wake up and enable register auto-increment
i2c.writeto_mem(0x40, 0x00, bytes([0x20]))
```

**Auto-increment** (bit 5 of MODE1) means you can write multiple registers in a single transaction by writing a byte array — the chip automatically advances the register pointer after each byte.

---

## Set the PWM frequency to 50 Hz

```python
prescale = round(25_000_000 / (4096 * 50)) - 1   # = 121

i2c.writeto_mem(0x40, 0x00, bytes([0x10]))         # sleep mode (required to change prescale)
i2c.writeto_mem(0x40, 0xFE, bytes([prescale]))     # set prescale
i2c.writeto_mem(0x40, 0x00, bytes([0x20]))         # wake up
```

---

## Move a servo on channel 0

```python
import ustruct

def set_servo(channel, off_count):
    reg = 0x06 + channel * 4
    i2c.writeto_mem(0x40, reg, ustruct.pack('<HH', 0, off_count))

set_servo(0, 205)   # 0°
set_servo(0, 307)   # 90°
set_servo(0, 410)   # 180°
```

`ustruct.pack('<HH', 0, off_count)` packs two 16-bit little-endian integers: ON=0, OFF=off_count. Writing 4 bytes starting at channel's base register sets all four registers in one transaction.

---

## Move multiple servos

```python
set_servo(0, 307)   # servo 0 → 90°
set_servo(1, 205)   # servo 1 → 0°
set_servo(2, 410)   # servo 2 → 180°
```

All three commands are independent — each sends one I2C transaction to a different register address.

In Lab 4 you will wrap this logic in a clean `ServoDriver` class.
