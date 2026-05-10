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


motor = MotorDriver(2, 3, 6)

btn_speed = Pin(14, Pin.IN, Pin.PULL_UP)   # press to cycle speed: 25→50→75→100→25…
btn_dir   = Pin(13, Pin.IN, Pin.PULL_UP)   # press to flip direction

SPEEDS    = [25, 50, 75, 100]
speed_idx = 0
forward   = True

last_speed = 1
last_dir   = 1

# Start moving
motor.forward(SPEEDS[speed_idx])

while True:
    s = btn_speed.value()
    d = btn_dir.value()

    # TODO: detect falling edge on btn_speed → advance speed_idx with modulo
    #       then re-apply motor direction at the new speed

    # TODO: detect falling edge on btn_dir → toggle forward flag
    #       then call motor.forward() or motor.backward() accordingly

    last_speed = s
    last_dir   = d
    time.sleep(0.02)
