import json
from rtk.deployment import RTKNetwork


def json_output(func):
    def wrapped_func(*args, **kwargs):
        return json.dumps(func(*args, **kwargs))
    return wrapped_func


class RTKInterface(object):
    def __init__(self):
        self._network = RTKNetwork()

    @json_output
    def create_sensor(self, **kwargs):
        return self._network.add("sensor", **kwargs)

    @json_output
    def launch_sensor(self, **kwargs):
        return self._network.start(kwargs.get("id", None))

    @json_output
    def delete_sensor(self, **kwargs):
        return self._network.remove(kwargs.get("id", None))

    @json_output
    def stop_sensor(self, **kwargs):
        return self._network.stop(kwargs.get("id", None))

    @json_output
    def launch_filter(self, **kwargs):
        return self._network.start(kwargs.get("id", None))

    @json_output
    def create_filter(self, **kwargs):
        return self._network.add("filter", **kwargs)

    @json_output
    def stop_filter(self, **kwargs):
        return self._network.stop(kwargs.get("id", None))

    @json_output
    def delete_filter(self, **kwargs):
        return self._network.remove(kwargs.get("id", None))

    @json_output
    def sensor_data(self, **kwargs):
        return '{"galvanise": "create_sensor"}'

    @json_output
    def filter_data(self, **kwargs):
        return '{"galvanise": "create_sensor"}'
