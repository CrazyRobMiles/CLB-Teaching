from managers.base_manager import CLBAppManager


class Manager(CLBAppManager):
    version = "1.0.0"
    name = "Encoder Brightness"
    file = "App_encoder_brightness"
    desc = "Use a rotary encoder to control NeoPixel brightness"

    app_default_settings = {
        "indicator": {
            "enabled": True,
            "pixelpin": 18,
            "count": 8,
            "pixeltype": "RGB",
            "brightness": 1.0
        },
        "rotary_encoder": {
            "enabled": True,
            "encoders": [
                {"name": "brightness", "clk_pin": 16, "dt_pin": 17, "btn_pin": -1}
            ]
        },
        "App_encoder_brightness": {
            "enabled": True,
            "red": 255,
            "green": 100,
            "blue": 0,
            "step": 0.05,
            "dependencies": ["indicator", "rotary_encoder"]
        }
    }

    def __init__(self, clb):
        super().__init__(clb)
        self.indicator = None
        self.brightness = 0.5

    def setup(self, settings):
        super().setup(settings)
        if not self.enabled:
            self.state = self.STATE_DISABLED
            return
        self.red   = self.settings.get("red",   255)
        self.green = self.settings.get("green", 100)
        self.blue  = self.settings.get("blue",    0)
        self.step  = self.settings.get("step",  0.05)
        self.state = self.STATE_OK
        self.set_status(1001, "Encoder Brightness ready")

    def setup_services(self):
        self.indicator = self.get_service_handle("indicator")
        if self.indicator:
            self.indicator.cmd_brightness(self.brightness)
            self.indicator.cmd_fill(self.red, self.green, self.blue)

        cw = self.clb.get_event("rotary_encoder.brightness_moved_clockwise")
        if cw:
            cw.subscribe(self.on_clockwise)

        ccw = self.clb.get_event("rotary_encoder.brightness_moved_anticlockwise")
        if ccw:
            ccw.subscribe(self.on_anticlockwise)

    def on_clockwise(self, event, data):
        self.brightness = min(1.0, self.brightness + self.step)
        if self.indicator:
            self.indicator.cmd_brightness(self.brightness)

    def on_anticlockwise(self, event, data):
        self.brightness = max(0.0, self.brightness - self.step)
        if self.indicator:
            self.indicator.cmd_brightness(self.brightness)

    def update(self):
        if not self.enabled:
            return
