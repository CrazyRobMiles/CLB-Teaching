import machine
import neopixel
import time

NUM_PIXELS = 8
pin = machine.Pin(15, machine.Pin.OUT)
np = neopixel.NeoPixel(pin, NUM_PIXELS)
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

PALETTES = [
    # Warm fire
    [(255,   0,   0), (255,  60,   0), (255, 120,   0), (255, 180,   0),
     (255, 120,   0), (255,  60,   0), (200,  20,   0), (150,   0,   0)],
    # Ocean
    [(  0,   0, 255), (  0,  50, 200), (  0, 100, 180), (  0, 180, 200),
     (  0, 200, 180), (  0, 150, 200), (  0,  80, 255), (  0,   0, 200)],
    # Forest
    [(  0, 100,   0), (  0, 180,   0), ( 50, 200,  50), (100, 255,   0),
     (  0, 200,  50), (  0, 150,  80), (  0, 100,  50), (  0,  80,   0)],
    # Sunset
    [(255,   0, 100), (255,  50,   0), (255, 150,   0), (200,   0, 100),
     (150,   0, 150), (255, 100,   0), (200,  50,  50), (100,   0, 200)],
]

current_palette = 0

def show_palette(index):
    palette = PALETTES[index]
    for i in range(NUM_PIXELS):
        np[i] = palette[i % len(palette)]
    np.write()

show_palette(current_palette)

last_btn = 1
while True:
    btn = button.value()
    if last_btn == 1 and btn == 0:   # falling edge — button just pressed
        current_palette = (current_palette + 1) % len(PALETTES)
        show_palette(current_palette)
    last_btn = btn
    time.sleep(0.02)
