# Lab 4: Writing the Fade Program

To fade from colour A to colour B smoothly, loop from step 0 to STEPS, compute `t = step / STEPS`, and display `lerp_colour(A, B, t)` each pass.

```python copy
STEPS = 50    # how many frames per fade
DELAY = 0.02  # seconds between frames → 50 × 0.02 = 1 second per fade

for step in range(STEPS):
    t = step / STEPS        # t goes from 0.0 to ~1.0
    fill(lerp_colour(a, b, t))
    time.sleep(DELAY)
```

---

## The outer loop

The full program cycles through a list of colours, fading from each one to the next:

```python copy
COLOURS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

while True:
    for i in range(len(COLOURS)):
        a = COLOURS[i]
        b = COLOURS[(i + 1) % len(COLOURS)]
        for step in range(STEPS):
            t = step / STEPS
            fill(lerp_colour(a, b, t))
            time.sleep(DELAY)
```

`(i + 1) % len(COLOURS)` wraps the index so the last colour fades back into the first.

---

## Complete the skeleton

The skeleton in the editor has `lerp_colour` and the structure ready. Fill in:

1. The body of `lerp_colour` (one return statement with three channels)
2. The inner `for step in range(STEPS)` loop inside the outer fade loop

**Save & Run** — the strip should fade smoothly through the four colours in a continuous cycle.

---

## Experiment

**Faster/slower:** Change `STEPS` or `DELAY`. `STEPS = 20` and `DELAY = 0.02` fades in 0.4 s; `STEPS = 100` and `DELAY = 0.03` takes 3 s.

**More colours:** Add extra entries to `COLOURS`. The fade sequence grows automatically.

**Per-pixel lerp:** Instead of `fill()`, lerp each pixel separately — give pixel 0 `t=0.0` and pixel 7 `t=1.0` — to display the fade as a gradient across the strip at once.

---

## The problem with sleep

This program works, but it is completely unresponsive while fading. Try adding a button check anywhere in the inner loop — the button only responds once per fade step (every 20 ms), but the whole program is locked in the `time.sleep` during that delay. For a button-driven colour changer, this is frustrating.

In Lab 5 you will replace `time.sleep` with a non-blocking approach that can check the button on every pass through the main loop.
