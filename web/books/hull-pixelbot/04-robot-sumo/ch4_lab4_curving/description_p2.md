## Your Task

Open `start.py`. It contains the countdown and game loop skeleton.

1. Add the alternating arc loop to make the robot weave across the arena.
2. Add the close-range charge: if the sensor reads less than 150 mm, drive straight forward instead of curving.
3. Use pixel colours to distinguish curving (blue) from charging (red).

---

## Going Further

4. Try a pure one-direction curve: `robot.arc(ARC_RADIUS, 360)` traces a full circle. What sumo strategy does a spinning robot represent?
5. Start with a large arc that sweeps from one side of the arena to the other, then switch to a weave once past the centre line. Does this make the approach harder to track?
6. Play your curving robot against a charging robot and against a dodging robot. Which matchup does curving win, and which does it lose?

---

## Testing

Run the curving program in the empty arena first and watch the path the robot traces. Mark where it ends up after the full game duration. Does it cover more width than a charging robot? Does it end up further into the opponent's half?

Then add the opponent. Because the curving robot approaches from angles, its forward-facing sensor will sometimes not be pointing at the opponent — test whether the close-range charge trigger fires at the right moment.
