from tornado.websocket import WebSocketHandler
from rtk.utilities.helpers import unique_integer
import logging
import json


# message type should be in body of JSON not in header.


class HubHandler(WebSocketHandler):
    things = set()
    web = set()

    def open(self, *args, **kwargs):

        logging.info(self.request)

        ws_type = self.request.headers.get("Socket", "webclient").upper()
        if ws_type == "THING":
            self.uuid = self.request.headers.get("uuid")
            self.cid = unique_integer(list(sorted([x.cid for x in HubHandler.things])))
            logging.info("Connected: {0}:{1}.".format(ws_type, self.uuid))
            HubHandler.things.add(self)
        else:
            self.uuid = self.request.headers.get("Origin", "UNKNOWN_ORIGIN")
            logging.info("Connected: {0}:{1}.".format(ws_type, self.uuid))
            HubHandler.web.add(self)

    def on_close(self):
        if self in HubHandler.things:
            logging.info("Dropped: {0}:{1}.".format("THING", self.uuid))
            HubHandler.send_updates({"type": 1, "data": {"kill": {"uuid": self.uuid}}})
            HubHandler.things.remove(self)
        else:
            logging.info("Dropped Web: {0}:{1}.".format("WEBCLIENT", self.uuid))
            HubHandler.web.remove(self)

    def close(self, **kwargs):
        super(HubHandler, self).close(**kwargs)

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
        data["data"]["cid"] = self.cid
        logging.info("Received data from %r", str(self.uuid))
        HubHandler.send_updates(json.dumps(data))
