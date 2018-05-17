from .base import Simulator
import numpy as np
import time


class Sensor(Simulator):
    def __init__(self, data, wait=0):
        super(Sensor, self).__init__()
        self.wait = wait
        self.dims = "F"
        self.data = data
        self.index = 0

    def delay(self):
        time.sleep(self.wait)

    def step(self):
        if self.index >= len(self.data):
            self.index = 0
        self.wait = np.random.randint(1, 10)
        reading = self.reading()
        self.index += 1
        return reading

    def reading(self):
        return {"reading": "%.2f" % self.data[self.index]}
