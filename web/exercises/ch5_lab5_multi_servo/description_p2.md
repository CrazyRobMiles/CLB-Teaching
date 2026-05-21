# Lab 5: Completing the Program

The skeleton has everything set up: PCA9685, four servos at 90°, four buttons with pull-ups, and the `last` list for edge detection. Fill in the four `TODO` blocks inside `while True`.

---

## What to write

For each button, detect a falling edge and take the appropriate action:

```python copy
if last[0] == 1 and btns[0] == 0:   # btn_prev
    active = (active - 1) % len(servos)
    print(f"Servo {active}: {servos[active]._degrees}°")

if last[1] == 1 and btns[1] == 0:   # btn_next
    active = (active + 1) % len(servos)
    print(f"Servo {active}: {servos[active]._degrees}°")

if last[2] == 1 and btns[2] == 0:   # btn_ccw
    servos[active].nudge(-5)
    print(f"Servo {active}: {servos[active]._degrees}°")

if last[3] == 1 and btns[3] == 0:   # btn_cw
    servos[active].nudge(5)
    print(f"Servo {active}: {servos[active]._degrees}°")
```

**Save & Run** — each button press should move the correct servo and print the new angle.

---

## What you have built

This is a small but complete multi-device embedded application:
- One I2C bus carrying all servo commands
- A hardware peripheral (PCA9685) managing 16 PWM channels independently
- A driver class (ServoDriver) providing a high-level interface
- An interactive control loop responding to four independent buttons

The Pico's CPU is almost entirely idle between button presses — the PCA9685 holds the servo positions without any CPU involvement.

---

## Where this leads

In a robot arm, each `ServoDriver` instance corresponds to one joint. A higher-level class would then compose them:

```python copy
class RobotArm:
    def __init__(self, pca):
        self.base     = ServoDriver(pca, 0)
        self.shoulder = ServoDriver(pca, 1)
        self.elbow    = ServoDriver(pca, 2)
        self.gripper  = ServoDriver(pca, 3)

    def home(self):
        for s in [self.base, self.shoulder, self.elbow, self.gripper]:
            s.angle(90)
```

In Chapter 5 (Connected Little Boxes) you will see how this kind of layered abstraction scales to complex systems with many interacting components.
