from machine import Pin, PWM
import time

led = PWM(Pin(15))
led.freq(1000)

# Fade smoothly up then down, forever — impossible with software PWM
# because the CPU would be spending all its time in sleep() calls.
while True:
    for duty in range(0, 65536, 512):
        led.duty_u16(duty)
        time.sleep_ms(8)
    for duty in range(65535, -1, -512):
        led.duty_u16(duty)
        time.sleep_ms(8)
