import time

class PickupAction:
    def __init__(self, hold_s=6.0):
        self.hold_s = hold_s
        self._t0 = None
        self._sent = False

    def start(self, now=None):
        self._t0 = time.time() if now is None else now
        self._sent = False

    def step(self, driver, now=None):
        now = time.time() if now is None else now
        if not self._sent:
            if driver is not None:
                driver.send_pickup()
            self._sent = True
            self._t0 = now
            return False
        return (now - self._t0) >= self.hold_s
