from rtk.core import BaseSensor
import numpy as np


class SimulatedTemperatureSensor(BaseSensor):
    def __init__(self, uuid=None, units="F", loc=0.0, scale=1.0, *args, **kwargs):
        self.loc, self.scale = loc, scale
        self.uuid = uuid
        super(SimulatedTemperatureSensor, self).__init__(units=units, *args, **kwargs)

    def measure(self):
        reading = np.random.normal(self.loc, self.scale)
        measurement_confidence = str(np.random.randint(95, 100))
        set_confidence = str(np.random.randint(95, 100))
        data = {"type": "sensor",
                "payload": {
                    "uuid": self.uuid,
                    "value": "%.2f" % reading,
                    "units": self.units,
                    "conf":  measurement_confidence + "%",
                    "sconf": set_confidence + "%",
                    "type": "temperature",
                    "status": "Okay",
                }}
        return data
