from base import BaseGenerator


class CountGenerator(BaseGenerator):
    def __init__(self, start=0, stride=1, **kwargs):
        super(CountGenerator, self).__init__(**kwargs)
        self._count = start
        self._stride = stride

    def step(self):
        self._count += self._stride
        return self._count

