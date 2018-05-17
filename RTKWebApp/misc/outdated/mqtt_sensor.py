from rtk.core import RTKMQTTWrapper, generators
import json
import time


class RTKMQTTSensor(RTKMQTTWrapper):
    def __init__(self,
                 sensor_id="",
                 delay=0.5,
                 topic_fmt="/rtk/sensor/{0}",
                 config={"loc": 0.0, "scale": 1.0},
                 generator=generators.NormalGenerator, **kwargs):

        super(RTKMQTTSensor, self).__init__(client_id=sensor_id, **kwargs)
        self._topic = topic_fmt.format(sensor_id)
        self._generator = generator(**config)
        self._delay = delay

    def mainloop(self):
        for element in self._generator.start():
            self.publish(self._topic, json.dumps(element, indent=4))
            time.sleep(self._delay)

