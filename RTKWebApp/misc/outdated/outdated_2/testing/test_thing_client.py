# from rtk.core import RTKWebSocketWrapper
from rtk.sensors import WSSensor
import uuid
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser("TestWSClient")
    parser.add_argument('--port', type=int,
                        help='target port', default=8888)
    parser.add_argument('--address', type=str,
                        help='target address', default="localhost")
    parser.add_argument('--path', type=str,
                        help='target path', default="ws")
    parser.add_argument('--trace', type=bool,
                        help='target path', default=True)

    kwargs = vars(parser.parse_args())

    address = "{0}:{1}".format(kwargs.get("address"), kwargs.get("port"))

    ws = GenericSensor(wait=1, address=address, path=kwargs.get("path"), header={"CLIENT_TYPE": "thing",
                                                                        "uuid": str(uuid.uuid4())}, trace=True)
    ws.run_forever()



"""
python2 create_sensor.py --address localhost --port 8888 --path ws --trace True
"""