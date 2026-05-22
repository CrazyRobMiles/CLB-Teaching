# Lab 1: Reading Distance

The HC-SR04 is an ultrasonic distance sensor. It works by sending a short burst of ultrasound, then measuring how long it takes for the echo to return. Because sound travels at a known speed (343 m/s in air), the distance to the nearest object can be calculated from the echo time.

---

## How the sensor works

The HC-SR04 has two components:

- **Trigger (TRIG)** — a GPIO output from the Pico. A 10 µs pulse on this pin fires the ultrasound burst.
- **Echo (ECHO)** — a GPIO input to the Pico. This pin goes high when the burst fires and low when the echo returns. The width of the high pulse is the echo time.

The robot library measures the echo pulse width using a pin interrupt and converts it to millimetres:

```
distance_mm = echo_duration_µs × 343 / 2000
```

The division by 2 accounts for the fact that the sound travels to the object and back.

---

## Voltage divider — important!

The HC-SR04 runs on 5 V and its ECHO pin outputs a **5 V signal**. A Pico GPIO input is rated for **3.3 V maximum**. Connecting ECHO directly will damage the Pico over time.

You must connect ECHO through a **voltage divider** using two resistors:

```
ECHO ──┬── 1 kΩ ──── Pico GPIO
       └── 2 kΩ ──── GND
```

This reduces the 5 V signal to approximately 3.3 V:

```
Vout = 5 V × 2 kΩ / (1 kΩ + 2 kΩ) = 3.33 V
```

TRIG connects directly — it only receives a 3.3 V signal from the Pico and that is sufficient to trigger the sensor.

---

## Reading distance in code

```python
mm = robot.distance()
print("Distance:", mm, "mm")
```

`robot.distance()` sends a trigger pulse, waits for the echo, and returns the distance in millimetres. It returns **-1** if no echo is received within the timeout (60 ms) — meaning nothing is within range or there is a wiring problem.
