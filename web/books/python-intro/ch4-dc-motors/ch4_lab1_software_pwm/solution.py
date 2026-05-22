from machine import Pin
import time

led = Pin(15, Pin.OUT)

FREQ = 100
DUTY = 50

period   = 1.0 / FREQ
on_time  = period * DUTY / 100
off_time = period - on_time

while True:
    led.value(1)
    time.sleep(on_time)
    led.value(0)
    time.sleep(off_time)
