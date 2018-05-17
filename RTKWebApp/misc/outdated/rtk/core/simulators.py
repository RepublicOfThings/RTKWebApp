import time


class BaseSimulator(object):
    def __init__(self, *args, **kwargs):
        """
        Abstract class for RTK Simulators
        """
        self.active = False

    def __call__(self, *args, **kwargs):
        return self.start(*args, **kwargs)

    def start(self):
        self.active = True
        return self.run()

    def stop(self):
        self.active = False

    def run(self):
        while self.active:
            yield self.step()
            self.delay()

    def delay(self):
        pass

    def step(self):
        raise NotImplementedError


class BaseSensor(BaseSimulator):
    def __init__(self, units="ARB", delay_fn=lambda: 1, delay_args=(), *args, **kwargs):
        self.count = 0
        self.units = units
        self.delay_fn = delay_fn
        self.delay_args = delay_args
        super(BaseSensor, self).__init__(*args, **kwargs)

    def delay(self):
        time.sleep(self.delay_fn(*self.delay_args))

    def step(self):
        self.count += 1
        return self.measure()

    def measure(self):
        return {}
