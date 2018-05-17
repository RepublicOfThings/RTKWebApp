from rtk.utils import processing
from rtk.core import mqtt
import json


def model_selector(**config):
    return ""


class RTKMQTTFilter(mqtt.MQTTWrapper):
    def __init__(self, uuid=None, config={}, topic="/filter/{0}", target="/sensor/{0}", **kwargs):
        self._model = model_selector(**config)  # replace with model
        self.type = type(self._model).__name__
        if uuid is None:
            uuid = -1
        self.uuid = uuid
        self.topic = topic.format(self.uuid)
        subscriptions = [target.format(uuid)]
        super(RTKMQTTFilter, self).__init__(subscriptions=subscriptions, listen=True, **kwargs)

    @processing.mqtt_json_input
    def on_message(self, client, user_data, message):
        print(message)

    @classmethod
    def from_json(cls, filename):
        config = json.load(open(filename, "r"))
        return cls(id=config["uuid"],
                   topic=config["topic"],
                   target=config["target"],
                   config=config["model"])
