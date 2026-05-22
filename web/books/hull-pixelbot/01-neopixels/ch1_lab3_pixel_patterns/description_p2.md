## Your task

Open `start.py`. The chasing loop is partially written.

1. Complete the loop so it chases a **green** pixel from index 0 to index 7.
2. Then add a second loop that chases the pixel back from index 7 to index 0.  
   *Hint: use `range(7, -1, -1)` to count down.*
3. Wrap both loops in `while True` so the pixel bounces back and forth continuously.

---

## Checking your work

When you run the program a single green pixel should move smoothly from one end of the strip to the other and back, repeating indefinitely.

---

## Going further

- Change the chasing pixel colour.  Can you make it change colour as it travels — starting red and ending blue?
- Light **two** pixels at once: one slightly ahead of the other in a different colour, to give a comet trail effect.
- Instead of clearing the whole strip each step, try turning off only the *previous* pixel. Does it look any different?
