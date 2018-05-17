from rtk.sensors.sensors import RTKWebSocketSensor, simulations
import json


class RTKTemperatureSensor(RTKWebSocketSensor):
    def __init__(self, sensor={}, ws={}):
        sim = simulations.SimulatedTemperatureSensor(**sensor)
        super(RTKTemperatureSensor, self).__init__(sim=sim, **ws)

    def launch(self):
        self.run_forever()

    @classmethod
    def from_json(cls, filename):
        data = json.load(open(filename, "r"))

        # block should be replaced -- make uuid visible in a better way (why have it stored in three places?) fool
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data):
        sensor = data.get("sensor")
        ws = data.get("ws", {})
        sensor["uuid"] = data["uuid"]
        ws["uuid"] = data["uuid"]
        ws["header"]["uuid"] = data["uuid"]

        obj = cls(sensor=sensor, ws=ws)
        if data.get("launch", False):
            obj.launch()
        return obj