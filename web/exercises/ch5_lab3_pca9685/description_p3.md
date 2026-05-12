# Lab 3: Understanding the Transaction

## What happens on the wire

When you call `i2c.writeto_mem(0x40, 0x06, bytes([0, 0, 0x33, 0x01]))`, the I2C bus carries:

```
START
  0x40 << 1 | WRITE    ← device address + write flag
  0x06                 ← register address (LED0_ON_L)
  0x00                 ← ON_L  = 0
  0x00                 ← ON_H  = 0
  0x33                 ← OFF_L = 0x33 = 51
  0x01                 ← OFF_H = 0x01
STOP
```

The OFF count = `0x0133` = 307, corresponding to a 1.5 ms pulse (90°).

The START/STOP framing, clock generation, and bit serialisation are all handled by the Pico's I2C hardware. You see only the four bytes of payload.

---

## The prescale formula

The PCA9685 internal oscillator runs at 25 MHz. It divides this by `(prescale + 1) × 4096` to produce the PWM frequency:

```
freq = 25,000,000 / ((prescale + 1) × 4096)

prescale = round(25,000,000 / (4096 × freq)) − 1
         = round(25,000,000 / (4096 × 50)) − 1
         = round(122.07) − 1
         = 121
```

The actual frequency with prescale=121 is slightly off: `25,000,000 / (122 × 4096) ≈ 50.05 Hz`. Servos tolerate this — they are not sensitive to a 0.1% frequency error.

---

## What makes the PCA9685 an "intelligent peripheral"?

After you write the prescale and the channel registers, the PCA9685 generates the PWM signals **independently of the Pico**. The Pico's CPU can sleep, run other code, or even reboot — the chip keeps driving the servos at the last commanded positions. This is the key property of intelligent peripherals: they offload continuous work from the host processor.

In Lab 4 you will build the `PCA9685` and `ServoDriver` classes that hide these register details and present a clean Python interface.
