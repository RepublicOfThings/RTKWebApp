from rtk.sensors import RTKTemperatureSensor, RTKMQTTTemperatureSensor
import json
import uuid
import numpy as np

#ws_sensor = RTKTemperatureSensor.from_json("ws_sensor.json")
# mqtt_sensor = RTKMQTTTemperatureSensor.from_json("mqtt_sensor.json")

profile = {
  "uuid": "892f9739-182d-40f6-98eb-186c6c41f0ea",
  "launch": True,
  "ws": {
    "address": "localhost:8888",
    "path": "ws",
    "trace": True,
    "header": {
      "type": "sensor"
    }
  },
  "sensor": {
    "loc": 0.0,
    "scale": 1.0,
    "units": "F"
  }
}

for i in range(np.random.randint(3, 10)):
    profile["uuid"] = str(uuid.uuid4())
    sensor = RTKTemperatureSensor.from_dict(profile)
