## Deploying Your Program to the Robot

So far you have been running programs from Thonny while the Pico is plugged into your computer. For the sumo arena the robot runs **on its own** — no laptop, no cable.

MicroPython automatically runs a file called `main.py` from the Pico's storage every time it powers up. To deploy your sumo program:

1. In Thonny, go to **File → Save As**.
2. When prompted where to save, choose **MicroPython device** (not your laptop).
3. Name the file `main.py` and click OK.

Now unplug the USB cable, connect a battery pack, and the robot will start your program immediately on power-up — no button press needed.

---

## Stopping the Robot During Development

While the USB cable is connected you can stop a running program at any time:

- In **Thonny**: click the red **Stop** button, or press **Ctrl + C** in the Shell panel.
- In **mpremote**: press **Ctrl + C**.

Any keypress sent from the console stops the robot and returns to the MicroPython prompt — this works even in the middle of a motor move.

When running on battery in the arena there is no console, so the program simply runs until it finishes naturally. The sumo programs in the next three labs all stop by themselves when the game timer expires: the motors halt and the pixels turn off.

---

## Setting Up

Before writing any code, build and prepare the arena:

1. **Build the arena** from construction bricks. A rectangle roughly 600 mm × 400 mm works well. The walls only need to be one or two bricks high — just enough to feel like a defined space.
2. **Mark the centre line** with a strip of tape across the arena floor.
3. **Place both robots** at opposite ends, touching their end walls, sensors facing inward.
4. **Test your distance sensor** — with the robot at one end of a 600 mm arena you should see a reading of roughly 400–500 mm (the gap between the two robots).

---

## Questions to Think About

Before you write your first sumo program, consider:

- **What does your robot do when the opponent is very close (e.g. 100 mm)?**
- **What does your robot do when it cannot see the opponent (sensor returns -1)?**
- **What happens if both robots collide head-on and stall?**
- **How do you know whether your robot has crossed the centre line?** (Hint: count how far you have moved.)

---

## Choosing a Tactic

The next three labs each cover one core tactic. You can test each one, then design your own program that combines ideas from all three.

| Lab | Tactic | Summary |
|-----|--------|---------|
| Lab 2 | Charging | Drive straight at full speed — simple but predictable |
| Lab 3 | Dodging | Use the sensor to swerve around the opponent |
| Lab 4 | Curving | Approach from the side with arc moves |
