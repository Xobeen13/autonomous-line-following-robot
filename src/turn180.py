import time

class Turn180:
    def __init__(self, turn_pwm=160, duration_s=0.8, settle_s=0.15):
        self.turn_pwm = turn_pwm
        self.duration_s = duration_s
        self.settle_s = settle_s
        self._t0 = None
        self._phase = "idle"

    def start(self, now=None):
        self._t0 = time.time() if now is None else now
        self._phase = "turn"

    def step(self, now=None):
        now = time.time() if now is None else now
        if self._phase == "idle":
            return 0, 0, True
        elapsed = now - self._t0
        if self._phase == "turn":
            if elapsed < self.duration_s:
                return -self.turn_pwm, self.turn_pwm, False
            self._t0 = now
            self._phase = "settle"
            return 0, 0, False
        if self._phase == "settle":
            if elapsed < self.settle_s:
                return 0, 0, False
            self._phase = "done"
            return 0, 0, True
        return 0, 0, True
