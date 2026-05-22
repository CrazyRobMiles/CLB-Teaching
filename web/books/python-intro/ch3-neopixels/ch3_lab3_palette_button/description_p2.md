# Lab 3: Button Edge Detection

Adding a button to cycle palettes requires care. Simply checking `button.value() == 0` fires on every pass through the loop while the button is held — that's 50 times per second. You only want it to fire *once* when the button is first pressed.

---

## Edge detection

The technique is to compare the current button state with the *previous* state:

```python copy
last_btn = 1          # assume not pressed at start
while True:
    btn = button.value()
    if last_btn == 1 and btn == 0:   # just went from high to low
        # button was just pressed — act once
        ...
    last_btn = btn    # remember state for next pass
    time.sleep(0.02)
```

`last_btn == 1 and btn == 0` is called a **falling edge** (the signal fell from high to low). It is only true for exactly one pass through the loop.

---

## The complete program

The skeleton in the editor has the structure ready. You need to:

1. Fill in the `PALETTES` list with at least two palettes (8 colours each)
2. Implement `show_palette` to assign colours and call `np.write()`
3. Detect the falling edge in the loop and call `show_palette` with the new index

**Save & Run** — each press of the button should cycle to the next palette.

---

## Experiment

**Different palette lengths:** Try a palette with only 4 colours. Because `show_palette` uses `i % len(palette)`, it tiles: pixels 0–3 and 4–7 show the same four colours.

**Brightness:** Reduce all values by half (e.g. `(128, 0, 0)` instead of `(255, 0, 0)`) for a softer look.

**More palettes:** The solution has four palettes — Fire, Ocean, Forest, Sunset. Add your own.

In Lab 4 you'll learn how to smoothly fade between colours instead of jumping abruptly from one to another.
