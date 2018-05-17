import threading
from rtk.sensors import RTKTemperatureSensor


STOPPED = -1
READY = 0
ACTIVE = 1


class BaseThread(threading.Thread):
    def __init__(self, uuid=None, config={}, *args, **kwargs):
        self.id = uuid
        self.__status = READY
        self.__running = False
        self.variant = type(self).__name__
        self.config = config
        super(BaseThread, self).__init__(*args, **kwargs)

    @property
    def status(self):
        return self.__status

    @property
    def running(self):
        if self.__status == 1:
            return True
        else:
            return False


class SensorThread(BaseThread):
    def __init__(self, *args, **kwargs):
        super(SensorThread, self).__init__(*args, **kwargs)
        self.device = RTKTemperatureSensor.from_dict(kwargs.get("config"))

    def run(self):
        self.device.run_forever()
