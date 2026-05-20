# Lab 5: CLB Events

The `hcsr04` manager publishes four events that application managers can subscribe to. This is the same publish/subscribe system you used in earlier exercises — the distance sensor integrates with the rest of the CLB framework without any custom wiring between managers.

---

## Published events

| Event name | When it fires | Data payload |
|------------|---------------|--------------|
| `hcsr04.reading` | Every completed measurement | `{distance_mm, duration_us}` |
| `hcsr04.below_threshold` | Distance transitions from above to below `threshold_mm` | `{distance_mm, threshold_mm}` |
| `hcsr04.above_threshold` | Distance transitions from below to above `threshold_mm` | `{distance_mm, threshold_mm}` |
| `hcsr04.timeout` | No echo received within 500 ms of a trigger | `{last_trigger_ms}` |

The threshold events are **edge-triggered**: they fire once when the distance crosses the threshold, not continuously while the condition holds. Moving an object from 500 mm to 100 mm fires `hcsr04.below_threshold` once; holding it there produces no further threshold events. Moving it back above 300 mm fires `hcsr04.above_threshold` once.

---

## Subscribing from an application manager

The pattern is identical to subscribing to GPIO events in the Button Light exercise. Here is an application that lights up a NeoPixel strip when something moves within range:

```python
from managers.base_manager import CLBAppManager

class Manager(CLBAppManager):
    version = "1.0.0"
    name = "Proximity Alert"
    file = "App_proximity_alert"
    desc = "Lights pixels when something is within range"

    app_default_settings = {
        "App_proximity_alert": {
            "enabled": True,
            "dependencies": ["indicator", "hcsr04"]
        },
        "indicator": {
            "enabled": True,
            "pixelpin": 18,
            "count": 8
        },
        "hcsr04": {
            "enabled": True,
            "trigger_pin": 5,
            "echo_pin": 18,
            "threshold_mm": 300
        }
    }

    def setup(self, settings):
        super().setup(settings)
        self.state = self.STATE_OK

    def setup_services(self):
        super().setup_services()
        self.indicator = self.clb.get_service_handle("indicator")

        # Subscribe to threshold crossing events
        self.clb.get_event("hcsr04.below_threshold").subscribe(self._on_approach)
        self.clb.get_event("hcsr04.above_threshold").subscribe(self._on_retreat)

        # Start the sensor
        self.clb.get_service_handle("hcsr04").command_start()

    def _on_approach(self, event, data):
        self.indicator.cmd_fill(255, 80, 0)   # amber when close

    def _on_retreat(self, event, data):
        self.indicator.cmd_fill(0, 0, 0)       # off when far

    def update(self):
        pass
```

---

## Subscribing to every reading

If you need a continuous stream of distances — for example, to display the value on a screen or control motor speed — subscribe to `hcsr04.reading` instead:

```python
def setup_services(self):
    super().setup_services()
    self.clb.get_event("hcsr04.reading").subscribe(self._on_reading)
    self.clb.get_service_handle("hcsr04").command_start()

def _on_reading(self, event, data):
    distance_mm = data["distance_mm"]
    # use distance_mm however you like
```

---

## Handling timeouts

A timeout means the sensor fired but received no echo. Register a handler if your application needs to respond to out-of-range conditions:

```python
self.clb.get_event("hcsr04.timeout").subscribe(self._on_timeout)

def _on_timeout(self, event, data):
    # Target out of range or beam missed — treat as "very far"
    self.indicator.cmd_fill(0, 0, 0)
```

---

## What makes this design useful

The `hcsr04` manager has no knowledge of the indicator manager. The indicator manager has no knowledge of the distance sensor. They are decoupled entirely — connected only through event name strings.

This means you can swap the sensor, change the pin assignment, or replace the indicator with a buzzer or a motor command by editing one manager without touching the other. The same pattern scales from a single sensor to a device with dozens of inputs and outputs.
