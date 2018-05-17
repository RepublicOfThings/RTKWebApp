from .wrapper import RTKMQTTDevice
import json
import uuid


class RTKMQTTSensor(RTKMQTTDevice):

    @classmethod
    def from_json(cls, filename):
        data = json.load(open(filename))
        broker = data.get("broker")
        sid = str(data.get("id", uuid.uuid4()))
        host = str(broker.get("host", "localhost"))
        port = int(broker.get("port", 1883))
        sensor = cls(host, id=sid, port=port)
        sensor.config = data
        sensor.target = "sensors/RTK:{0}".format(sid)
        return sensor

    def loop_forever(self, simulation=None, **kwargs):
        if simulation is not None:
            for output in simulation():
                output["units"] = self.config["measurements"]["temperature"]["dims"]
                self.publish(self.target, json.dumps(output), **kwargs)
