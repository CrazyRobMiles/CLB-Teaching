# Lab 1: Colour

## RGB colour

Each pixel has three channels: **red**, **green**, and **blue**, each 0–255. You control them independently:

| Colour | R | G | B |
|--------|---|---|---|
| Red | 255 | 0 | 0 |
| Green | 0 | 255 | 0 |
| Blue | 0 | 0 | 255 |
| Yellow | 255 | 255 | 0 |
| Cyan | 0 | 255 | 255 |
| Magenta | 255 | 0 | 255 |
| White | 255 | 255 | 255 |
| Off | 0 | 0 | 0 |
| Orange | 255 | 100 | 0 |
| Dim red | 40 | 0 | 0 |

---

## 24-bit colour

With 256 levels per channel and three channels, a NeoPixel can display **256 × 256 × 256 = 16,777,216** distinct colours. This is called 24-bit colour — the same as a modern computer screen.

In practice you won't notice the difference beyond about 6 million colours, which is roughly the limit of the human eye. But it does mean you have very fine-grained control over exactly what shade you produce.

---

## Colour gamut

NeoPixels are **emissive** — they produce light rather than reflecting it. This gives them a wide gamut: they can produce pure, saturated colours (vivid reds, deep blues) that ink or paint cannot reproduce, because ink mixes by subtracting light while pixels add it.

The tradeoff: they cannot produce pastels or soft neutrals easily. `(255, 200, 200)` looks washed-out pink on a screen but can appear too bright and blue in a darkened room. In practice you often reduce brightness significantly — try `(40, 0, 0)` instead of `(255, 0, 0)` for a comfortable red.

---

## Brightness and current

At full white `(255, 255, 255)`, each NeoPixel draws about 60 mA. Eight pixels at full white would draw 480 mA — well above what the Pico's 3V3 pin can supply. Keep brightness moderate (values of 50–150 per channel) when running from 3V3, and the strip will stay well within safe limits.

---

## Try from the console

```python
np[0] = (0, 40, 80)    # a steel blue
np[1] = (80, 40, 0)    # a warm amber
np[2] = (0, 80, 0)     # a forest green
np.write()
```

In the next lab you'll write a program that assigns a different colour to every pixel.
