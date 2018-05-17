import json


class ResponseModel(object):
    def __init__(self, status, message, payload):
        self._status = status
        self._message = message
        self._payload = payload

    def __repr__(self):
        return "<RTKResponse[{0}]>".format(self._status)

    @property
    def data(self):
        return {
                "statusCode": self._status,
                "responseMsg": self._message,
                "payload": self._payload
            }

    @property
    def json(self):
        return json.dumps(self.data)