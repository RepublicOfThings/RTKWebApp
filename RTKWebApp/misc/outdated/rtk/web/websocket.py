from tornado.websocket import WebSocketHandler
from rtk.utils.helpers import unique_integer
import logging
import json
import uuid


# message type should be in body of JSON not in header (no body sent with open request currently).


class RTKWebSocketHandler(WebSocketHandler):
    sensors = set()
    web = set()

    def __init__(self, *args, **kwargs):
        self.uuid = None
        super(RTKWebSocketHandler, self).__init__(*args, **kwargs)

    def open(self, *args, **kwargs):
        client_type = self.request.headers.get("Socket", "webclient").upper()
        print client_type, self.request.headers
        if client_type == "THING":
            self.uuid = self.request.headers.get("uuid")
            self.cid = unique_integer(list(sorted([x.cid for x in RTKWebSocketHandler.sensors])))
            logging.info("Connected: {0}:{1}.".format(client_type, self.uuid))
            RTKWebSocketHandler.sensors.add(self)
        else:
            self.uuid = str(uuid.uuid4())
            logging.info("Connected: {0}:{1}.".format(client_type, self.uuid))
            RTKWebSocketHandler.web.add(self)

    def on_close(self):
        if self in RTKWebSocketHandler.sensors:
            logging.info("Dropped: {0}:{1}.".format("THING", self.uuid))
            RTKWebSocketHandler.send_updates({"type": "action", "data": {"kill": {"uuid": self.uuid}}})
            RTKWebSocketHandler.sensors.remove(self)
        else:
            logging.info("Dropped Web: {0}:{1}.".format("WEBCLIENT", self.uuid))
            RTKWebSocketHandler.web.remove(self)

    def close(self, **kwargs):
        super(RTKWebSocketHandler, self).close(**kwargs)

    @classmethod
    def send_updates(cls, data):
        logging.info("Forwarding to %d web clients.", len(cls.web))
        for client in cls.web:
            try:
                client.write_message(data)
            except Exception as error:
                logging.error("couldn't send data to client ({0})".format(error.message), exec_info=True)

    def on_message(self, data):
        data = json.loads(data)
        data["payload"]["cid"] = self.cid
        logging.info("Received data from %r", str(self.uuid))
        RTKWebSocketHandler.send_updates(json.dumps(data))
