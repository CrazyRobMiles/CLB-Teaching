## Your Task

Open `start.py`. It contains the countdown and game loop skeleton.

1. Add code inside the `while` loop to move the robot forward.
2. Set a pixel colour during the charge so you can see the robot is running.
3. Set the pixel to black when the game ends.

---

## Going Further

4. Add the instant-win check: stop if the distance sensor reads less than 50 mm (the robot has reached the far wall).
5. Experiment with different step sizes — does a larger step make the robot faster overall?
6. What if you charge at reduced speed (`seconds=` parameter)? Does a slower, more controlled push work better when the robots collide head-on?

---

## Testing

Place your robot at one end of the arena with no opponent. Switch it on and measure where it ends up after 30 seconds. It should be at or beyond the far wall if the arena is 600 mm or shorter.

Then try it against an opponent robot running the same charging program. Watch what happens in the head-on collision — do the robots stall, or does one push the other back?
