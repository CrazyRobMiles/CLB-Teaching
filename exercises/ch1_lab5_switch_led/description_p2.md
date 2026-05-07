# Lab 5: Writing the Program

The skeleton in the editor already imports `machine` and `time`, creates both pins, and gives you the `while True` loop. Fill in the body.

---

## What to write

Inside `while True:`, replace `pass` with:

```python
if switch.value() == 0:
    led.on()
else:
    led.off()
time.sleep(0.01)
```

**Save & Run** — pressing the button should turn the LED on immediately; releasing it should turn it off.

---

## Experiment

**Invert the logic** — make the LED turn on when the button is *not* pressed:

```python
if switch.value() == 1:
    led.on()
else:
    led.off()
```

Or more compactly, since `switch.value()` is already 0 or 1:

```python
led.value(switch.value())
```

(This works because the LED and switch use the same logic level — but note it gives you active-low LED too, which may feel odd.)

**Add a blink on press** — flash the LED rapidly while held:

```python
if switch.value() == 0:
    led.on()
    time.sleep(0.05)
    led.off()
    time.sleep(0.05)
else:
    led.off()
    time.sleep(0.01)
```

---

## What you've built and where it leads

You've written a simple **polling loop**: check input, update output, repeat. This works well for one input and one output. When you add more devices — more buttons, LEDs, sensors — the loop gets complicated. You need to share time between devices, handle debounce, and decide what to do when two things happen at once.

This is the problem the **Connected Little Boxes** framework solves. In Chapter 2 you'll see how it replaces the polling loop with an *event-driven* model: instead of your code checking the button every 10 ms, the button *tells* your code when it changes — and your code only runs when there's something to do.
