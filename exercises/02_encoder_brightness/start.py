from managers.base_manager import CLBAppManager


class Manager(CLBAppManager):
    version = "1.0.0"
    name = "Encoder Brightness Start"
    file = "App_encoder_brightness_start"
    desc = "Exercise 02 starting point — skeleton with no hardware attached"

    app_default_settings = {
        "App_encoder_brightness_start": {
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
        self.set_status(1001, "Encoder Brightness ready")

    def update(self):
        if not self.enabled:
            return
