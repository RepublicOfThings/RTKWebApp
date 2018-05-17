from .base import Simulator
from rtk.utilities import helpers
import numpy as np
import time


class Sensor(Simulator):
    def __init__(self, wait=0):
        super(Sensor, self).__init__()
        self.wait = wait
        self.dims = "F"
        self.index = 0

    def delay(self):
        time.sleep(self.wait)

    def step(self):
        self.index += 1
        self.wait = np.random.randint(1, 10)
        return self.reading()

    def reading(self):
        return {"reading": "%.2f" % np.random.normal(70.0)}
