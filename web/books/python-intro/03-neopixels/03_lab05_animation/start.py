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
# Each function is a generator: it contains a while True loop that does one
# step of animation then YIELDS — pausing until next() calls it again.

def fade_loop(colours, steps=60):
    """Fade continuously between each pair of colours in the list."""
    n = len(colours)
    pair = 0
    step = 0
    while True:
        a = colours[pair]
        b = colours[(pair + 1) % n]
        # TODO: fill the strip with lerp_colour(a, b, step / steps)
        # TODO: advance step; when step > steps, reset to 0 and advance pair
        yield


def solid_pulse(colour, steps=30):
    """Pulse a single colour from off to full brightness and back."""
    step = 0
    direction = 1
    while True:
        brightness = step / steps
        # TODO: scale each channel of colour by brightness and call fill()
        # TODO: advance step by direction; reverse direction at 0 and steps
        yield


# ── Animation registry ─────────────────────────────────────────────────────
# Each entry is a lambda that creates a fresh generator when called.

ANIMATIONS = [
    lambda: fade_loop([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]),
    lambda: solid_pulse((0, 100, 255)),
]

current_anim = 0
animation = ANIMATIONS[current_anim]()

last_btn = 1

# ── Main loop ──────────────────────────────────────────────────────────────

while True:
    next(animation)          # advance animation one step

    btn = button.value()
    # TODO: detect a falling edge and switch to the next animation
    #       Hint: animation = ANIMATIONS[current_anim]()  creates a fresh one
    last_btn = btn

    time.sleep(0.016)        # ~60 updates per second
