# Lab 2: Writing the Program

The skeleton in the editor has the setup code ready. Your job is to fill in the `colours` list and write the loop.

---

## What to write

1. Add 8 colour tuples to the `colours` list — one for each pixel.
2. Write a `for` loop that assigns `colours[i]` to `np[i]` for each pixel.
3. Call `np.write()` after the loop.

**Save & Run** — the strip should light up with a different colour on each pixel.

---

## enumerate — a cleaner loop

Python's `enumerate()` gives you both the index and the value at once:

```python copy
for i, colour in enumerate(colours):
    np[i] = colour
```

This is equivalent to the `range(NUM_PIXELS)` version but reads more clearly.

---

## Experiment

**Try dim versions:** Replace `255` with `50` across all your colours. The hues are the same but the brightness is much more comfortable.

**Try a gradient:** Instead of picked colours, calculate them:

```python copy
for i in range(NUM_PIXELS):
    # ramp red up from 0 to 255 across the strip
    r = int(255 * i / (NUM_PIXELS - 1))
    np[i] = (r, 0, 0)
np.write()
```

**Try a warm-to-cool transition:**
```python
(255, 0, 0) → (255, 50, 0) → ... → (0, 0, 255)
```

In the next lab you'll define several palettes and use a button to switch between them.
