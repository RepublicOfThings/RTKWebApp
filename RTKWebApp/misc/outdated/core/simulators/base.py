

class Simulator(object):
    def __init__(self, *args, **kwargs):
        """
        Abstract class for RTK Simulators
        """
        self.active = False

    def __call__(self, *args, **kwargs):
        self.configure(*args, **kwargs)
        return self.start()

    def start(self):
        self.active = True
        while self.active:
            yield self.step()
            self.delay()

    def configure(self, *args, **kwargs):
        pass

    def delay(self):
        pass

    def step(self):
        raise NotImplementedError

