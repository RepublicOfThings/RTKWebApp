from .base import RTKMQTTSensor
from rtk.sensors.sensors import simulations


class RTKMQTTTemperatureSensor(RTKMQTTSensor):
    def __init__(self, config={}, auto=True, **kwargs):
        super(RTKMQTTTemperatureSensor, self).__init__(simulations.SimulatedTemperatureSensor(**config))
        if auto:
            self.start()
