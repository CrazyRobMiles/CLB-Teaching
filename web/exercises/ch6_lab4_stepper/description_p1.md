# Lab 4: Stepper Motors

A **stepper motor** moves in discrete, numbered steps rather than spinning freely like a DC motor. Send it a command and it advances exactly the number of steps you asked for — no encoder or feedback sensor required. That precision makes steppers useful for robot wheels, 3D printer axes, and camera sliders.

---

## The 28BYJ-48

The motor used in this lab is the 28BYJ-48: a small, cheap, unipolar stepper with an internal gear train.

| Property | Value |
|----------|-------|
| Type | Unipolar, 4-phase |
| Supply voltage | 5 V |
| Wires | 5 (one common + four coil pins) |
| Motor shaft steps per revolution | 64 (in half-step mode: 512) |
| Internal gear ratio | approximately 64:1 |
| Output shaft half-steps per revolution | 4096 |

The gear reduction trades speed for torque: the output shaft is strong enough to drive a small robot wheel but rotates slowly. Running at maximum speed (one half-step every 1200 µs) a full output revolution takes about 4.9 seconds.

---

## The ULN2003 Driver Board

Each coil in the motor draws up to 200 mA — far more than a Pico GPIO pin can supply. The ULN2003 breakout board solves this the same way the L298N did for DC motors: its **Darlington transistor array** uses the GPIO signal to switch the full coil current from the 5 V supply.

| ULN2003 board pin | Purpose |
|-------------------|---------|
| IN1 – IN4 | Control signals from the Pico (3.3 V logic is fine) |
| OUT1 – OUT4 | Connected internally to the motor's four coil wires |
| VCC | 5 V motor power (connect to Pico VBUS) |
| GND | Common ground |

The motor's 5-pin JST connector plugs directly into the matching socket on the ULN2003 board. The four coil wires connect automatically; the red common wire connects to the board's VCC rail.

Each IN pin has an indicator LED on the board. When a coil is energised the corresponding LED lights — a useful diagnostic when checking the wiring.

---

## The Half-Step Sequence

The CLB stepper manager drives the four coil pins in an **8-step half-step sequence**. Steps that energise a single coil pull the rotor to a full-step position; steps that energise two adjacent coils pull the rotor to the intermediate half-step position.

| Step | IN1 | IN2 | IN3 | IN4 | Active coils |
|------|-----|-----|-----|-----|--------------|
|  0   |  1  |  0  |  0  |  0  | A only       |
|  1   |  1  |  1  |  0  |  0  | A + B        |
|  2   |  0  |  1  |  0  |  0  | B only       |
|  3   |  0  |  1  |  1  |  0  | B + C        |
|  4   |  0  |  0  |  1  |  0  | C only       |
|  5   |  0  |  0  |  1  |  1  | C + D        |
|  6   |  0  |  0  |  0  |  1  | D only       |
|  7   |  1  |  0  |  0  |  1  | D + A        |

Progressing 0 → 1 → 2: the rotor aligns with coil A, is attracted to the midpoint between A and B, then aligns with coil B. Running the sequence in reverse steps the motor in the opposite direction.

After a move finishes, the manager de-energises all four coils automatically. The gear train holds position without needing powered holding.

---

## Distance and Steps

The manager converts millimetres to steps using the wheel geometry you configure:

```
steps = (distance_mm / (π × wheel_diameter_mm)) × steps_per_rev
```

For the 69 mm wheels in this lab: circumference = π × 69 ≈ 216.8 mm. Moving 200 mm requires about 200 / 216.8 × 4096 ≈ 3780 half-steps per wheel.
