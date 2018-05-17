from rtk.core import clients, generators, models
from rtk.instances import pipes


class Plugin(object):
    pass


class PluginManagerMixin(object):
    def __init__(self):
        self._available = {
            "client": {
                    "mqtt": clients.MQTTClient,
                    "websocket": clients.WebSocketClient,
                    "default": clients.MQTTClient,
                },
            "pipe": {
                    "kalman": pipes.KPipe,
                    "json": pipes.JPipe,
                    "default": pipes.JPipe
                },
            "generator": {
                    "normal": generators.NormalGenerator,
                    "data": generators.DataGenerator,
                    "default": generators.DataGenerator
                },
            "data": {
                    "apartment": models.ApartmentReading,
                    "default": None  # huh?
                }
        }

    def plugin(self, variant, plugin_object):
        pass
