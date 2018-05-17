from base import BaseGenerator
import apogee as ap


class NormalGenerator(BaseGenerator):
    def __init__(self, loc=0.0, scale=1.0, **kwargs):
        super(NormalGenerator, self).__init__(**kwargs)
        self._normal = ap.MultivariateNormal(loc, scale)

    def update_config(self, **kwargs):
        self._wait_time = kwargs.get("wait", self._wait_time)
        loc, scale = kwargs.get("loc", self._normal.mean), kwargs.get("scale", self._normal.cov)
        self._normal = ap.MultivariateNormal(loc, scale)

    def step(self):
        return float(self._normal.sample(1).squeeze())

    def to_dict(self):
        return {
                "loc": self._normal.mean,
                "scale": self._normal.cov,
                "wait": self._wait_time
            }

    def from_dict(self):
        pass