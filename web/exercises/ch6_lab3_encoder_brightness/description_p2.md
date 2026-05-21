# Step 1 — Set up the skeleton and the indicator

Start from the skeleton in the editor. Your first job is to wire up the indicator service so the LEDs show a colour at a starting brightness.

---

## Add the indicator to app_default_settings

```python copy
app_default_settings = {
    "indicator": {
        "enabled": True,
        "pixelpin": 18,
        "count": 8,
        "pixeltype": "RGB",
        "brightness": 1.0          # indicator's own max — we'll control brightness in code
    },
    "App_encoder_brightness_start": {
        "enabled": True,
        "red": 255,
        "green": 100,
        "blue": 0,
        "step": 0.05,
        "dependencies": ["indicator"]   # rotary_encoder comes next
    }
}
```

> **Why list `"indicator"` in `dependencies`?**  
> It tells the CLB boot system to start the indicator manager *before* your app, so `get_service_handle` can find it.

---

## Add instance variables and read settings

In `__init__`:

```python copy
self.indicator = None
self.brightness = 0.5     # start halfway
```

In `setup`, read your colour and step values from settings:

```python copy
self.red   = self.settings.get("red",   255)
self.green = self.settings.get("green", 100)
self.blue  = self.settings.get("blue",    0)
self.step  = self.settings.get("step",  0.05)
```

---

## Get the service and light the LEDs

Add a `setup_services` method:

```python copy
def setup_services(self):
    self.indicator = self.get_service_handle("indicator")
    if self.indicator:
        self.indicator.cmd_brightness(self.brightness)
        self.indicator.cmd_fill(self.red, self.green, self.blue)
```

**Save & Run** — the strip should glow amber at half brightness.
