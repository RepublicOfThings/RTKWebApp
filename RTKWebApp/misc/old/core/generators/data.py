from base import BaseGenerator
import csv
import io


class DataGenerator(BaseGenerator):
    def __init__(self, path=None, cols=None, loop=True, data=None, **kwargs):
        super(DataGenerator, self).__init__(**kwargs)
        self._data = data
        if data is not None:
            if path is None:
                raise IOError("(DataGenerator) A valid path to 'csv' file must be specified, not None")
            else:
                self._csv = csv.reader(io.StringIO(data), delimiter=',')
        elif path is not None:
            self._csv = csv.reader(open(path), delimiter=',')
        else:
            raise IOError("(DataGenerator) No valid data file obtained.")
        if cols is None:
            self.data = [x for x in self._csv]
        else:
            self.data = [{y: x[y] for y in x.keys() if y in cols} for x in self._csv]

        self._path = path
        self._idx = 0
        self._loop = True

    def update_config(self, **kwargs):
        self._wait_time = kwargs.get("wait", self._wait_time)

    def step(self):
        if self._idx >= len(self.data)-1:
            self._idx = 0  # this should be optional!
        else:
            self._idx += 1
        return self.data[self._idx]

    def to_dict(self):
        return {
                "path": self._path,
                "wait": self._wait_time,
                "data": self._data
            }

    @classmethod
    def from_dict(self):
        pass
