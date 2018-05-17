from .client import BaseClient
from ...instances import errors
import paho.mqtt.client as mqtt


class MQTTClient(BaseClient):
    def __init__(self, host="localhost", port=1883, client_id="", topics=[], **kwargs):
        super(MQTTClient, self).__init__(client_id)
        self.id = client_id
        self.__client = mqtt.Client(client_id=client_id, **kwargs)
        self.__subscriptions = []
        self.__topics = topics
        self.__client.on_connect = self.on_connect
        self.__client.on_message = self.on_message
        self.__client.on_unsubscribe = self.on_unsubscribe
        self.__kwargs = kwargs
        self.host = host
        self.port = port
        self.connect(host, port=int(port))

    def update_config(self, **config):
        self.id = config.get("client_id", self.id)
        self._update_subs(config.get("subscriptions", self.__subscriptions))
        self.__topics = config.get("topics", self.__topics)

    def _update_subs(self, topics):
        # print self.__subscriptions
        keep_topics = [y for y in [x["topic"] for x in self.__subscriptions] if y in [z["topic"] for z in topics]]
        rem_topics = [y for y in [x["topic"] for x in self.__subscriptions] if y not in [z["topic"] for z in topics]]
        new_topics = [x for x in [y["topic"] for y in topics] if x not in keep_topics]

        try:
            for topic in new_topics:
                self.subscribe(str(topic), qos=2)

            for topic in rem_topics:
                self.unsubscribe(topic)

        except ValueError as e:
            raise errors.ConfigurationError("Failed to update subscription - fell back to original settings. (091)")

    def run_forever(self, subs=[], qos=0, **kwargs):
        for sub in subs:
            self.subscribe(sub, qos)
        return self.mainloop(**kwargs)

    def connect(self, host="localhost", port=1883, **kwargs):
        self._log("Connecting to host '{0}:{1}'".format(host, port))
        self.__client.connect(host, port=port, **kwargs)

    def send(self, topic=None, payload=None, **kwargs):
        if topic is None and len(self.__topics) == 0:
            raise ValueError("Must specify a target topic if topics are not defined.")
        elif topic is not None:
            self.publish(topic, payload, **kwargs)
        else:
            for topic in self.__topics:
                self.publish(topic, payload, **kwargs)

    def publish(self, topic, payload=None, **kwargs):
        self.__client.publish(topic, payload=payload, **kwargs)
        self._log("Sending to topic '{0}': {1} bytes".format(topic, str(payload).__sizeof__()))

    def subscribe(self, sub, qos=0):
        self.__client.subscribe(sub, qos)
        self.__subscriptions.append({"topic": sub, "qos": qos})
        self._log("Subscribed to topic: {0}".format(sub))

    def unsubscribe(self, topic):
        self._log("Unsubscribing from topic: {0}...".format(topic))
        self.__client.unsubscribe(topic)
        self.__subscriptions.remove({"topic": topic, "qos": 2})
        self._log("Unsubscribed from topic: {0}".format(topic))

    def on_message(self, client, user_data, message):
        self._log("Received message: {0}".format(message.payload))

    def on_connect(self, client, user_data, flags, rc):
        self._log("Connected to host, status: {0}".format(rc))

    def on_unsubscribe(self, *args, **kwargs):
        print args, kwargs

    def set_method(self, method, func):
        setattr(self.__client, method, func)

    def mainloop(self, **kwargs):
        try:
            rc = 0
            while rc == 0:
                rc = self.__client.loop()
            return rc
        except KeyboardInterrupt:
            self._log("Keyboard Interrupt, shutting down.")

    def to_dict(self):
        output = {
                "host": self.host,
                "port": self.port,
                "client_id": self.cid,
                "subscriptions": self.__subscriptions,
                "topics": self.__topics,
            }
        output.update(self.__kwargs)
        return output

    @classmethod
    def from_dict(cls, config):
        subs = config.get("subscriptions", [])

        del config["subscriptions"]

        mqtt_client = cls(**config)

        for sub in subs:
            mqtt_client.subscribe(sub["topic"], sub.get("qos", 0))

        return mqtt_client

    @property
    def inputs(self):
        return [sub["topic"] for sub in self.__subscriptions]

    @property
    def outputs(self):
        return self.__topics