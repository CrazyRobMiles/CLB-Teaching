# Lab 4: Testing and Calibrating

The skeleton's test code calls `angle(0)`, `angle(90)`, `angle(180)` with 1-second pauses. Once you implement `angle()`, **Save & Run** should sweep the servo through its full range.

---

## Calibrating MIN_PULSE and MAX_PULSE

The values 150 and 600 are starting points. Real servos vary:

- If the servo **doesn't reach 0°** (hits its physical stop before the commanded position), decrease `MIN_PULSE`
- If the servo **doesn't reach 180°**, increase `MAX_PULSE`
- If the servo **grinds at the end of its travel**, the pulse is too wide — back off `MAX_PULSE`

Because `MIN_PULSE` and `MAX_PULSE` are class attributes, you can override them per instance:

```python copy
servo0 = ServoDriver(pca, 0)
servo0.MIN_PULSE = 130    # this servo needs a narrower minimum
```

---

## Testing multiple servos

```python copy
servo0 = ServoDriver(pca, 0)
servo1 = ServoDriver(pca, 1)

servo0.angle(45)
servo1.angle(135)
```

Both commands complete in microseconds — the PCA9685 holds both positions simultaneously with no further CPU involvement.

---

## Experiment

**Slow sweep:**
```python copy
import time
for deg in range(0, 181, 5):
    servo0.angle(deg)
    time.sleep_ms(50)
```

**Oscillate two servos in opposite phases:**
```python copy
for deg in range(0, 181, 2):
    servo0.angle(deg)
    servo1.angle(180 - deg)
    time.sleep_ms(20)
```

In Lab 5 you will control four servos interactively using buttons.
