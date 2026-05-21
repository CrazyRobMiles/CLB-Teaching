# Lab 4: Configuration

The stepper manager reads all of its settings from `settings.json` on the device. This page explains the settings structure and how to load the robot configuration.

---

## Settings structure

```json
"stepper": {
    "enabled": true,
    "wheel_spacing_mm": 110,
    "steps_per_rev": 4096,
    "min_step_delay_us": 1200,
    "motors": [
        {"pins": [15, 14, 13, 12], "wheel_diameter_mm": 69},
        {"pins": [8,  9, 10, 11],  "wheel_diameter_mm": 69}
    ]
}
```

Motor index **0 is always left**, index **1 is always right**. The `pins` array lists the GPIO numbers for IN1, IN2, IN3, IN4 in that order.

---

## What each setting does

| Setting | Effect |
|---------|--------|
| `wheel_diameter_mm` | Converts millimetres to steps: a larger value means more mm per step, so the robot travels further than expected. Measure across the tyre, not the hub. |
| `wheel_spacing_mm` | Distance between the two wheel contact patches. Used by `rotate` and `arc` to calculate how far each wheel travels. |
| `steps_per_rev` | Half-steps per output shaft revolution. 4096 is correct for the 28BYJ-48 in half-step mode. |
| `min_step_delay_us` | Minimum time between half-steps in microseconds. Lower = faster, but the motor stalls if driven too fast. 1200 µs is the reliable minimum for the 28BYJ-48. |
| `motors[n].pins` | GPIO numbers for IN1–IN4 of motor n. Reversing this order reverses the motor's direction. |

---

## Loading the configuration

This exercise's default settings already contain the robot configuration above. Apply them:

```copy
reload
```

Then verify the manager started:

```copy
status
```

You should see:

```
stepper  ready  Stepper ready (2 motor(s)) on rp2
```

If the status shows `error`, check the REPL output for a message — it usually means a pin number is wrong or the `motors` list is malformed.

---

## Changing a setting

Adjust any value live from the console. The change is written to `settings.json` immediately and persists across reboots:

```copy
set stepper.wheel_spacing_mm=115
reload
```

You can also adjust individual motor settings using dot notation into the JSON:

```copy
set stepper.motors[0].wheel_diameter_mm=71
reload
```

---

## How the manager fits into CLB

The stepper manager is a **device manager**: it handles one piece of hardware (the motors) and exposes a console API. Unlike the application managers you built in earlier exercises, it has no `setup_services()` — it does not subscribe to events or provide services to other managers.

Its timer callback runs in a hardware interrupt context, advancing the half-step sequence for whichever motors have remaining steps. The `update()` method runs in the main loop and detects when movement has finished, de-energising the coils and setting the state back to `ready`.
