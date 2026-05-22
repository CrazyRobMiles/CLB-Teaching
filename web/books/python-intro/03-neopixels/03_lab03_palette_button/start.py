import machine
import neopixel
import time

NUM_PIXELS = 8
pin = machine.Pin(15, machine.Pin.OUT)
np = neopixel.NeoPixel(pin, NUM_PIXELS)
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

# Define palettes — each palette is a list of (r, g, b) tuples.
# You need at least 8 colours per palette (one per pixel).
PALETTES = [
    # TODO: add two or more palettes here
]

current_palette = 0

def show_palette(index):
    # TODO: assign each pixel a colour from PALETTES[index]
    # Hint: use i % len(palette) to wrap if the palette is shorter than NUM_PIXELS
    pass

show_palette(current_palette)

last_btn = 1
while True:
    btn = button.value()
    # TODO: detect a button press (falling edge: last_btn was 1, btn is now 0)
    #       and advance to the next palette
    last_btn = btn
    time.sleep(0.02)
