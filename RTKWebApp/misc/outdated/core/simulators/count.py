from .base import Simulator
import time


class Counter(Simulator):
    def __init__(self, wait=0):
        """
        Simulator that counts indefinitely.

        Parameters
        ----------
        wait: numeric
            Time to wait in seconds.

        """
        super(Counter, self).__init__()
        self.wait = wait
        self.count = 0

    def delay(self):
        time.sleep(self.wait)

    def step(self):
        self.count += 1
        data = {"count": self.count}
        return data
