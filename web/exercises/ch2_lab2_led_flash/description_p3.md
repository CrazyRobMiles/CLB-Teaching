# Python Indentation

Python uses indentation — the spaces at the start of each line — to define which lines belong together. Unlike most other languages, there are no curly braces `{}`: the indentation *is* the structure.

---

## How it works

Look at the loop you just wrote:

```python
while True:
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)
```

The four lines are indented by 4 spaces. Python sees that indentation and knows they belong to the `while True:` block. If you removed the indentation, Python would raise a `SyntaxError` because it expects an indented block after the colon.

Every line ending in `:` — such as `while`, `if`, `for`, or `def` — must be followed by an indented block.

---

## Spaces vs tabs

There are two characters that can create indentation:

| Character | Key to press | What Python sees |
|-----------|-------------|-----------------|
| Space (×4) | Spacebar | Four individual space characters |
| Tab (×1)  | Tab key  | One tab-stop character |

**Always use spaces — never tabs.**

Python allows either, but **mixing tabs and spaces in the same file causes an error**. Because a tab and four spaces can look identical on screen, this mistake is easy to make and hard to spot by eye.

The Python standard — and this course — uses **4 spaces** per indentation level.

> **In this editor**, pressing the Tab key automatically inserts 4 spaces, so you will not accidentally type a tab character. Code pasted from another source (such as a website) may still contain tabs.

---

## Common indentation errors

```
IndentationError: unexpected indent
```
A line is indented by a different amount than expected. Check that every line in the same block uses exactly the same number of spaces.

```
TabError: inconsistent use of tabs and spaces in indentation
```
A line mixes tab characters and spaces. This is almost always a copy-paste issue. Replace all tabs in that block with 4 spaces each.

---

## Seeing the difference in the editor

The editor marks every whitespace character with a subtle indicator:

- A small **dot** marks each **space** character
- A short **line** marks each **tab** character

Indentation that shows only dots is correct for this course. If you see a line indicator anywhere in the indentation, that character is a tab and needs to be replaced with 4 spaces.

Each additional level of indentation adds 4 more dots on the left — a nested `if` inside a `while` loop would show 8 dots of indentation.
