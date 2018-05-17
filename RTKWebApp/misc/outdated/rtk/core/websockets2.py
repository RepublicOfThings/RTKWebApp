from tornado import escape
from tornado import gen
from tornado import httpclient
from tornado import httputil
from tornado import ioloop
from tornado import websocket
import json

APPLICATION_JSON = 'application/json'

DEFAULT_CONNECT_TIMEOUT = 60
DEFAULT_REQUEST_TIMEOUT = 60


class WebSocketClient(object):
    """
    Base for web socket clients.
    """

    def __init__(self, address, path="ws", headers={}, connect_timeout=DEFAULT_CONNECT_TIMEOUT,
                 request_timeout=DEFAULT_REQUEST_TIMEOUT):

        self.target = "ws://{address}/{path}".format(address=address, path=path)
        self.connect_timeout = connect_timeout
        self.request_timeout = request_timeout
        self.connect(self.target, headers=headers)

    def connect(self, url, headers={}):
        """
        Connect to the server.
        :param str url: server URL.
        """
        default = {'Content-Type': APPLICATION_JSON}
        headers.update(default)
        headers = httputil.HTTPHeaders(headers)
        request = httpclient.HTTPRequest(url=url,
                                         connect_timeout=self.connect_timeout,
                                         request_timeout=self.request_timeout,
                                         headers=headers)
        ws_conn = websocket.WebSocketClientConnection(ioloop.IOLoop.current(),
                                                      request)
        ws_conn.connect_future.add_done_callback(self._connect_callback)

    def send(self, data):
        """
        Send message to the server
        :param str data: message.
        """
        if not self._ws_connection:
            raise RuntimeError('Web socket connection is closed.')

        self._ws_connection.write_message(escape.utf8(json.dumps(data)))

    def close(self):
        """
        Close connection.
        """

        if not self._ws_connection:
            raise RuntimeError('Web socket connection is already closed.')

        self._ws_connection.close()

    def _connect_callback(self, future):
        if future.exception() is None:
            self._ws_connection = future.result()
            self._on_connection_success()
            self._read_messages()
        else:
            self._on_connection_error(future.exception())

    @gen.coroutine
    def _read_messages(self):
        while True:
            msg = yield self._ws_connection.read_message()
            if msg is None:
                self._on_connection_close()
                break

            self._on_message(msg)

    def _on_message(self, msg):
        """This is called when new message is available from the server.
        :param str msg: server message.
        """

        pass

    def _on_connection_success(self):
        """This is called on successful connection ot the server.
        """
        pass

    def _on_connection_close(self):
        """This is called when server closed the connection.
        """
        pass

    def _on_connection_error(self, exception):
        """This is called in case if connection to the server could
        not established.
        """

        pass