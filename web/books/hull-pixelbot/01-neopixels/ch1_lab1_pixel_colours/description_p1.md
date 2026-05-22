# Lab 1: Pixel Colours

The Hull Pixelbot has a strip of **NeoPixels** — individually addressable RGB LEDs that you can set to any colour. Each pixel contains a tiny red, green, and blue LED element. Mix those three channels (each from 0 to 255) and you can make any colour in the spectrum.

The robot library gives you named colour constants and a single `colour()` function to set them.

---

## Setting up the library

Copy the following files from the CLB-robot repository onto your Pico:

```
robot.py
config.py
lib/stepper.py
lib/distance.py
lib/pixels.py
```

Open `config.py` and check that `PIXEL_PIN` and `PIXEL_COUNT` match your robot's wiring. The defaults are correct for a standard Hull Pixelbot build.

At the top of every program you write, import the library and call `robot.init()`:

```python
import time
import robot

robot.init()
```

`robot.init()` reads the hardware settings from `config.py` and prepares the pixel strip, stepper motors, and distance sensor.

---

## Colour constants

The robot library defines eight colour constants that match the colours available in PythonIsh:

```python
robot.RED
robot.GREEN
robot.BLUE
robot.CYAN
robot.MAGENTA
robot.YELLOW
robot.WHITE
robot.BLACK
```

Each constant is an RGB tuple — for example `robot.RED` is `(255, 0, 0)`. You pass a constant to `robot.colour()` to light the pixels:

```python
robot.colour(robot.RED)
time.sleep(1)
robot.colour(robot.GREEN)
time.sleep(1)
robot.colour(robot.BLACK)   # off
```

You can also write a colour as a plain tuple if you want a shade that does not have a name:

```python
robot.colour((255, 128, 0))   # orange
robot.colour((128, 0, 128))   # purple
```
