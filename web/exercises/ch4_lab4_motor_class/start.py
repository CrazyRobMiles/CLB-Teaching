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
        """Run forward at speed (0–100%)."""
        # TODO: set IN1 high and IN2 low, then call _set_speed(speed)
        pass

    def backward(self, speed=100):
        """Run backward at speed (0–100%)."""
        # TODO: set IN1 low and IN2 high, then call _set_speed(speed)
        pass

    def stop(self):
        """Coast to a stop — motor terminals left floating."""
        # TODO: set both direction pins low, speed to 0
        pass

    def brake(self):
        """Active brake — short-circuits the motor terminals for a fast stop."""
        # TODO: set both direction pins high, speed to 100
        pass

    def _set_speed(self, percent):
        """Map 0–100% to a 16-bit duty cycle value."""
        # TODO: call self._pwm.duty_u16() with the correct value
        # Hint: duty_u16 range 0–65535; use integer division to avoid rounding drift
        pass


# ── Test ────────────────────────────────────────────────────────────────────
# Wiring:  Motor A: IN1=GP2, IN2=GP3, ENA=GP6
#          Motor B: IN3=GP4, IN4=GP5, ENB=GP7

motor_a = MotorDriver(2, 3, 6)
motor_b = MotorDriver(4, 5, 7)

motor_a.forward(50)
motor_b.backward(75)
