import subprocess
import threading
import numpy as np


def start_sensor():
    p = subprocess.Popen(["python2", "spawn_sensor.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait()
    print(p.stdout.read())


if __name__ == "__main__":

    count = np.random.randint(1, 10)
    threads = []

    for i in range(count):
        threads.append(threading.Thread(target=start_sensor))
        threads[-1].start()