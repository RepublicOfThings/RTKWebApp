from .client import BaseClient
import socket
import websocket


class WebSocketClient(BaseClient):
    def __init__(self, host="localhost", port=8888, path="ws", client_id="", trace=False, header={}, **kwargs):
        super(WebSocketClient, self).__init__(client_id)
        self.host, self.port, self.path, self._trace, self.header = host, port, path, trace, header
        self.address = "ws://{host}:{port}/{path}".format(host=host, port=port, path=path)
        self.trace(trace)
        self.socket = self.connect(**kwargs)

    def update_config(self, **config):
        pass

    def send(self, payload=None):
        try:
            self.socket.send(str(payload))
        except socket.error as error:
            self.on_error(self, error)
        except websocket._exceptions.WebSocketConnectionClosedException as error:
            self.on_error(self, error)
        except Exception as error:
            self.on_error(self, error)

    def connect(self, **kwargs):
        self.socket = websocket.WebSocketApp(self.address,
                                             on_message=self.on_message,
                                             on_cont_message=self.on_cont_message,
                                             on_close=self.on_close,
                                             on_data=self.on_data,
                                             on_open=self.on_open,
                                             on_ping=self.on_ping,
                                             on_pong=self.on_pong,
                                             header=self.header,
                                             **kwargs)
        return self.socket

    def set_method(self, method, value):
        setattr(self.socket, method, value)

    def mainloop(self, *args, **kwargs):
        pass

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

    def run_forever(self, ping=10.0, pong=1.0, *args, **kwargs):
        self.socket.run_forever(ping_interval=ping, ping_timeout=pong, *args, **kwargs)

    def close(self, **kwargs):
        self.socket.close(**kwargs)

    def to_dict(self, *args, **kwargs):
        return {
                "client_id": self.cid,
                "host": self.host,
                "port": self.port,
                "path": self.path,
                "header": self.header,
                "trace": self._trace
            }

    @classmethod
    def from_dict(cls, **kwargs):
        return cls(**kwargs)

    def trace(self, state):
        self._trace = state
        websocket.enableTrace(state)
