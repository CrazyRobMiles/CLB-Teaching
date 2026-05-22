## Your task

Open `start.py`. A colour list has been started for you, but it is incomplete and the loop is missing.

1. Add the remaining colour constants so the list contains all eight: `RED`, `GREEN`, `BLUE`, `CYAN`, `MAGENTA`, `YELLOW`, `WHITE`, `BLACK`.
2. Write a `for` loop that calls `robot.colour(c)` for each item with a half-second pause between each colour.
3. Wrap the whole thing in `while True` so it loops forever.

---

## Checking your work

When you run the program the pixel strip should cycle through all eight colours continuously, with a smooth half-second step between each one.

---

## Going further

- Change the sleep time. What is the fastest rate at which you can still clearly see each colour?
- Custom colours are plain tuples — add `(255, 128, 0)` (orange) or `(128, 0, 128)` (purple) anywhere in the list.
- Try building two separate lists — one warm, one cool — and alternate between them with a longer pause.
