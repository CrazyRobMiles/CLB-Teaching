from machine import Pin, PWM
import time


class MotorDriver:
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


def apply(motor, forward, speed):
    if forward:
        motor.forward(speed)
    else:
        motor.backward(speed)


motor = MotorDriver(2, 3, 6)

btn_speed = Pin(14, Pin.IN, Pin.PULL_UP)
btn_dir   = Pin(13, Pin.IN, Pin.PULL_UP)

SPEEDS    = [25, 50, 75, 100]
speed_idx = 0
forward   = True

last_speed = 1
last_dir   = 1

apply(motor, forward, SPEEDS[speed_idx])

while True:
    s = btn_speed.value()
    d = btn_dir.value()

    if last_speed == 1 and s == 0:
        speed_idx = (speed_idx + 1) % len(SPEEDS)
        apply(motor, forward, SPEEDS[speed_idx])
        print(f"Speed: {SPEEDS[speed_idx]}%")

    if last_dir == 1 and d == 0:
        forward = not forward
        apply(motor, forward, SPEEDS[speed_idx])
        print("Forward" if forward else "Backward")

    last_speed = s
    last_dir   = d
    time.sleep(0.02)
