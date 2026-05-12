# Lab 2: Writing the Program

The skeleton in the editor already imports `machine` and `time`, creates the `led` pin, and sets up the `while True` loop. Your job is to replace the four `# TODO` comments with working code.

---

## What to write

Inside the `while True:` loop, in order:

1. Call `led.on()` to turn the LED on
2. Call `time.sleep(0.5)` to wait half a second
3. Call `led.off()` to turn the LED off
4. Call `time.sleep(0.5)` to wait half a second
5. Remove the `pass` line (it was only there to make the empty loop valid Python)

---

## Save & Run

Click **Save & Run**. The app writes `main.py` to the Pico and reboots it. After a moment the LED should start flashing.

To stop it, press **Interrupt** in the toolbar (or Ctrl+C in the console). This sends a keyboard interrupt to MicroPython and stops the running program.

---

## Experiment

Once it's working, try changing the numbers:

- Make it flash faster: change both `0.5` values to `0.1`
- Make it flash slower: try `1.0`
- Create an unequal rhythm: `time.sleep(0.1)` on, `time.sleep(0.9)` off

> **Tip:** After each change, click Save & Run again to push the new code to the device.

---

## What `pass` does

`pass` is Python's "do nothing" statement. An empty `while True:` body is a syntax error, so `pass` acts as a placeholder until you fill it in. You'll see it often in starter code.
