# Lab 3: Reading the Switch

Type these commands in the **Console** panel.

---

## Create an input pin with pull-up

```python
import machine
switch = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
```

Three arguments:
1. `14` — GP14
2. `machine.Pin.IN` — configure as input
3. `machine.Pin.PULL_UP` — enable the internal pull-up resistor

---

## Read the value

```python
switch.value()
```

This returns:
- **`1`** when the button is **not pressed** (pin pulled to 3.3 V)
- **`0`** when the button **is pressed** (pin connected to GND)

Try it: call `switch.value()` and press the button while calling it again.

---

## Watch the value change

To see the value update continuously, run this in the console:

```python
import time
while True:
    print(switch.value())
    time.sleep(0.1)
```

Press the button and watch the output change from `1` to `0`. Press **Ctrl+C** to stop.

---

## Why is the logic inverted?

With a pull-up, "not pressed" reads as 1 and "pressed" reads as 0. This is called **active-low** logic. It's very common in electronics because it makes the wiring simpler (no power wire to the button — just GND). Your code checks `if switch.value() == 0` to mean "button is pressed".

---

## Experiment

- What does `switch.value()` return when you hold the button down?
- What happens if you remove the `PULL_UP` argument? (The pin will float — the readings will be unreliable.)
- Can you write a loop that only prints when the value *changes*?
