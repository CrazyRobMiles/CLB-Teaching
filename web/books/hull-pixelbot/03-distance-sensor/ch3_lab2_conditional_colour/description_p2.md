## Your task

Open `start.py`. The while loop and distance reading are already there.

1. Complete the `if / elif / else` chain to produce three distance zones:
   - **Red** for objects closer than 100 mm
   - **Yellow** for objects between 100 mm and 300 mm
   - **Green** for objects farther than 300 mm
   - **White** if the reading is -1 (no echo)

2. Run the program and move your hand toward and away from the sensor. The pixel should change colour as you cross each threshold.

3. Adjust the threshold values so they feel right for your robot's physical size.

---

## Checking your work

Move your hand slowly toward the sensor from beyond 300 mm:
- The pixel should start green.
- It should turn yellow when your hand is roughly 300 mm away.
- It should turn red when your hand is roughly 100 mm away.

---

## Going further

- Add a fourth zone: **blue** for objects within 50 mm.
- Try adding a fifth: **magenta** for objects beyond 500 mm. What threshold gives you a reliable green-to-magenta transition?
- Print the distance value alongside the colour change. Does the printed value match what you expect at each threshold?
