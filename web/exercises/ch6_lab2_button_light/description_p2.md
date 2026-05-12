# Part 2: Create the Skeleton Application

The editor on this page has already loaded the starting file for you. It contains a minimal working application with no behaviour yet:

```python
from managers.base_manager import CLBAppManager

class Manager(CLBAppManager):
    version = "1.0.0"
    name = "Button Light"
    file = "App_button_light"
    desc = "Lights up pixels when a button is pressed"

    app_default_settings = {
        "App_button_light": {
            "enabled": True,
            "dependencies": []
        }
    }

    def __init__(self, clb):
        super().__init__(clb)

    def setup(self, settings):
        super().setup(settings)
        if not self.enabled:
            self.state = self.STATE_DISABLED
            return
        self.state = self.STATE_OK
        self.set_status(1001, "Button Light ready")

    def update(self):
        if not self.enabled:
            return
```

Make a copy of this file and name it `App_button_light_manager.py`. This is the file you will build on. Save it to the device.

Now load it from the REPL:

```
select-app Button Light
```

The device reboots. When it comes back up, check the manager status:

```
status
```

**What you should see:** The `App_button_light` manager appears in the list with state `ok`. No other managers are loaded. Nothing visible happens — the application has no hardware yet.

### Think About It

- Why does only `App_button_light` appear? Look at `app_default_settings` — what does it say to load?
- What would you need to add to make the `indicator` manager load?
- The `update()` method currently returns immediately. What would happen if it contained `time.sleep(1)`?
