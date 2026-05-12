# Lab 1: Using the neopixel Library

MicroPython includes a `neopixel` module built in — no installation needed. Type these commands in the **Console**.

---

## Set up the strip

```python
import machine
import neopixel

pin = machine.Pin(15, machine.Pin.OUT)
np = neopixel.NeoPixel(pin, 8)
```

`NeoPixel(pin, n)` creates a strip object for `n` pixels on the given pin. The pixels all start off (black).

---

## Set individual pixels

Pixels are addressed from `0` (nearest to the Pico) to `n-1`. Assign a colour as an `(r, g, b)` tuple:

```python
np[0] = (255, 0, 0)    # first pixel: red
np[1] = (0, 255, 0)    # second pixel: green
np[2] = (0, 0, 255)    # third pixel: blue
```

**Nothing happens on the strip yet.** Setting `np[i]` only updates the buffer in memory.

---

## Send the colours to the hardware

```python
np.write()
```

`write()` transmits the entire buffer to the strip in one operation. Always call it after making changes.

---

## Fill the whole strip

To set every pixel to the same colour, loop over all indices:

```python
for i in range(len(np)):
    np[i] = (255, 100, 0)    # amber
np.write()
```

`len(np)` gives the number of pixels (8 in our case).

---

## Turn everything off

```python
for i in range(len(np)):
    np[i] = (0, 0, 0)
np.write()
```

Setting a pixel to `(0, 0, 0)` means no light — full off.

---

## Experiment

Try mixing colours by hand. What does `(255, 255, 255)` look like? What about `(255, 0, 255)`?
