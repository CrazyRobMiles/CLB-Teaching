# Lab 2: Colour Range

In Lab 1 you set pixels one at a time from the console. In this lab you'll write a program that assigns a different colour to every pixel, showing the range of colours a NeoPixel strip can display.

---

## The plan

You'll define a list of eight colours — one per pixel — spread across the visible spectrum, then loop through the list and assign each colour to its pixel. One call to `np.write()` at the end sends everything to the hardware.

```
colours = [(r, g, b), (r, g, b), ...]   ← one entry per pixel
for i in range(NUM_PIXELS):
    np[i] = colours[i]
np.write()
```

---

## NUM_PIXELS as a constant

Instead of writing `8` everywhere, define it once at the top:

```python
NUM_PIXELS = 8
```

Then use `NUM_PIXELS` wherever you need the length. If you ever change the strand length, you only have one place to update.

---

## Choosing colours

Try to spread across the spectrum. A good starting set:

- Red `(255, 0, 0)`
- Orange `(255, 127, 0)`
- Yellow `(255, 255, 0)`
- Green `(0, 255, 0)`
- Spring green `(0, 255, 127)`
- Sky blue `(0, 127, 255)`
- Blue `(0, 0, 255)`
- Violet `(127, 0, 255)`

You don't have to use these — experiment with your own choices.
