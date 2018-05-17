from .wrapper import RTKMQTTDevice
import json
import uuid


class RTKMQTTFilter(RTKMQTTDevice):
    @classmethod
    def from_json(cls, filename, **kwargs):
        data = json.load(open(filename))
        broker = data.get("broker")
        sid = str(data.get("id", uuid.uuid4()))
        host = str(broker.get("host", "localhost"))
        port = int(broker.get("port", 1883))
        subs = [str(x) for x in data.get("subscribe_to", [])]
        sensor = cls(host, id=sid, port=port, subscriptions=subs, **kwargs)
        return sensor

    def on_subscribe(self, client, user_data, mid_var, qos):
        print(mid_var, qos)

    def filter(self, vector):
        return vector

    def on_message(self, client, user_data, message):
        data = json.loads(message.payload)
        data["filtered"] = {"temp": {"value": float(data["readings"][0]), "pval": 0.0}}
        self.publish("filters/RTK:d5d8a564-c005-4337-9fb6-bb091d2d1cec", json.dumps(data))