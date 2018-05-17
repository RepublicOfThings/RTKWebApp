from rtk.sensors import RTKTemperatureSensor
import argparse
import uuid

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser("SensorLauncher")
    parser.add_argument('--port', type=int,
                        help='target port', default=8888)
    parser.add_argument('--address', type=str,
                        help='target address', default="localhost")
    parser.add_argument('--path', type=str,
                        help='target path', default="ws")
    parser.add_argument('--trace', type=bool,
                        help='target path', default=True)
    parser.add_argument('--uuid', type=str,
                        help='device uuid', default=str(uuid.uuid4()))

    kwargs = vars(parser.parse_args())
    address = "{0}:{1}".format(kwargs.get("address"), kwargs.get("port"))
    profile["uuid"] = kwargs.get("uuid")
    print(profile)
    sensor = RTKTemperatureSensor.from_dict(profile)
