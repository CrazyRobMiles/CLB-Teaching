from machine import Pin, PWM
import time

# Wrap the LED pin in a PWM object — the Pico hardware takes over the toggling
led = PWM(Pin(15))

# TODO: set the PWM frequency to 1000 Hz
# TODO: set the duty cycle to 50%
#       Hint: duty_u16() takes a value from 0 (off) to 65535 (full on)
#             50% = 32768
