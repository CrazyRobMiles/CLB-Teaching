# Part 5: Customise and Explore

Your application now works. These changes require only a `set` command — no code edits and no reboot:

**Change the colour:**
```
set App_button_light.on_red=0
set App_button_light.on_green=0
set App_button_light.on_blue=255
```
Press the button. The pixels are now blue. The new values are saved to `settings.json` and will survive reboot.

**Change the number of pixels:**
```
set indicator.count=4
```
Reboot. Only four pixels light up.

Now try some code changes in the editor on this page:

- Make the pixels turn a different colour on long press (you will need to track time in `update()`)
- Make the pixels fade out gradually after release instead of turning off immediately
- Subscribe to both `button_low` and `button_high` with a single handler that uses `data` to determine which event fired

---

# Using the AI Assistant

If this class has AI assistance available, you can use the `ask` command from the REPL:

```
ask <your question>
```

The assistant knows what this exercise is about and what you are expected to figure out yourself. Getting useful help requires describing what you observe precisely:

**Not useful:**
```
ask it doesn't work
```

**Useful:**
```
ask the indicator manager shows STATE_OK in the status output but when I press
the button nothing happens. There are no errors in the console. The gpio
manager also shows STATE_OK.
```

The second description tells the assistant: what you expected, what actually happened, what you have already checked, and what the relevant manager states are. That is enough to diagnose most problems.

If you are not sure what to observe, check:

1. `status` — what state is each manager in?
2. The console output since the last reboot — any errors?
3. Whether the event is firing at all (add `print("button pressed")` to your handler temporarily)
4. Whether the service call is reaching the indicator manager (try calling `indicator.fill 255 0 0` directly from the REPL)

Forming a precise description of a broken system is itself an engineering skill. The discipline of separating *what I expected* from *what I observed* from *what I have already tried* is the same process used to write a useful bug report, ask a useful question on a forum, or brief a colleague on a problem.

---

# Reference: What You Built

```
┌─────────────────────────────────────────────────────┐
│  App_button_light  (CLBAppManager)                  │
│                                                     │
│  app_default_settings defines:                      │
│    indicator ──► pixelpin, count, ...               │
│    gpio      ──► input_pins: [{name:"button",pin:14}│
│    App_button_light ──► on_red, on_green, on_blue   │
│                                                     │
│  setup_services():                                  │
│    get_service_handle("indicator") ─► self.indicator│
│    subscribe gpio.button_low  ──► on_button_pressed │
│    subscribe gpio.button_high ──► on_button_released│
│                                                     │
│  on_button_pressed:  indicator.cmd_fill(r, g, b)    │
│  on_button_released: indicator.cmd_fill(0, 0, 0)    │
└─────────────────────────────────────────────────────┘
         │ service call              │ event subscription
         ▼                          ▼
┌─────────────────┐      ┌──────────────────────┐
│indicator manager│      │ gpio manager         │
│(CLBDeviceManager)      │ (CLBDeviceManager)   │
│                 │      │                      │
│ cmd_fill(r,g,b) │      │ publishes:           │
│ cmd_set(i,r,g,b)│      │  gpio.button_low     │
│ cmd_fade(i,...) │      │  gpio.button_high    │
└─────────────────┘      └──────────────────────┘
```

The indicator manager does not know the button exists.  
The GPIO manager does not know the pixels exist.  
Your application connects them — and is the only place that knows about both.

This separation is the same pattern used in professional embedded systems, distributed services, and event-driven architectures at any scale.
