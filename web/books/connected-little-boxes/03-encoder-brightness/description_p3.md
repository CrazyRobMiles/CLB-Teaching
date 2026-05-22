# Step 2 — Connect the rotary encoder

Now subscribe to the encoder events and update brightness on each tick.

---

## Add the rotary encoder to app_default_settings

```python copy
"rotary_encoder": {
    "enabled": True,
    "encoders": [
        {"name": "brightness", "clk_pin": 16, "dt_pin": 17, "btn_pin": -1}
    ]
},
```

Add `"rotary_encoder"` to your `dependencies` list too.

---

## Subscribe to the events

The rotary encoder manager publishes two events per encoder, named:

```
rotary_encoder.<name>_moved_clockwise
rotary_encoder.<name>_moved_anticlockwise
```

Because your encoder is called `"brightness"`, the full names are:

```
rotary_encoder.brightness_moved_clockwise
rotary_encoder.brightness_moved_anticlockwise
```

In `setup_services`, add:

```python copy
cw = self.clb.get_event("rotary_encoder.brightness_moved_clockwise")
if cw:
    cw.subscribe(self.on_clockwise)

ccw = self.clb.get_event("rotary_encoder.brightness_moved_anticlockwise")
if ccw:
    ccw.subscribe(self.on_anticlockwise)
```

---

## Write the handlers

```python copy
def on_clockwise(self, event, data):
    self.brightness = min(1.0, self.brightness + self.step)
    if self.indicator:
        self.indicator.cmd_brightness(self.brightness)

def on_anticlockwise(self, event, data):
    self.brightness = max(0.0, self.brightness - self.step)
    if self.indicator:
        self.indicator.cmd_brightness(self.brightness)
```

`min` and `max` clamp the value so it never leaves the 0.0–1.0 range.

**Save & Run** — turning the encoder should now smoothly fade the strip up and down.

---

## Troubleshooting

If the encoder doesn't respond, check `status` in the console. If `rotary_encoder` is missing or faulted, verify `clk_pin` and `dt_pin` match your wiring and that `"rotary_encoder"` is in `dependencies`.
