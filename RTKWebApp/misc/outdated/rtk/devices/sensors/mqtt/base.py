from rtk.utils import processing
from rtk.core import mqtt, BaseSimulator


class RTKMQTTSensor(mqtt.MQTTWrapper):
    def __init__(self, sim=None, id=None, topic="/sensor/{0}", **kwargs):
        self._sim = sim
        self.uuid = id
        self.type = type(sim).__name__
        self.topic = topic.format(self.uuid)
        super(RTKMQTTSensor, self).__init__(**kwargs)

    @property
    def simulator(self):
        return self._sim

    @simulator.setter
    def simulator(self, value):
        if issubclass(type(value), BaseSimulator):
            self._sim = value

    def on_connect(self, client, user_data, flags, response):
        self.start()

    def start(self, *args, **kwargs):
        for output in self._sim(*args, **kwargs):
            self.send(output)

    @processing.json_output
    def send(self, data, *args, **kwargs):
        # topic, payload=None, qos=0, retain=False
        self.publish(self.topic, data, *args, **kwargs)
