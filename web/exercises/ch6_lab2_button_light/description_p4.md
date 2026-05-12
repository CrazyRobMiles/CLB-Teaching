# Part 4: Add the Button

You now have a working output. The final step is connecting an input to it. The GPIO manager watches input pins and, when a pin changes state, **publishes an event**.

### Events

An event is a named signal. Any manager can subscribe to any event by name. When the event fires, every subscriber's handler function is called with `(event, data)`.

This is the publish/subscribe pattern. The GPIO manager does not know or care who is listening. Your application does not know or care how the GPIO manager detected the change. They are connected only by a name — a string.

The GPIO manager names its events using a consistent pattern:

```
gpio.<pin_name>_low     ← pin went low (button pressed, with pull-up)
gpio.<pin_name>_high    ← pin went high (button released)
```

Your pin is named `"button"` in the settings. So the events are `gpio.button_low` and `gpio.button_high`.

### Modify Your App

Add the `gpio` section to `app_default_settings`:

```python
"gpio": {
    "enabled": True,
    "input_pins": [{"name": "button", "pin": 14}],
    "output_pins": [],
    "default_debounce_ms": 20,
    "pullup": True
},
```

Add `"gpio"` to the dependencies list:

```python
"dependencies": ["indicator", "gpio"]
```

Read the colour settings in `setup()`, after the `STATE_OK` line:

```python
self.on_red   = self.settings.get("on_red",   255)
self.on_green = self.settings.get("on_green", 100)
self.on_blue  = self.settings.get("on_blue",    0)
```

Add the two event subscriptions to `setup_services()`:

```python
button_pressed = self.clb.get_event("gpio.button_low")
if button_pressed:
    button_pressed.subscribe(self.on_button_pressed)

button_released = self.clb.get_event("gpio.button_high")
if button_released:
    button_released.subscribe(self.on_button_released)
```

Add the two handler methods to your class:

```python
def on_button_pressed(self, event, data):
    if self.indicator:
        self.indicator.cmd_fill(self.on_red, self.on_green, self.on_blue)

def on_button_released(self, event, data):
    if self.indicator:
        self.indicator.cmd_fill(0, 0, 0)
```

Save. Reload:

```
select-app Button Light
```

**What you should see:** Press the button — the pixels light up. Release — they go off. The application is complete.

### Think About It

- Your `on_button_pressed` handler calls `self.indicator.cmd_fill()`. The indicator manager has no idea a button exists anywhere on the device. The GPIO manager has no idea pixels exist. What makes this possible?
- What would happen if you subscribed a second handler to `gpio.button_low` — for example, one that played a sound? Would you need to change anything in the GPIO manager?
- The `update()` method in your application is empty. All the work happens in event handlers. Is this typical? What kind of work *would* belong in `update()`?
