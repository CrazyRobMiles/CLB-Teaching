# Lab 5: Non-Blocking Animation

In Lab 4 the fade program used `time.sleep` to pace the animation. This works, but it **blocks** — while the program is sleeping, it cannot do anything else: check buttons, respond to inputs, or update a display.

---

## The problem with blocking code

Imagine you want the LED to fade *and* respond to a button at the same time. With sleep, you might try:

```python copy
while True:
    for step in range(STEPS):
        fill(lerp_colour(a, b, step / STEPS))
        time.sleep(DELAY)
        if button.value() == 0:   # check button inside the inner loop
            change_animation()
```

This is awkward. The button is only checked once per animation step, and the step delay makes it feel unresponsive. Add more features and the problem compounds.

The root cause: the loop structure and the animation state are tangled together. We need to *separate* the animation state from the main loop.

---

## A non-blocking approach

The idea is to restructure the animation as a function that does **one step at a time** and remembers where it left off. The main loop calls it once per pass, then does everything else (check buttons, etc.) before calling it again.

```
main loop:
    advance animation by one step
    check button
    sleep a short time (e.g. 16 ms)
    repeat
```

The animation is no longer responsible for timing — it just advances when asked. The sleep in the main loop paces everything.

---

## This lab is larger than the previous ones

The complete solution is about 70 lines of code — the largest program in this chapter. Don't be put off by the size: it is made up of small, independent pieces. Read the skeleton carefully before you start writing. The structure is already there; your job is to fill in the generator bodies and the button logic.
