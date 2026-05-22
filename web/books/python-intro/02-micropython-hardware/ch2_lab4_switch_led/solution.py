import machine
import time

led = machine.Pin(15, machine.Pin.OUT)
switch = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    if switch.value() == 0:    # button pressed — pin pulled to GND
        led.on()
    else:                       # button released — pin pulled high
        led.off()
    time.sleep(0.01)
