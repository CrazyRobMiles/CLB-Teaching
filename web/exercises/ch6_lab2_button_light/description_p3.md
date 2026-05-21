# Part 3: Add the Indicator Manager

The indicator manager drives the NeoPixel strip. To use it, your application needs to do two things:

1. **Declare it** in `app_default_settings` so CLB loads it at boot
2. **Get a service handle** to it in `setup_services()` so you can call its functions

### Services

Device managers expose their capabilities as *services* — a dictionary of named functions returned by `get_interface()`. The indicator manager exposes functions like `fill`, `set`, `fade`, and others.

You access these from another manager using `get_service_handle()`:

```python copy
self.indicator = self.get_service_handle("indicator")
```

This returns the manager object. Calling `self.indicator.cmd_fill(255, 100, 0)` calls the indicator manager's `cmd_fill` function with those arguments.

### Modify Your App

Add the indicator section to `app_default_settings`. Your settings block should now look like this:

```python copy
app_default_settings = {
    "indicator": {
        "enabled": True,
        "pixelpin": 18,
        "count": 8,
        "pixeltype": "RGB",
        "brightness": 1.0
    },
    "App_button_light": {
        "enabled": True,
        "on_red": 255,
        "on_green": 100,
        "on_blue": 0,
        "dependencies": ["indicator"]
    }
}
```

Note two things: the `on_red`, `on_green`, `on_blue` settings define the colour you will use later, and `"indicator"` has been added to `dependencies` so CLB initialises the indicator manager before your application.

Now add `setup_services()` to your class — this goes after `setup()`:

```python copy
def setup_services(self):
    self.indicator = self.get_service_handle("indicator")
    if self.indicator:
        self.indicator.cmd_fill(0, 0, 0)
```

And add `self.indicator = None` to `__init__`:

```python copy
def __init__(self, clb):
    super().__init__(clb)
    self.indicator = None
```

Save the file. Now reload the application:

```copy
select-app Button Light
```

**What you should see:** The device reboots. Now `status` shows both `indicator` and `App_button_light` in state `ok`. The pixel strip should initialise (it may flash briefly) and settle to off.

Try calling the indicator service directly from the REPL:

```copy
indicator.fill 255 0 0
```

The strip should turn red. Turn it off again:

```copy
indicator.fill 0 0 0
```

### Think About It

- You called `indicator.fill` from the REPL just like your code will call it. The REPL and your manager use the same service interface. Why is that consistent design useful?
- What does `get_service_handle("indicator")` return if the indicator manager failed to initialise? Why does the `if self.indicator:` guard matter?
- The indicator settings are inside your `app_default_settings`. Who owns those settings — your app or the indicator manager?
