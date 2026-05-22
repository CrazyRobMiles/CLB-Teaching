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
