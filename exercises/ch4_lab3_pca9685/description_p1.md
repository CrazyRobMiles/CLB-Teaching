# Lab 3: The PCA9685

The PCA9685 is a 16-channel, 12-bit PWM controller from NXP. It generates up to 16 independent PWM signals with no CPU involvement — you set the parameters once over I2C, and the chip produces the waveforms indefinitely.

This is an example of an **intelligent peripheral**: a specialised chip that handles a complex task (precise multi-channel PWM timing) and exposes a simple register interface for configuration and control.

---

## Why a dedicated PWM chip?

- The Pico has 16 PWM channels, but they are grouped into 8 slices. Two channels sharing a slice must have the same frequency.
- For 16 independently-timed servos you would need 16 separate slices — more than the Pico has.
- The PCA9685 solves this: all 16 channels share one oscillator but each can have an independent duty cycle. One I2C transaction updates a channel.

---

## Key registers

| Register | Address | Purpose |
|----------|---------|---------|
| MODE1 | 0x00 | Sleep, restart, auto-increment |
| PRE_SCALE | 0xFE | Sets PWM frequency |
| LED0_ON_L | 0x06 | Channel 0 on-count low byte |
| LED0_ON_H | 0x07 | Channel 0 on-count high byte |
| LED0_OFF_L | 0x08 | Channel 0 off-count low byte |
| LED0_OFF_H | 0x09 | Channel 0 off-count high byte |

Each channel has 4 registers (ON_L, ON_H, OFF_L, OFF_H). Channel N starts at register `0x06 + N × 4`.

---

## 12-bit resolution

Within each 20 ms period (at 50 Hz), the counter counts 0 to 4095. The ON count sets when the pulse goes HIGH; the OFF count sets when it goes LOW. For servos, the ON count is always 0:

```
ON  = 0
OFF = pulse_counts
```

where `pulse_counts = pulse_ms / 20 × 4096`.

| Angle | Pulse | OFF count |
|-------|-------|-----------|
| 0° | 1.0 ms | 205 |
| 90° | 1.5 ms | 307 |
| 180° | 2.0 ms | 410 |
