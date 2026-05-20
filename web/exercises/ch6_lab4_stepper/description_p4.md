# Lab 4: Console Commands

Type these commands in the **Console** panel. The stepper manager must be in `ready` state — confirm with `status` before starting.

---

## move

Move both wheels the same distance. Positive moves forward, negative moves backward.

```
stepper.move 200
```

Moves the robot forward 200 mm. With 69 mm wheels this is 200 / (π × 69) ≈ 0.92 wheel revolutions, or about 3780 half-steps per motor.

```
stepper.move -100
```

Moves backward 100 mm.

```
stepper.move 500 5
```

Moves forward 500 mm, completing the move in 5 seconds. The second argument sets the duration; omitting it runs at maximum speed (one half-step every 1200 µs).

---

## rotate

Spin in place around the midpoint between the wheels. Positive is clockwise when viewed from above (left wheel forward, right wheel backward).

```
stepper.rotate 90
```

Turns 90° clockwise. The manager computes arc_len = π × 110 × 90 / 360 ≈ 86 mm for each wheel.

```
stepper.rotate -180
```

Turns 180° counter-clockwise — a U-turn.

```
stepper.rotate 360 4
```

One full clockwise rotation in 4 seconds.

---

## arc

Move along a circular arc. The first argument is the radius to the robot's centre in mm; the second is the angle to sweep in degrees.

```
stepper.arc 200 90
```

Sweeps a 90° arc curving to the **left** with a 200 mm radius. The inner (left) wheel travels `2π × (200 − 55) × 90/360 ≈ 228 mm`; the outer (right) wheel travels `2π × (200 + 55) × 90/360 ≈ 400 mm`.

```
stepper.arc 200 -90
```

Same 200 mm radius but curving to the **right** — the sign of the angle reverses which side is inner and outer.

```
stepper.arc 150 180 6
```

A 180° semicircle of radius 150 mm in 6 seconds. The robot ends up 300 mm to the side of where it started.

---

## stop

Stop both motors immediately and de-energise all coils.

```
stepper.stop
```

Use this if a move is wrong or the robot is about to fall off the table.

---

## moving

Report whether a movement is still in progress.

```
stepper.moving
```

Returns `moving` or `stopped`. Useful for confirming that a move has completed before issuing the next one.

---

## Observe

Work through these in order. Each one tests a different part of the system.

**1. Straight line accuracy**

Run `stepper.move 500` and measure the actual distance travelled. If it is consistently shorter or longer than 500 mm, the value in `wheel_diameter_mm` does not match your actual wheel. Adjust and re-run until the distance is correct.

**2. Rotation accuracy**

Run `stepper.rotate 360` and check whether the robot ends up pointing in the same direction it started. If it over- or under-rotates, `wheel_spacing_mm` is wrong — increase it if the robot over-rotates, decrease it if it under-rotates. (This setting does not affect straight-line accuracy, only rotation and arcs.)

**3. Arc geometry**

Run `stepper.arc 150 180`. The robot should trace a semicircle and stop approximately 300 mm to its left. After calibrating `wheel_diameter_mm` and `wheel_spacing_mm` in the steps above, this should be accurate without further adjustment.

**4. Speed**

Hold the robot off the ground and run `stepper.move 500 30` (500 mm over 30 seconds). At this slow speed you can see the ULN2003 indicator LEDs stepping through the 8-step pattern. Each full cycle of all four LEDs is one electrical revolution of the motor; 64 electrical revolutions equals one output shaft revolution.

**5. Motor direction**

If one motor runs backward — the robot curves or spins instead of going straight — reverse the pin order for that motor in settings:

```
set stepper.motors[0].pins=[12,13,14,15]
reload
```

(This reverses the half-step sequence for motor 0, making it spin the other way.)
