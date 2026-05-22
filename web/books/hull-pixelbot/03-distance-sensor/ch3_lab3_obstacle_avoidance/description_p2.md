## Your task

Open `start.py`. The loop structure is provided; you need to fill in the movement and colour commands.

1. In the obstacle branch: set the pixel **red**, move backward **100 mm**, turn **90 degrees**, then set the pixel back to **green**.
2. In the clear branch: move forward **50 mm**.
3. Run the program and place obstacles (books, boxes) in the robot's path.

---

## Checking your work

- The robot should move forward until it detects an obstacle within 200 mm.
- It should stop, turn red, back up, turn, and then resume moving forward green.
- Left alone in a clear space the robot should just keep driving straight.

---

## Tuning challenge

Experiment with these values to improve the robot's behaviour:

| Parameter | Start value | Try increasing | Try decreasing |
|-----------|-------------|---------------|---------------|
| Obstacle threshold | 200 mm | Robot avoids earlier | Robot gets closer before turning |
| Backup distance | 100 mm | Clears obstacles better | Faster recovery |
| Turn angle | 90° | More direction change | Smaller heading change |
| Forward step | 50 mm | Faster but less responsive | Slower but checks more often |

---

## Going further

- Add a random element to the turn angle: `robot.turn(robot.random_val() * 10 + 60)` gives a turn between 70 and 180 degrees. Does this produce more varied exploration?
- Try a left turn instead of always turning right. Does the robot get stuck in corners?
- What happens if you set the forward step to 0 (remove the move)? The robot only moves when it detects an obstacle — is that useful?
