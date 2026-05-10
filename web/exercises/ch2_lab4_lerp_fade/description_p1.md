# Lab 4: Lerp Fade

In Lab 3 the palette changed instantly — one call to `show_palette` replaced all the colours in one frame. In this lab you'll create a *smooth* transition by interpolating between colours one step at a time.

---

## Linear interpolation (lerp)

**Linear interpolation** — usually shortened to **lerp** — calculates a value that is a fraction of the way between two values.

```
lerp(a, b, t) = a + (b - a) × t
```

When `t = 0` the result is `a`; when `t = 1` the result is `b`; when `t = 0.5` the result is exactly halfway.

```
a = 0,  b = 100,  t = 0.25  →  result = 25
a = 0,  b = 100,  t = 0.75  →  result = 75
```

---

## Lerping colours

Apply the formula to each RGB channel independently:

```python
def lerp_colour(a, b, t):
    return (
        int(a[0] + (b[0] - a[0]) * t),
        int(a[1] + (b[1] - a[1]) * t),
        int(a[2] + (b[2] - a[2]) * t),
    )
```

`int(...)` rounds the result down to a whole number, since pixel channels must be integers 0–255.

---

## Testing lerp in the console

Before writing a program, verify your `lerp_colour` works:

```python
def lerp_colour(a, b, t):
    return (
        int(a[0] + (b[0] - a[0]) * t),
        int(a[1] + (b[1] - a[1]) * t),
        int(a[2] + (b[2] - a[2]) * t),
    )

lerp_colour((255, 0, 0), (0, 0, 255), 0.0)   # should give (255, 0, 0)
lerp_colour((255, 0, 0), (0, 0, 255), 0.5)   # should give (127, 0, 127)
lerp_colour((255, 0, 0), (0, 0, 255), 1.0)   # should give (0, 0, 255)
```
