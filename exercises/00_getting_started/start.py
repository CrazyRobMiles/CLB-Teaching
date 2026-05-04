import time
from managers.base_manager import CLBAppManager


class Manager(CLBAppManager):
    version = "1.0.0"
    name = "Hello CLB"
    file = "App_hello_clb"
    desc = "Confirms the CLB framework is installed and running"

    app_default_settings = {
        "App_hello_clb": {
            "enabled": True,
            "dependencies": []
        }
    }

    def __init__(self, clb):
        super().__init__(clb)
        self._last_heartbeat = 0

    def setup(self, settings):
        super().setup(settings)
        if not self.enabled:
            self.state = self.STATE_DISABLED
            return
        self.state = self.STATE_OK
        self._last_heartbeat = time.ticks_ms()
        print("CLB framework is running!")
        print("Type 'status' to see all manager states.")
        self.set_status(1000, "Hello CLB ready")

    def update(self):
        if not self.enabled:
            return
        now = time.ticks_ms()
        if time.ticks_diff(now, self._last_heartbeat) >= 5000:
            self._last_heartbeat = now
            print("CLB is alive!")
