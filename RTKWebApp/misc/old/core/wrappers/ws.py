import websocket
import socket
import logging


class WebSocketWrapper(object):
    def __init__(self, address="localhost:8888", path="ws", trace=False, header={}, **kwargs):
        """
        A wrapper abstract-class for a WebSocketApp.

        Parameters
        ----------

        """
        self.target = "ws://{address}/{path}".format(address=address, path=path)
        self.header = header
        self.trace(trace)
        self.socket = self.connect(**kwargs)

    def on_message(self, socket, message):
        pass

    def on_data(self, socket, data, *args, **kwargs):
        pass

    def on_error(self, socket, exception):
        pass

    def on_close(self, socket):
        pass

    def on_ping(self, *args, **kwargs):
        pass

    def on_pong(self, *args, **kwargs):
        pass

    def on_cont_message(self, socket, message, flag):
        raise NotImplementedError

    def on_open(self, socket):
        pass

    def connect(self, **kwargs):
        self.socket = websocket.WebSocketApp(self.target,
                                      on_message=self.on_message,
                                      on_cont_message=self.on_cont_message,
                                      on_close=self.on_close,
                                      on_data=self.on_data,
                                      on_ping=self.on_ping,
                                      on_pong=self.on_pong,
                                      header=self.header,
                                      **kwargs)
        self.socket.on_open = self.on_open
        return self.socket

    def run_forever(self, ping=10.0, pong=1.0, *args, **kwargs):
        self.socket.run_forever(ping_interval=ping, ping_timeout=pong, *args, **kwargs)

    def close(self, **kwargs):
        self.socket.close(**kwargs)

    def send(self, data):
        try:
            self.socket.send(str(data))
        except socket.error as error:
            self.on_error(self, error)
        except websocket._exceptions.WebSocketConnectionClosedException as error:
            self.on_error(self, error)
        except Exception as error:
            self.on_error(self, error)

    @staticmethod
    def trace(state):
        websocket.enableTrace(state)
