from .device import Device
from rtk.core.simulators import Simulator
from rtk.utilities import json_output
from rtk.utilities import helpers
import numpy as np


class DeviceSim(Device):
    def __init__(self, sim=None, **kwargs):
        self._sim = sim
        self.type = type(sim).__name__
        super(DeviceSim, self).__init__(**kwargs)

    @property
    def simulator(self):
        return self._sim

    @simulator.setter
    def simulator(self, value):
        if issubclass(type(value), Simulator):
            self._sim = value

    def on_open(self, socket):
        print("SimThing: Connection opened.")
        self.start()

    def on_data(self, socket, data, *args, **kwargs):
        pass

    def on_message(self, socket, message):
        pass

    def on_close(self, socket):
        print("SimThing: Connection closed.")

    def on_cont_message(self, socket, message, flag):
        pass

    def on_error(self, socket, exception):
        pass

    def on_ping(self, socket):
        pass

    def on_pong(self, socket):
        pass

    def start(self, *args, **kwargs):
        for output in self._sim(*args, **kwargs):
            data = {"type": 0,
                    "data": {
                        "uuid": self.uuid,
                        "value": output["reading"],
                        "units": self._sim.dims,
                        "conf": str(np.random.randint(95, 100)) + "%",
                        "sconf": str(np.random.randint(95, 100)) + "%",
                        "type": self.type,
                        "status": "Okay",
                    }}
            self.send(data)

    def stop(self):
        self._sim.active = False
        self.close()

    @json_output
    def send(self, data):
        return super(DeviceSim, self).send(data)
