## Your Task

Open `start.py`. It contains the countdown and game loop skeleton.

1. Add the `if / else` structure to read the distance sensor and choose between dodging and advancing.
2. Set different pixel colours for advancing (green) and dodging (yellow) so you can watch the behaviour.
3. Set the pixel to black when the game ends.

---

## Going Further

4. Add randomised dodge direction using `robot.random_val()`.
5. After dodging, the robot is facing sideways. What happens if it is near the arena wall? Add a short `distance()` check after the dodge to avoid hitting the side wall. (You would need a separate side-facing sensor for this to be reliable — think about why.)
6. Tune `DODGE_MM`, `DODGE_ANGLE`, and `DODGE_STEP` to find values that let the robot reliably slip past an opponent that is just standing still in the middle.

---

## Testing

Before testing in the arena, save your program as `main.py` on the Pico (**File → Save As → MicroPython device → main.py**). Unplug the USB cable and connect a battery pack — the robot will start automatically on power-up. While you still have the cable connected you can stop the program at any time with **Ctrl + C** in Thonny.

Test with the opponent robot switched off and placed in the centre of the arena. The dodger should detect it, swerve, and continue past to reach the far wall. If it misses, adjust the dodge angle or step.

Then test against a charging opponent. A charging opponent creates a moving target — does your dodge threshold need to be larger to give enough reaction time?
