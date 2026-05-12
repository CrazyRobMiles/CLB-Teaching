# Lab 5: Python Generators

The key to non-blocking animation in this lab is the Python **generator** — a function that can pause in the middle and resume from the same point on the next call.

---

## yield

A generator function contains `yield`. When Python reaches `yield`, it pauses the function and returns to the caller. The next time `next()` is called on the generator, it continues from just after the `yield`.

```python
def counter():
    i = 0
    while True:
        yield i
        i += 1

gen = counter()
next(gen)   # returns 0
next(gen)   # returns 1
next(gen)   # returns 2
```

**All local variables persist** between calls. `i` keeps incrementing because the generator remembers its entire state.

---

## Generators for animation

An animation generator does one frame of work, then yields:

```python
def fade_loop(colours, steps=60):
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
        yield    # ← pause here; resume next time next() is called
```

Each call to `next(animation)` advances one frame. The animation state — `pair` and `step` — lives inside the generator and persists automatically.

---

## The animation registry

To switch animations cleanly, store each animation type as a **lambda** that creates a fresh generator when called:

```python
ANIMATIONS = [
    lambda: fade_loop([(255, 0, 0), (0, 255, 0), (0, 0, 255)]),
    lambda: solid_pulse((0, 100, 255)),
]
```

To switch: `animation = ANIMATIONS[current_anim]()` — calling the lambda creates a new generator, starting the animation from scratch.

---

## The main loop

```python
while True:
    next(animation)       # one animation frame

    btn = button.value()
    if last_btn == 1 and btn == 0:
        current_anim = (current_anim + 1) % len(ANIMATIONS)
        animation = ANIMATIONS[current_anim]()
    last_btn = btn

    time.sleep(0.016)     # ~60 fps
```

The button is checked on every single pass — never blocked by the animation.
