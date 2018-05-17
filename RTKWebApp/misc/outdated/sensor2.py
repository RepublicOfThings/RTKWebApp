from .core import RTKDevice
from .utils import IOMixin
import json
import uuid


class RTKSensor2(RTKDevice, IOMixin):
    def __init__(self, id_, client, generator, model=None):
        RTKDevice.__init__(self, id_, client)
        IOMixin.__init__(self)
        self._generator = generator
        self._model = model

    def start(self):
        try:
            for element in self._generator.start():
                data = self._parse_output(element)
                self._client.send(payload=data)

        except KeyboardInterrupt:
            self._log("Keyboard Interrupt, shutting down.")  # fix

    # needs work
    def _parse_output(self, element):
        # element = json.loads(element)
        if self._model is None:
            data = {"id": self.id, "content": element}
        else:
            data = self._model(element).to_dict()
            data["id"] = self.id

        return json.dumps(data)

    # I/O =====================================================================

    def save(self, path, **kwargs):
        return open(path, "w").write(self.to_json(**kwargs))

    def to_dict(self, *args, **kwargs):
        return {
                "id": self.id,
                "client_type": self.plugin_variant("client", self._client),
                "gen_type": self.plugin_variant("generator", self._client),
                "data_model": self.plugin_variant("model", self._client),
                "generator": self._generator.to_dict(),
                "client": self._client.to_dict()
            }

    @classmethod
    def load(cls, path, **kwargs):
        return cls.from_json(open(path, "r").read(), **kwargs)

    @classmethod
    def from_dict(cls, config):
        id_ = config.get("id", "s:" + str(uuid.uuid4()))
        client_variant = config.get("client_type", "default")
        client_config = config.get("client", {})
        generator_variant = config.get("gen_type", "default")
        generator_config = config.get("generator", {})
        model_variant = config.get("data_model", "default")

        client = cls.plugin_object("client", client_variant).from_dict(client_config)
        generator = cls.plugin_object("generator", generator_variant)(**generator_config)
        model = cls.plugin_object("data", model_variant)

        return cls(id_, client, generator, model)
