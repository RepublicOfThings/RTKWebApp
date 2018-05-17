import abc
import logging


class BaseClient(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, client_id, level=logging.DEBUG):
        self.cid = client_id
        self.__logger = logging.getLogger("{0}({1})".format(type(self).__name__, client_id))
        logging.basicConfig(level=level)
        self.__logger.setLevel(level)

    @abc.abstractmethod
    def inputs(self):
        pass

    @abc.abstractmethod
    def outputs(self):
        pass

    @abc.abstractmethod
    def run_forever(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def send(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def connect(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def mainloop(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def set_method(self, method, func):
        pass

    @abc.abstractmethod
    def update_config(self, **config):
        pass

    def on_message(self, *args, **kwargs):
        pass

    def on_connect(self, *args, **kwargs):
        pass

    def _log(self, message, **kwargs):
        self.__logger.log(kwargs.get("level", self.__logger.level), message)

    def to_dict(self, *args, **kwargs):
        pass

    def from_dict(self, *args, **kwargs):
        pass
