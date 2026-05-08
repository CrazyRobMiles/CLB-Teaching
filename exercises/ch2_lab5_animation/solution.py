import machine
import neopixel
import time

NUM_PIXELS = 8
pin = machine.Pin(15, machine.Pin.OUT)
np = neopixel.NeoPixel(pin, NUM_PIXELS)
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)


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


# ── Animation generators ───────────────────────────────────────────────────

def fade_loop(colours, steps=60):
    """Fade continuously between each pair of colours in the list."""
    n = len(colours)
    pair = 0
    step = 0
    while True:
        a = colours[pair]
        b = colours[(pair + 1) % n]
        fill(lerp_colour(a, b, step / steps))
        step += 1
        if step > steps:
            step = 0
            pair = (pair + 1) % n
        yield


def solid_pulse(colour, steps=30):
    """Pulse a single colour from off to full brightness and back."""
    step = 0
    direction = 1
    while True:
        brightness = step / steps
        c = (int(colour[0] * brightness),
             int(colour[1] * brightness),
             int(colour[2] * brightness))
        fill(c)
        step += direction
        if step >= steps or step <= 0:
            direction = -direction
        yield


def rainbow_chase():
    """Chase a rainbow pattern along the strip one pixel at a time."""
    colours = [
        (255,   0,   0), (255, 127,   0), (255, 255,   0), (  0, 255,   0),
        (  0, 127, 255), (  0,   0, 255), (127,   0, 255), (255,   0, 127),
    ]
    offset = 0
    while True:
        for i in range(NUM_PIXELS):
            np[i] = colours[(i + offset) % len(colours)]
        np.write()
        offset += 1
        yield


# ── Animation registry ─────────────────────────────────────────────────────

ANIMATIONS = [
    lambda: fade_loop([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]),
    lambda: solid_pulse((0, 100, 255)),
    lambda: rainbow_chase(),
]

current_anim = 0
animation = ANIMATIONS[current_anim]()

last_btn = 1

# ── Main loop ──────────────────────────────────────────────────────────────

while True:
    next(animation)

    btn = button.value()
    if last_btn == 1 and btn == 0:   # falling edge — button just pressed
        current_anim = (current_anim + 1) % len(ANIMATIONS)
        animation = ANIMATIONS[current_anim]()
    last_btn = btn

    time.sleep(0.016)
