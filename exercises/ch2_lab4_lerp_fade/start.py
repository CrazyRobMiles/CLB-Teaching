import machine
import neopixel
import time

NUM_PIXELS = 8
pin = machine.Pin(15, machine.Pin.OUT)
np = neopixel.NeoPixel(pin, NUM_PIXELS)

def lerp_colour(a, b, t):
    # t is a float from 0.0 to 1.0.
    # When t=0, return colour a. When t=1, return colour b.
    # Interpolate each channel (R, G, B) separately and return as a tuple of ints.
    # TODO: implement this function
    pass

def fill(colour):
    for i in range(NUM_PIXELS):
        np[i] = colour
    np.write()

COLOURS = [
    (255,   0,   0),   # red
    (  0, 255,   0),   # green
    (  0,   0, 255),   # blue
    (255, 255,   0),   # yellow
]

STEPS = 50    # steps per fade
DELAY = 0.02  # seconds per step  → total fade = STEPS × DELAY = 1 second

while True:
    for i in range(len(COLOURS)):
        a = COLOURS[i]
        b = COLOURS[(i + 1) % len(COLOURS)]
        # TODO: fade from a to b in STEPS steps
        # Hint: loop from 0 to STEPS, compute t = step / STEPS,
        #       call fill(lerp_colour(a, b, t)), then time.sleep(DELAY)
        pass
