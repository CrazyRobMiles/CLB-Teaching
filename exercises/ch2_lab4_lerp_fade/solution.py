import machine
import neopixel
import time

NUM_PIXELS = 8
pin = machine.Pin(15, machine.Pin.OUT)
np = neopixel.NeoPixel(pin, NUM_PIXELS)

def lerp_colour(a, b, t):
    return (
        int(a[0] + (b[0] - a[0]) * t),
        int(a[1] + (b[1] - a[1]) * t),
        int(a[2] + (b[2] - a[2]) * t),
    )

def fill(colour):
    for i in range(NUM_PIXELS):
        np[i] = colour
    np.write()

COLOURS = [
    (255,   0,   0),
    (  0, 255,   0),
    (  0,   0, 255),
    (255, 255,   0),
]

STEPS = 50
DELAY = 0.02

while True:
    for i in range(len(COLOURS)):
        a = COLOURS[i]
        b = COLOURS[(i + 1) % len(COLOURS)]
        for step in range(STEPS):
            t = step / STEPS
            fill(lerp_colour(a, b, t))
            time.sleep(DELAY)
