## Your task

Open `start.py`. It contains only `robot.init()` — the rest is yours.

Design and implement a robot behaviour. Some suggestions:

1. **Decide what your robot will do.** Write it down in a comment at the top of your program before you write any code.

2. **Plan the states.** Most robot behaviours can be described as a small number of states: *moving forward*, *avoiding obstacle*, *searching*, *following*. What states does your behaviour have?

3. **Use the pixel to show state.** Pick a colour for each state. This makes it much easier to understand what the robot is doing while it runs.

4. **Start simple.** Get a basic version working first, then add complexity.

---

## Things to consider

- What should happen when `distance()` returns -1?
- What should the robot do when it reaches the edge of a table? (If your robot is on a table, consider using a very short `move()` step with a frequent distance check.)
- Is there a situation your robot could get stuck in? How would you detect and recover from it?

---

## Sharing your work

When you have a behaviour you are pleased with:
- Add a comment at the top describing what it does.
- Test it in different environments (open floor, corridor, cluttered table).
- Consider: what would you need to change to make it work better? What would the Connected Little Boxes framework give you that the sequential library cannot?
