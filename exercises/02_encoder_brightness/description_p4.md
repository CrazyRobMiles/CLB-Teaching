# Step 3 — Customise and explore

Once the encoder controls brightness, try these extensions.

---

## Change the colour

Edit `red`, `green`, `blue` in `app_default_settings` (or in `settings.json` on the device) to set any colour you like.

Some starting points:

| Colour | R | G | B |
|--------|---|---|---|
| Amber  | 255 | 100 | 0 |
| Cool white | 200 | 220 | 255 |
| Red    | 255 | 0 | 0 |
| Green  | 0 | 255 | 50 |

---

## Change the step size

`"step": 0.05` means 20 clicks from off to full brightness. Try `0.1` for a coarser feel, or `0.02` for finer control.

---

## Add a button press to toggle on/off

The rotary encoder manager also publishes `rotary_encoder.<name>_button_pressed` if you wire up a button (set `btn_pin` to the correct GPIO). You could subscribe to that event to toggle the indicator on and off:

```python
btn = self.clb.get_event("rotary_encoder.brightness_button_pressed")
if btn:
    btn.subscribe(self.on_button)
```

---

## What you've learned

- How to subscribe to multiple events from the same manager
- How to store and update state between event calls
- How to use `min`/`max` to keep a value within a valid range
- That the CLB event pattern scales: adding a new encoder or indicator requires no changes to the other managers

---

## Quick reference

| Call | Effect |
|------|--------|
| `indicator.cmd_brightness(b)` | Set brightness (0.0–1.0) |
| `indicator.cmd_fill(r, g, b)` | Set all pixels to one colour |
| `clb.get_event(name)` | Get an event object |
| `event.subscribe(handler)` | Register a handler |

Handler signature: `def handler(self, event, data):`

Use the **AI Tutor** (Hints tab) if you get stuck — it knows this exercise and can guide you without just giving you the answer.
