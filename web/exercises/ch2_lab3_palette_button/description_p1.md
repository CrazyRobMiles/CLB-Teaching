# Lab 3: Palette and Button

A **palette** is a pre-selected set of colours that work well together — like a painter's palette. In this lab you'll define several palettes and display them on the strip, then add a button that cycles through them.

---

## Palettes as a data structure

A palette is a list of `(r, g, b)` tuples. A collection of palettes is a list of lists:

```python
PALETTES = [
    # Warm fire
    [(255, 0, 0), (255, 60, 0), (255, 120, 0), (255, 180, 0),
     (255, 120, 0), (255, 60, 0), (200, 20, 0), (150, 0, 0)],
    # Ocean
    [(0, 0, 255), (0, 50, 200), (0, 100, 180), (0, 180, 200),
     (0, 200, 180), (0, 150, 200), (0, 80, 255), (0, 0, 200)],
]
```

To display palette number `i`, you write `PALETTES[i]` to the strip.

---

## show_palette function

Wrapping the display logic in a function keeps the main loop clean:

```python
def show_palette(index):
    palette = PALETTES[index]
    for i in range(NUM_PIXELS):
        np[i] = palette[i % len(palette)]
    np.write()
```

`i % len(palette)` wraps the index so shorter palettes tile across the strip — useful if you define palettes with fewer than 8 colours.

---

## Cycling with modulo

To advance through the palette list and wrap back to the start:

```python
current_palette = (current_palette + 1) % len(PALETTES)
```

When `current_palette` reaches `len(PALETTES)`, modulo resets it to `0`.
