## Your task

Open `start.py`. It already imports the library and calls `robot.init()`.

Add code to do the following:

1. Set the pixels to **red** and wait one second.
2. Set the pixels to **green** and wait one second.
3. Set the pixels to **blue** and wait one second.
4. Turn the pixels **off** (`robot.BLACK`).
5. Now try the other five named colours — `CYAN`, `MAGENTA`, `YELLOW`, `WHITE`, and `BLACK` — with a half-second pause between each.

---

## Checking your work

When you run the program:
- The strip should cycle through colours with visible pauses between each change.
- The strip should end dark (off).

---

## Going further

`robot.colour()` accepts any `(r, g, b)` tuple, not just the eight named constants. Try making **orange** (`(255, 128, 0)`) or **purple** (`(128, 0, 128)`).

What is the brightest white you can make? What happens when all three channels are at 255?
