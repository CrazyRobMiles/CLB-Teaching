# Lab 5: Switch and LED

You know how to control an LED and how to read a switch. Now combine them: the LED should light up while the button is pressed and go off when it's released.

---

## Why we need a program

In Lab 2 you controlled the LED by typing commands. In Lab 4 you read the switch the same way. But to react to the button *in real time*, you need code that reads the switch continuously and updates the LED on every pass of a loop.

You cannot do this by hand quickly enough — so you write a program.

---

## Circuit

Keep everything from Lab 4 connected:

- LED via 220 Ω resistor on **GP15 (physical pin 20)**
- Push button on **GP14 (physical pin 19)** to GND

![Switch and LED circuit](images/lab5_circuit.jpg)

*Photo: The breadboard with both the LED+resistor on GP15 and the push button on GP14 connected.*

---

## Plan

```
set up led as output on GP15
set up switch as input on GP14 with pull-up

loop forever:
    if switch is pressed (value == 0):
        turn LED on
    else:
        turn LED off
    short pause
```

The short pause (`time.sleep(0.01)`) prevents the program from consuming 100% of the CPU doing nothing useful between checks.
