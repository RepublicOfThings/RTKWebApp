import logging
import uuid
import abc
from .store import InstanceStore


ACTIVE_PROCESS = 1
INACTIVE_PROCESS = 0
UNINIT_PROCESS = -1


class BaseInstanceManager(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, headers=None, level=logging.DEBUG, max_load=50):
        self._instances = InstanceStore()
        self._headers = headers or {}
        self._logger = logging.getLogger("{0}({1})".format(type(self).__name__, str(uuid.uuid4())))
        self._max_load = max_load
        logging.basicConfig(level=level)

    def instance(self, id_):
        return self._instances.object(id_)

    def status(self, id_):
        return self.instance(id_).status

    @property
    def instances(self):
        return self._instances.objects()

    @property
    def active(self):
        return [x for x in self._instances.processes() if x.is_alive()]

    @property
    def ids(self):
        return self._instances.keys()

    def _process(self, id_):
        return self._instances.process(id_)

    def _instance(self, id_):
        return self._instances.object(id_)

    def _process_status(self, id_):
        if self._process(id_) is None:
            return UNINIT_PROCESS
        elif self._process(id_).is_alive():
            return ACTIVE_PROCESS
        else:
            return INACTIVE_PROCESS

    def _exists(self, id_):
        if id_ in self.ids:
            return True
        else:
            return False

    def _log(self, message, level=logging.DEBUG):
        self._logger.log(level, message)

    def __repr__(self):
        return "{0}(Instances:{1})".format(type(self).__name__, len(self.instances))

    @abc.abstractmethod
    def to_dict(self):
        pass

    @abc.abstractmethod
    def to_json(self):
        pass

    @abc.abstractmethod
    def from_json(self):
        pass

    @abc.abstractmethod
    def from_dict(self):
        pass
