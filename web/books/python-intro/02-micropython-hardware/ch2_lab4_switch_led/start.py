import machine
import time

# LED on GP15 (physical pin 20)
led = machine.Pin(15, machine.Pin.OUT)

# Switch on GP14 (physical pin 19), with pull-up enabled.
# Pull-up means: value() returns 1 when the button is NOT pressed,
# and 0 when it IS pressed (because pressing connects the pin to GND).
switch = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    # TODO: read the switch and control the LED
    # Hint: if switch.value() == 0, the button is pressed
    pass
