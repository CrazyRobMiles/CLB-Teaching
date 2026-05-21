# Lab 5: Completing the Program

The skeleton has `lerp_colour`, `fill`, the ANIMATIONS registry, and the main loop already written. You need to implement the two generator bodies.

---

## fade_loop

```python copy
def fade_loop(colours, steps=60):
    n = len(colours)
    pair = 0
    step = 0
    while True:
        a = colours[pair]
        b = colours[(pair + 1) % n]
        # TODO: call fill(lerp_colour(a, b, step / steps))
        # TODO: increment step; when step > steps, reset to 0 and advance pair
        yield
```

The `pair` and `step` variables track where in the fade sequence we are. `step` counts from 0 to `steps` for each colour transition; `pair` indexes the colour list.

---

## solid_pulse

```python copy
def solid_pulse(colour, steps=30):
    step = 0
    direction = 1
    while True:
        brightness = step / steps
        # TODO: scale each channel: int(colour[0] * brightness), etc.
        # TODO: call fill() with the scaled colour
        # TODO: advance step by direction; reverse direction when step hits 0 or steps
        yield
```

`direction` alternates between +1 (brightening) and −1 (dimming). When `step` reaches `steps` or 0, flip the sign.

---

## Save & Run

**Save & Run** — the strip should start fading through colours. Pressing the button should switch to the pulsing animation instantly, with no delay.

---

## The solution adds a third animation

The solution file includes a `rainbow_chase` generator that shifts a rainbow pattern along the strip one pixel per frame. Once your two generators work, look at the solution to see how it is structured — it follows exactly the same pattern.

---

## What you've built

This is the core architecture of real-time embedded software:

- **Separate state from timing** — each animation owns its state; the main loop owns timing
- **Single main loop** — all inputs and outputs share one loop; nothing blocks
- **Composable** — adding a new animation means adding one function and one entry in ANIMATIONS; the rest is unchanged

In Chapter 3 you'll see the Connected Little Boxes framework, which takes this idea further: animations, inputs, and outputs become independent *managers*, connected by events — so they don't even need to share the same loop.
