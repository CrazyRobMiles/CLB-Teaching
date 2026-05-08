from machine import Pin
import time

# Use the LED from Chapter 1 (GP15 via 220 Ω resistor)
led = Pin(15, Pin.OUT)

FREQ = 100   # Hz  — how many on/off cycles per second
DUTY = 50    # %   — percentage of each cycle the LED is on

# TODO: calculate the period (1 / FREQ) and the on/off times from DUTY
period  = None
on_time = None
off_time = None

while True:
    # TODO: turn LED on, sleep on_time, turn LED off, sleep off_time
    pass
