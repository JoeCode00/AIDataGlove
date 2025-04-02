from time import time


class Timer:
    def __init__(self):
        self.origin = time()
        self.timer_durration = 0
        self.timer_start_time = 0
        self.time_at_last_poll = self.origin
        self.current_time = self.origin
        self.time_since_last_poll = 0

    def update(self):
        self.current_time = time()
        self.time_since_last_poll = self.current_time - self.time_at_last_poll
        self.time_at_last_poll = time()

    def now(self):
        self.update()
        return self.current_time - self.origin

    def current(self):
        self.update()
        return self.current_time

    def start(self, durration: float | int):
        self.update()
        if durration <= 0:
            raise ValueError(f"Durration must be positive, not {durration}.")
        self.timer_durration = durration
        self.timer_start_time = self.now()

    def complete(self, new_durration: float | int = None):
        self.update()
        if new_durration is not None:
            if self.now() >= self.timer_start_time + new_durration:
                return True

        if self.now() >= self.timer_start_time + self.timer_durration:
            return True
        else:
            return False
