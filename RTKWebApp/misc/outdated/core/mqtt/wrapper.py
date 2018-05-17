import paho.mqtt.client as mqtt
import uuid


class RTKMQTTDevice(object):
    def __init__(self, host, id=None, port=1883, name="RTKMQTTDevice", subscriptions=[], listen=False, **kwargs):
        self._host = host
        self._subs = subscriptions
        self._port = port
        self._name = name
        if id is None:
            id = uuid.uuid4()
        self._client = mqtt.Client(client_id=self._name+str(id))
        self.__setup(listen, **kwargs)

    def __setup(self, listen, **kwargs):
        self._client.on_connect = self.on_connect
        self._client.on_message = self.on_message
        self._client.on_publish = self.on_publish
        self._client.on_subscribe = self.on_subscribe
        self._client.on_unsubscribe = self.on_unsubscribe
        self._client.connect(self._host, port=self._port)
        for sub in self._subs:
            self._client.subscribe(sub)
        if listen:
            self._client.loop_forever(**kwargs)

    def subscribe(self, *args, **kwargs):
        return self._client.subscribe(*args, **kwargs)

    def publish(self, *args, **kwargs):
        return self._client.publish(*args, **kwargs)

    def on_connect(self, client, user_data, flags, response):
        print(client, user_data, flags, response)

    def on_message(self, client, user_data, message):
        print(message.payload)

    def on_publish(self, client, user_data, message):
        pass

    def on_subscribe(self, client, user_data, mid_var, qos):
        pass

    def on_unsubscribe(self, client, user_data, mid_var):
        pass

    @classmethod
    def from_json(cls, filename):
        pass