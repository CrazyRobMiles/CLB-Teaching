import machine
import neopixel

NUM_PIXELS = 8
pin = machine.Pin(15, machine.Pin.OUT)
np = neopixel.NeoPixel(pin, NUM_PIXELS)

colours = [
    (255,   0,   0),   # red
    (255, 127,   0),   # orange
    (255, 255,   0),   # yellow
    (  0, 255,   0),   # green
    (  0, 255, 127),   # spring green
    (  0, 127, 255),   # sky blue
    (  0,   0, 255),   # blue
    (127,   0, 255),   # violet
]

for i in range(NUM_PIXELS):
    np[i] = colours[i]
np.write()
