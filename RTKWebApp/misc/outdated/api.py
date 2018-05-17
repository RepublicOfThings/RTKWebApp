from .interface import RTKInterface
import functools
import json


API = RTKInterface()

API_MAP = {
            "GET": {
                    (): lambda: "API Ready",
                    # ("help"): lambda: "API Help",
                    ("data", "filter"): API.filter_data,
                    },
            "POST": {
                    ("create", "filter"): API.create_filter,
                    ("launch", "filter"): API.launch_filter,
                    ("delete", "filter"): API.delete_filter,
                    ("create", "sensor"): API.create_sensor,
                    ("launch", "sensor"): API.launch_sensor,
                    ("delete", "sensor"): API.delete_sensor
            },
        }


def rtk_call(call_type):
    def outer(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            args = tuple(str(x) for x in args)
            if self.request.body == "":
                data = {}
            else:
                data = json.loads(self.request.body)

            return method(self, API_MAP.get(call_type, {}).get(args), data, **kwargs)
        return wrapper
    return outer


class APIHandler(BaseHandler):
    # @tornado.web.authenticated
    @rtk_call("GET")
    def get(self, func, data, *args, **kwargs):
        self.write(func(**data))

    def put(self, *args, **kwargs):
        pass

    # @tornado.web.authenticated
    @rtk_call("POST")
    def post(self, func, data, *args, **kwargs):
        self.write(func(**data))

    def delete(self, *args, **kwargs):
        pass