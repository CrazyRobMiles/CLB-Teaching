# Lab 5: Distance Sensor

The **HC-SR04** measures distance by timing a reflected sound pulse. It needs no moving parts, draws little power, and works reliably from about 20 mm to 4000 mm — useful for obstacle detection, proximity triggers, and fill-level sensing.

---

## How ultrasonic ranging works

Sound travels through air at approximately 343 m/s. If you emit a short pulse and measure how long it takes for the echo to return, you can compute the distance to the reflecting surface:

```
distance = (travel_time × speed_of_sound) / 2
```

The division by 2 accounts for the round trip — the sound travels to the target and back.

---

## The HC-SR04 protocol

The sensor has four pins: VCC, GND, TRIG, and ECHO. A measurement works like this:

1. Hold TRIG low for at least 2 µs to clear any previous state.
2. Raise TRIG high for **10 µs**, then bring it low. This tells the sensor to fire a burst of 8 × 40 kHz ultrasonic pulses.
3. The sensor raises ECHO high when it starts transmitting.
4. When the echo returns, the sensor pulls ECHO low.
5. The duration of the ECHO pulse is the round-trip travel time.

```
TRIG:  _____|‾‾10µs‾‾|_________________________________
ECHO:  ___________|‾‾‾‾‾ travel time ‾‾‾‾‾‾|__________
```

The CLB manager fires the TRIG pulse from the main update loop. It starts its own timer when the TRIG pulse ends, then catches the falling edge of ECHO using a GPIO interrupt.

---

## Distance formula

The manager converts the measured duration to millimetres using:

```
distance_mm = (duration_us × 343) / 2000
```

At 343 m/s = 0.343 mm/µs, a 1 mm gap produces a 2/0.343 ≈ 5.8 µs round-trip. A reading of 1000 µs corresponds to about 171 mm.

---

## The startup offset

The manager sets its timer when the TRIG pulse ends, not when ECHO rises. The sensor takes approximately 450 µs to process the trigger and begin transmitting. Without correction this delay would inflate every reading by 450 × 0.1715 ≈ 77 mm.

The `startup_offset_us` setting (default 450) is subtracted from the raw duration before computing distance. You should not normally need to change it.

---

## Range and accuracy

| Property | Value |
|----------|-------|
| Minimum range | ~20 mm |
| Maximum range | ~4000 mm |
| Accuracy | ±3 mm typical |
| Beam angle | ~15° cone |
| Supply voltage | 5 V |

Readings below 20 mm are unreliable — the transmitted and reflected pulses overlap. Objects outside the beam cone, or highly sound-absorbing materials (foam, thick fabric), may not return a detectable echo. When no echo arrives within 500 ms the manager fires a **timeout** event.
