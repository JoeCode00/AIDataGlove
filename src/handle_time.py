from time import time

class Timer():
    def __init__(self, *args, **kwargs):
        self.origin = time()
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