from machine import I2C, Pin
import ustruct
import time


class PCA9685:
    """I2C driver for the PCA9685 16-channel PWM controller."""

    def __init__(self, i2c, address=0x40):
        self._i2c = i2c
        self._addr = address
        self._write(0x00, 0x20)   # wake up, enable register auto-increment

    def set_freq(self, freq_hz):
        """Set the PWM frequency for all channels (e.g. 50 for servos)."""
        prescale = round(25_000_000 / (4096 * freq_hz)) - 1
        mode = self._read(0x00)
        self._write(0x00, (mode & 0x7F) | 0x10)  # sleep to change prescale
        self._write(0xFE, prescale)
        self._write(0x00, mode & 0x7F)            # wake
        time.sleep_ms(5)
        self._write(0x00, mode | 0x80)            # restart

    def set_pwm(self, channel, on, off):
        """Set on/off counts (0–4095) for one channel."""
        reg = 0x06 + channel * 4
        self._i2c.writeto_mem(self._addr, reg, ustruct.pack('<HH', on, off))

    def _write(self, reg, val):
        self._i2c.writeto_mem(self._addr, reg, bytes([val]))

    def _read(self, reg):
        return self._i2c.readfrom_mem(self._addr, reg, 1)[0]


class ServoDriver:
    """Controls one servo on a single PCA9685 channel."""

    # Pulse width counts at 50 Hz (4096 steps per period = 20 ms)
    # Typical servo range: 1 ms (0°) to 2 ms (180°)
    MIN_PULSE = 150   # ~0° — adjust for your servo if needed
    MAX_PULSE = 600   # ~180°

    def __init__(self, pca, channel):
        self._pca = pca
        self._channel = channel

    def angle(self, degrees):
        """Move the servo to degrees (0–180)."""
        # TODO: clamp degrees to the range 0–180
        # TODO: map degrees linearly from MIN_PULSE to MAX_PULSE
        # TODO: call self._pca.set_pwm(self._channel, 0, pulse)
        pass

    def off(self):
        """Remove power from the servo (it goes limp)."""
        self._pca.set_pwm(self._channel, 0, 0)


# ── Setup ─────────────────────────────────────────────────────────────────
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
pca = PCA9685(i2c)
pca.set_freq(50)

servo0 = ServoDriver(pca, 0)
servo1 = ServoDriver(pca, 1)

# Once angle() works, test it:
servo0.angle(0)
time.sleep(1)
servo0.angle(90)
time.sleep(1)
servo0.angle(180)
