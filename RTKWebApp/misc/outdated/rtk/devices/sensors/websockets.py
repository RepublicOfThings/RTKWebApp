from rtk.core import WebSocketWrapper, BaseSimulator
from rtk.utils import processing
import uuid


class RTKWebSocketSensor(WebSocketWrapper):
    def __init__(self, sim=None, id=None, **kwargs):
        self._sim = sim
        self.uuid = id or str(uuid.uuid4())
        self.type = type(sim).__name__
        super(RTKWebSocketSensor, self).__init__(header={"type": "sensor", "uuid": self.uuid}, **kwargs)

    @property
    def simulator(self):
        return self._sim

    @simulator.setter
    def simulator(self, value):
        if issubclass(type(value), BaseSimulator):
            self._sim = value

    def on_open(self, socket):
        print("SimThing: Connection opened.")
        self.start()

    def on_data(self, socket, data, *args, **kwargs):
        pass

    def on_message(self, socket, message):
        pass

    def on_close(self, socket):
        print("SimThing: Connection closed.")

    def on_cont_message(self, socket, message, flag):
        pass

    def on_error(self, socket, exception):
        pass

    def on_ping(self, socket):
        pass

    def on_pong(self, socket):
        pass

    def start(self, *args, **kwargs):
        for output in self._sim(*args, **kwargs):
            self.send(output)

    def stop(self):
        self._sim.active = False
        self.close()

    @processing.json_output
    def send(self, data):
        return super(RTKWebSocketSensor, self).send(data)
