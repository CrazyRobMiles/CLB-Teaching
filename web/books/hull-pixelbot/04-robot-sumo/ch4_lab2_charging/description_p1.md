# Lab 2: Charging

The simplest sumo tactic is the **charge**: drive straight forward for the entire game duration at full speed. No sensor reading, no turning — just raw forward momentum.

---

## Why Charging Works

- A charging robot covers maximum distance. If the opponent is stationary or slow it will reach the far end and win instantly.
- There are no sensor readings to go wrong — the program is as simple as it gets.
- The stepper motors have enough torque that a charging robot can physically push a lighter or slower opponent backward.

---

## Why Charging Can Fail

- A charging robot is completely predictable. An opponent using the Dodging tactic (Lab 3) can swerve around it.
- If both robots charge head-on, they collide in the middle. Both stall. Neither makes progress.
- The robot cannot respond to anything — it commits to one direction regardless of what it senses.

---

## The Program Structure

```python
import time
import robot

GAME_S = 30

robot.init()

# Countdown: 3 red flashes
for _ in range(3):
    robot.colour(robot.RED)
    time.sleep(0.5)
    robot.colour(robot.BLACK)
    time.sleep(0.5)

# Charge: keep moving forward for the whole game
start = time.time()
robot.colour(robot.RED)

while time.time() - start < GAME_S:
    robot.move(100)   # advance 100 mm per step

robot.colour(robot.BLACK)
```

The `move(100)` inside the loop drives the robot 100 mm at a time. Each call blocks until the move finishes, then the loop checks whether the game is still running before taking another step.

---

## Tuning the Step Size

The step size (100 mm above) is a trade-off:

- **Larger steps** (e.g. 200 mm) mean fewer loop iterations and slightly faster overall progress — but the robot is less responsive to the time limit at the end.
- **Smaller steps** (e.g. 50 mm) mean more loop iterations and a sharper cutoff when time expires.

For a 30-second game at full speed, 100 mm steps work well for most arena sizes.

---

## Sensing the Instant-Win Condition

A refined charging program can watch for the instant-win condition — reaching the far wall:

```python
while time.time() - start < GAME_S:
    mm = robot.distance()
    if mm > 0 and mm < 50:
        # We are at (or have pushed past) the far wall — stop
        break
    robot.move(100)
```

When the sensor reads less than 50 mm the robot is very close to the far wall or has already won. `break` exits the game loop immediately.
