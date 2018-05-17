import logging
from .plugins import PluginInterface


class Logger(object):
    def __init__(self, name, level=logging.DEBUG, **kwargs):
        logging.basicConfig(level=level, **kwargs)
        self.__log = logging.getLogger(name)
        self.__level = level

    def log(self, msg, *args, **kwargs):
        self.__log.log(self.__level, msg, *args, **kwargs)


class BaseInstance(Logger, PluginInterface):
    def __init__(self, identifier, name, client, **kwargs):
        self.id_ = identifier
        self.name = name
        self.client = client
        Logger.__init__(name, **kwargs)
        PluginInterface.__init__()

