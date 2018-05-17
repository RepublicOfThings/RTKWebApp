from rtk.core import websockets, simulators
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser("SimThing")
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

    sim = websockets.DeviceSim(sim=simulators.Sensor(),
                   header={"socket": "thing"},
                   address=address,
                   path=kwargs.get("path"),
                   trace=kwargs.get("trace"))
    sim.run_forever()

"""
python2 create_sensor.py --address localhost --port 8888 --path ws --trace True
"""