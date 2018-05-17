from rtk.core import RTKWebSocketWrapper, generators
import json
import logging


class RTKWebsocketSensor(RTKWebSocketWrapper):
    def __init__(self,
                 host="localhost",
                 port=8888,
                 path="ws",
                 trace=False,
                 header={},
                 generator=generators.NormalGenerator,
                 *args, **kwargs):

        super(RTKWebsocketSensor, self).__init__(host=host, port=port, path=path, trace=trace, header=header)
        self._generator = generator(*args, **kwargs)

    def on_open(self, socket):
        for element in self._generator.start():
            if self.socket.sock.connected:
                self.send({"measurement": element})
            else:
                break

    def on_error(self, socket, exception):
        logging.error("Shutting down: exception {0}".format(exception))
        self.socket.sock.connected = False
        self.close()

    def on_close(self, *args, **kwargs):
        pass

    def send(self, data):
        super(RTKWebsocketSensor, self).send(json.dumps(data))