# Lab 3: Console Commands

Type these commands in the **Console** panel. They use only `machine.Pin` and `machine.PWM` — no extra libraries needed.

---

## Set up the pins

```python
from machine import Pin, PWM

in1 = Pin(2, Pin.OUT)
in2 = Pin(3, Pin.OUT)
ena = PWM(Pin(6))
ena.freq(1000)
```

---

## Run forward at half speed

```python
in1.value(1)
in2.value(0)
ena.duty_u16(32768)   # 50%
```

---

## Run backward at full speed

```python
in1.value(0)
in2.value(1)
ena.duty_u16(65535)   # 100%
```

---

## Change speed without changing direction

```python
ena.duty_u16(16384)   # 25%
ena.duty_u16(49151)   # 75%
```

---

## Coast (motor spins down freely)

```python
in1.value(0)
in2.value(0)
ena.duty_u16(0)
```

---

## Active brake (motor stops immediately)

```python
in1.value(1)
in2.value(1)
ena.duty_u16(65535)
```

Short-circuiting both motor terminals creates a braking torque. The motor decelerates much faster than coasting.

---

## Observe

- Feel the difference between coast and brake — the shaft resists rotation when braking.
- Run forward at 25% speed — does the motor start reliably? Many motors have a minimum duty cycle below which they stall. Find yours.
- Connect the second motor (IN3, IN4, ENB on GP4, GP5, GP7) and run both simultaneously.

In Lab 4 you will wrap all of this in a clean class so you never have to remember the pin logic again.
