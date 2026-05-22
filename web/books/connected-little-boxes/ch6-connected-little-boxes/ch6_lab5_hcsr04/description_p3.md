# Lab 5: Configuration and Console Commands

---

## Settings

```json
"hcsr04": {
    "enabled": true,
    "trigger_pin": 5,
    "echo_pin": 18,
    "interval_ms": 500,
    "threshold_mm": 300,
    "startup_offset_us": 450
}
```

| Setting | Effect |
|---------|--------|
| `trigger_pin` | GPIO number for the TRIG output |
| `echo_pin` | GPIO number for the ECHO input |
| `interval_ms` | Time between readings in milliseconds. Lower values give more frequent updates but each measurement ties up the echo pin briefly. 100–1000 ms is a practical range. |
| `threshold_mm` | The crossing distance for threshold events. The manager fires `hcsr04.below_threshold` when a reading drops below this value and `hcsr04.above_threshold` when it rises back above it. |
| `startup_offset_us` | Timing correction for the sensor's internal startup delay. 450 µs is correct for most HC-SR04 boards; only adjust if readings are consistently offset by a fixed amount. |

---

## Loading the configuration

Apply the default settings for this exercise:

```copy
reload
```

Confirm the manager is ready:

```copy
status
```

Expected output:

```
hcsr04  ok  HC-SR04 ready (trigger=5, echo=18)
```

If you see `error`, the most common cause is a pin conflict — another manager is already using one of those GPIO numbers.

---

## Console commands

The manager does not take readings until you call `start`. This is deliberate: the echo interrupt runs continuously once active, and you may not want that overhead until you need it.

### start

Begin taking distance readings at the configured interval:

```copy
hcsr04.start
```

### reading

Print the most recent distance measurement:

```copy
hcsr04.reading
```

Output: `[hcsr04] Distance: 342mm`

Move your hand toward and away from the sensor and call `reading` again to see the value change.

### set_interval

Change the reading rate without reloading:

```copy
hcsr04.set_interval 100
```

Readings every 100 ms. Use a faster interval when tracking a moving object; use a slower one to reduce CLB update loop overhead.

### set_threshold

Change the threshold distance:

```copy
hcsr04.set_threshold 200
```

Setting the threshold resets the crossing state — the manager re-evaluates whether the current distance is above or below the new value on the next reading.

### stop

Stop all readings and disable the echo interrupt:

```copy
hcsr04.stop
```

---

## Observe

1. Call `hcsr04.start`, then `hcsr04.reading` several times while moving an object toward the sensor. Note that `reading` returns the *last completed* measurement — if the sensor is firing every 500 ms, the value is up to 500 ms stale.

2. Set a fast interval (`hcsr04.set_interval 100`) and call `reading` repeatedly to see the value update more quickly.

3. Point the sensor at a wall at a known distance and compare the reading with a tape measure. You should be within ±5 mm.

4. Aim the sensor at the ceiling, then tilt it slightly. As the beam misses the ceiling and finds a distant object (or nothing), the reading will jump and eventually fire a timeout.
