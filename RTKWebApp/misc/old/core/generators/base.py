import abc
import time


class BaseGenerator(object):
    __metaclass__ = abc.ABCMeta
    INACTIVE = -1
    READY = 0
    ACTIVE = 1

    def __init__(self, wait=1.0, maxiter=1e6):
        self._status = self.READY
        self._wait_time = wait
        self._iter = 0
        self._maxiter = maxiter or int(1e28)

    def __call__(self, *args, **kwargs):
        self.configure(*args, **kwargs)
        self.start()

    def start(self):
        self._status = self.ACTIVE
        while self._status:
            if self._iter >= self._maxiter:
                break
            else:
                self._iter += 1
            yield self.step()
            self._wait()

    def _wait(self):
        time.sleep(self._wait_time)

    def configure(self, *args, **kwargs):
        self._wait_time = kwargs.get("wait", self._wait_time)

    @abc.abstractmethod
    def update_config(self):
        pass

    @abc.abstractmethod
    def step(self):
        pass

    @abc.abstractmethod
    def to_dict(self):
        pass

    @abc.abstractmethod
    def from_dict(self):
        pass