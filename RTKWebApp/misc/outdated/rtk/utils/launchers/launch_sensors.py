import subprocess
import threading
import numpy as np
import argparse


def launch_sensor():
    p = subprocess.Popen(["python2", "launch_sensor.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait()
    print(p.stdout.read())


if __name__ == "__main__":
    parser = argparse.ArgumentParser("SensorLauncher")
    parser.add_argument('--random', type=bool,
                        help='random number of sensors (1 - 10)', default=True)
    parser.add_argument('--n', type=int,
                        help='n simulated sensors', default=-1)
    kwargs = vars(parser.parse_args())
    if kwargs.get("n") > 0:
        count = kwargs.get("n")
    elif kwargs.get("n") < 0 and kwargs.get("random"):
        count = np.random.randint(1, 10)
    else:
        count = 1
    threads = []

    for i in range(count):
        threads.append(threading.Thread(target=launch_sensor))
        threads[-1].start()
