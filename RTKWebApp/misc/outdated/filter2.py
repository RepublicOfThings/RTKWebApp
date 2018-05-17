from .core import RTKDevice
from .utils import IOMixin
import json
import uuid


class RTKFilter2(RTKDevice, IOMixin):
    def __init__(self, id_, client, pipe, model=None):
        RTKDevice.__init__(self, id_, client)
        IOMixin.__init__(self)
        self._pipe = pipe
        self._model = model

    def start(self):
        self._client.set_method("on_message", self.on_message)
        self._client.run_forever()

    def on_message(self, client, user_data, message):
        payload = json.loads(message.payload)
        payload["meta"] = self._pipe.pipe(json.dumps(payload))
        self._client.send(payload=json.dumps(payload, indent=4))

    # I/O =====================================================================

    def save(self, path, **kwargs):
        return open(path, "w").write(self.to_json(**kwargs))

    def to_dict(self, *args, **kwargs):
        return {
            "id": self.id,
            "filter_type": self.plugin_variant("pipe", self._pipe),
            "client_type": "mqtt",
            "filter": self._pipe.to_dict(),
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

        pipe_variant = config.get("filter_type", "default")
        pipe_config = config.get("filter")

        client = cls.plugin_object("client", client_variant)
        pipe = cls.plugin_object("pipe", pipe_variant)

        return cls(id_, client.from_dict(client_config), pipe(pipe_config))
