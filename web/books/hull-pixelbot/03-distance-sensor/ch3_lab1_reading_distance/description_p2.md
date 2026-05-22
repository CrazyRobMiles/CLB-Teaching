## Your task

Open `start.py`.

1. Complete the reading loop so it prints the distance every half second for 30 readings.
2. Hold your hand at different distances in front of the sensor while it runs. Observe how the readings change.
3. Remove your hand entirely. What value does the sensor return?

---

## Checking your work

- Readings should be in the range 20–4000 mm for objects within range.
- A reading of -1 means no echo was received — nothing is in range, or there is a wiring problem.
- Readings should be reasonably stable (within ±10 mm) when you hold your hand still.

---

## Troubleshooting

| Symptom | Likely cause |
|---------|-------------|
| Always returns -1 | No echo received — check ECHO wiring and voltage divider |
| Readings jump wildly | ECHO connected directly without voltage divider |
| Readings are consistent but wrong | WHEEL_DIAMETER_MM in config.py is unrelated — check sensor wiring |
| No output at all | TRIGGER_PIN or ECHO_PIN in config.py do not match your wiring |

---

## Going further

- What is the maximum reliable range of the sensor? At what distance do readings become -1 or erratic?
- How close can you get before readings become unreliable? The minimum is approximately 20 mm.
- Point the sensor at a soft surface (a cushion, for example). Is it less reliable than a hard flat surface?
