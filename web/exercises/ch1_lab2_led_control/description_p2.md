# Lab 2: Console Commands

With the device connected, type these commands one at a time in the **Console** panel at the bottom of the screen. Press Enter after each one.

---

## Import the machine module

```python
import machine
```

`machine` is MicroPython's built-in module for hardware control. You need to import it before you can use pins.

---

## Create an output pin

```python
led = machine.Pin(15, machine.Pin.OUT)
```

This creates a Pin object for GP15 and configures it as an **output**. The result is stored in the variable `led`.

---

## Turn the LED on and off

```python
led.on()
```

```python
led.off()
```

You can also use `value()` with 0 or 1:

```python
led.value(1)    # same as led.on()
led.value(0)    # same as led.off()
```

Try switching the LED on and off a few times to confirm it responds instantly.

---

## Read the current state

```python
led.value()
```

Called without arguments, `value()` returns the current output state: `1` for on, `0` for off.

---

## Experiment

- Try assigning the pin to a different GP number (e.g. `machine.Pin(14, machine.Pin.OUT)`) — does anything happen? (No LED there yet, but the pin still works.)
- What happens if you create the same pin twice?

In the next lab we'll write a program so the LED flashes on its own — without you having to type every command.
