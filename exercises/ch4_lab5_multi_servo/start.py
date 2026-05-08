from machine import I2C, Pin
import ustruct
import time


class PCA9685:
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
    MIN_PULSE = 150
    MAX_PULSE = 600

    def __init__(self, pca, channel):
        self._pca     = pca
        self._channel = channel
        self._degrees = 90
        self.angle(90)

    def angle(self, degrees):
        degrees = max(0, min(180, degrees))
        self._degrees = degrees
        pulse = self.MIN_PULSE + int((self.MAX_PULSE - self.MIN_PULSE) * degrees / 180)
        self._pca.set_pwm(self._channel, 0, pulse)

    def nudge(self, delta):
        """Move by delta degrees from current position."""
        # TODO: call self.angle() with the new position
        pass

    def off(self):
        self._pca.set_pwm(self._channel, 0, 0)


# ── Setup ─────────────────────────────────────────────────────────────────
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
pca = PCA9685(i2c)
pca.set_freq(50)

# Four servos on channels 0–3, all starting at 90°
servos = [ServoDriver(pca, i) for i in range(4)]
active = 0   # which servo the buttons currently control

btn_prev  = Pin(14, Pin.IN, Pin.PULL_UP)   # select previous servo
btn_next  = Pin(13, Pin.IN, Pin.PULL_UP)   # select next servo
btn_ccw   = Pin(12, Pin.IN, Pin.PULL_UP)   # rotate −5°
btn_cw    = Pin(11, Pin.IN, Pin.PULL_UP)   # rotate +5°

last = [1, 1, 1, 1]

print(f"Controlling servo {active}")

while True:
    btns = [btn_prev.value(), btn_next.value(), btn_ccw.value(), btn_cw.value()]

    # TODO: falling edge on btn_prev  → decrement active (with wrap)
    # TODO: falling edge on btn_next  → increment active (with wrap)
    # TODO: falling edge on btn_ccw   → servos[active].nudge(-5)
    # TODO: falling edge on btn_cw    → servos[active].nudge(+5)
    # After each change, print the active servo number and its current angle

    last = btns
    time.sleep(0.02)
