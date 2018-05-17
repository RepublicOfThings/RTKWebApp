import abc
from rtk.core.generators import DataGenerator, NormalGenerator
from rtk.core.clients import MQTTClient, WebSocketClient
from rtk.core.models import ApartmentReading
from rtk.instances.pipes import KPipe, JPipe
import logging


ACTIVE = 2
PAUSED = 1
INITIALISED = 0
UNINITIALISED = -1
ERROR = -2
DELETED = -3


class Instance(object):
    __metaclass__ = abc.ABCMeta

    _plugins = {
            "client": {
                    "mqtt": MQTTClient,
                    "websocket": WebSocketClient,
                    "default": MQTTClient,
                },
            "pipe": {
                    "kalman": KPipe,
                    "json": JPipe,
                    "default": JPipe
                },
            "generator": {
                    "normal": NormalGenerator,
                    "data": DataGenerator,
                    "default": DataGenerator
                },
            "data": {
                    "apartment": ApartmentReading,
                    "default": None  # huh?
                }
        }

    def __init__(self, id_, name, client):
        """
        
        
        Parameters
        ----------
        id_
        name
        client
        
        Todo
        ----
        * Not a fan of the way status flags are currently handled -- very inelegant.
        * The 'plugins' approach is a bit naff. Give it a rethink at some point.
        
        """

        self.id = id_
        self.name = name
        self._client = client
        self._logger = logging.getLogger("{0}:{1}".format(type(self).__name__, self.id))
        self._state = INITIALISED
        logging.basicConfig(level=logging.DEBUG)

    @abc.abstractmethod
    def update_config(self):
        pass

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def load(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def save(self, *args, **kwargs):
        pass

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def status(self):
        return {"id": self.id, "status": self.state}

    @property
    def plugins(self):
        for key, value in self._plugins.items():
            yield key, value

    @classmethod
    def plugin_variant(cls, plugin_type, instantiation):
        for key, value in cls._plugins.get(plugin_type, {}).items():
            # careful.
            if type(instantiation) == value or instantiation == value:
                return key

    @classmethod
    def plugin_object(cls, plugin_type, variant):
        return cls._plugins.get(plugin_type, {}).get(variant, None)

    @classmethod
    def is_plugin_instance(cls, plugin_type, variant, instance):
        if cls.plugin_variant(plugin_type, instance) == variant:
            return True
        else:
            return False

    @property
    def inputs(self):
        return self._client.inputs

    @property
    def outputs(self):
        return self._client.outputs

    def new_plugin(self, plugin_type, **kwargs):
        """
        sensor.new_plugin("client", http=HTTPClient)
        
        Parameters
        ----------
        plugin_type

        Returns
        -------

        """

        if plugin_type not in self.plugins:
            self._plugins[plugin_type] = {}

        self._plugins[plugin_type].update(kwargs)

    def _log(self, message, level=logging.DEBUG, **kwargs):
        self._logger.log(level, message, **kwargs)
