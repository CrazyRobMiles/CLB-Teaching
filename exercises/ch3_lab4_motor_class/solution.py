from machine import Pin, PWM


class MotorDriver:
    """Controls one DC motor via one channel of an L298N H-bridge."""

    def __init__(self, in1_pin, in2_pin, en_pin, freq=1000):
        self._in1 = Pin(in1_pin, Pin.OUT)
        self._in2 = Pin(in2_pin, Pin.OUT)
        self._pwm = PWM(Pin(en_pin))
        self._pwm.freq(freq)
        self.stop()

    def forward(self, speed=100):
        self._in1.value(1)
        self._in2.value(0)
        self._set_speed(speed)

    def backward(self, speed=100):
        self._in1.value(0)
        self._in2.value(1)
        self._set_speed(speed)

    def stop(self):
        self._in1.value(0)
        self._in2.value(0)
        self._set_speed(0)

    def brake(self):
        self._in1.value(1)
        self._in2.value(1)
        self._set_speed(100)

    def _set_speed(self, percent):
        self._pwm.duty_u16(int(percent * 65535 // 100))


# ── Test ────────────────────────────────────────────────────────────────────
motor_a = MotorDriver(2, 3, 6)
motor_b = MotorDriver(4, 5, 7)

motor_a.forward(50)
motor_b.backward(75)
