import machine
import neopixel

NUM_PIXELS = 8
pin = machine.Pin(15, machine.Pin.OUT)
np = neopixel.NeoPixel(pin, NUM_PIXELS)

# Define a list of colours — one for each pixel.
# Each colour is a tuple: (red, green, blue), values 0–255.
colours = [
    # TODO: add 8 colours here — try to spread across the colour spectrum
]

# TODO: assign each colour to its pixel using np[i] = colours[i]
# TODO: call np.write() to send the colours to the LEDs
