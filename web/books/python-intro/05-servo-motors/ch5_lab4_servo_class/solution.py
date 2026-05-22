from machine import I2C, Pin
import ustruct
import time


class PCA9685:
    """I2C driver for the PCA9685 16-channel PWM controller."""

    def __init__(self, i2c, address=0x40):
        self._i2c = i2c
        self._addr = address
        self._write(0x00, 0x20)

    def set_freq(self, freq_hz):
        prescale = round(25_000_000 / (4096 * freq_hz)) - 1
        mode = self._read(0x00)
        self._write(0x00, (mode & 0x7F) | 0x10)
        self._write(0xFE, prescale)
        self._write(0x00, mode & 0x7F)
        time.sleep_ms(5)
        self._write(0x00, mode | 0x80)

    def set_pwm(self, channel, on, off):
        reg = 0x06 + channel * 4
        self._i2c.writeto_mem(self._addr, reg, ustruct.pack('<HH', on, off))

    def _write(self, reg, val):
        self._i2c.writeto_mem(self._addr, reg, bytes([val]))

    def _read(self, reg):
        return self._i2c.readfrom_mem(self._addr, reg, 1)[0]


class ServoDriver:
    """Controls one servo on a single PCA9685 channel."""

    MIN_PULSE = 150
    MAX_PULSE = 600

    def __init__(self, pca, channel):
        self._pca     = pca
        self._channel = channel
        self._degrees = 90

    def angle(self, degrees):
        degrees = max(0, min(180, degrees))
        self._degrees = degrees
        pulse = self.MIN_PULSE + int((self.MAX_PULSE - self.MIN_PULSE) * degrees / 180)
        self._pca.set_pwm(self._channel, 0, pulse)

    def off(self):
        self._pca.set_pwm(self._channel, 0, 0)


# ── Demo ──────────────────────────────────────────────────────────────────
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
pca = PCA9685(i2c)
pca.set_freq(50)

servo0 = ServoDriver(pca, 0)
servo1 = ServoDriver(pca, 1)

servo0.angle(0)
time.sleep(1)
servo0.angle(90)
time.sleep(1)
servo0.angle(180)
time.sleep(1)
servo1.angle(45)
