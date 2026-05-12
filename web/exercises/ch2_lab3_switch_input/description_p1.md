# Lab 4: Switch Input

So far we've only produced outputs. Now we'll add an **input**: a push button whose state the Pico can read.

---

## How a push button works

A push button is a simple switch — it connects two terminals when pressed and disconnects them when released. On its own, connecting a pin directly to a button creates a problem: when the button is open (not pressed), the pin is connected to nothing. A pin with no defined voltage has an **undefined state** — it floats between 0 and 1 randomly, producing unreliable readings.

---

## The pull-up resistor

The solution is to tie the pin to 3.3 V through a large resistor (the **pull-up**). Now when the button is open, the pin reads HIGH (1). When the button is pressed and connects the pin to GND, the pin reads LOW (0).

```
3.3 V ── [pull-up resistor] ──┬── GP14
                               │
                           [button]
                               │
                              GND
```

The Pico has built-in pull-up resistors on every GPIO pin — you enable them in software with `machine.Pin.PULL_UP`, so **no extra resistor is needed in your circuit**.

---

## Circuit

Add a push button to your breadboard:

- One leg of the button into the same row as **GP14 (physical pin 19)**
- Other leg into the GND rail (or a row connected to a GND pin)

The LED from the previous labs can stay connected.

![Switch circuit](images/lab4_circuit.jpg)

*Photo: The breadboard from Lab 2 with a push button added. One leg of the button connects to GP14 (physical pin 19); the other connects to GND.*
