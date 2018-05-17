from rtk.core import DeviceSim
from rtk.core import Counter
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser("SimThing v0.0.1")
    parser.add_argument('--port', type=int,
                        help='target port', default=8888)
    parser.add_argument('--address', type=str,
                        help='target address', default="localhost")
    parser.add_argument('--path', type=str,
                        help='target path', default="")
    parser.add_argument('--trace', type=bool,
                        help='target path', default=True)

    kwargs = vars(parser.parse_args())
    address = "{0}:{1}".format(kwargs.get("address"), kwargs.get("port"))

    sim = DeviceSim(sim=Counter(wait=0.1),
                   header={"socket": "thing"},
                   address=address,
                   path=kwargs.get("path"),
                   trace=kwargs.get("trace"))
    sim.run_forever()
