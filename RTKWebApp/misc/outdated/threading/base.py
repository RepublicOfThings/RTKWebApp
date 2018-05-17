import threading
from rtk.core import DeviceSim, Sensor


class RTKThread(threading.Thread):
    def __init__(self, id, *args, **kwargs):
        self.id = id
        self.running = False
        self.variant = type(self).__name__
        super(RTKThread, self).__init__(*args, **kwargs)

    def status(self):
        if self.running:
            return "active", 0

    def stop(self):
        pass


class RTKFilterThread(RTKThread):
    def __init__(self, *args, **kwargs):
        self.filter = kwargs.get("config")
        super(RTKFilterThread, self).__init__(*args, **kwargs)

    def run(self):
        pass


class RTKSensorThread(RTKThread):
    def __init__(self, *args, **kwargs):
        self.sensor = DeviceSim(sim=Sensor(), **kwargs.get("config"))
        del kwargs["config"]
        super(RTKSensorThread, self).__init__(*args, **kwargs)

    def run(self):
        self.running = True
        self.sensor.run_forever()

    def stop(self):
        self.running = False
        self.sensor.stop()
