import paho.mqtt.client as mqtt
import logging


class MQTTWrapper(mqtt.Client):
    def __init__(self, client_id="", host="localhost", port=1883, timeout=60, log_level=logging.DEBUG, **kwargs):
        super(MQTTWrapper, self).__init__(client_id=client_id, **kwargs)
        self.connect(host, port=port, keepalive=timeout)
        self._log = self._init_log(level=log_level)

    def on_connect(self, client, obj, flags, rc):
        pass

    def on_message(self, client, obj, msg):
        print msg

    def on_publish(self, client, obj, mid):
        pass

    def on_subscribe(self, client, obj, mid, granted_qos):
        pass

    def on_log(self, client, obj, level, string):
        pass

    def _init_log(self, name=None, level=logging.DEBUG):
        logger = logging.getLogger(name or self._client_id)
        logging.basicConfig(level=level)
        return logger

    def run(self, subs=[], qos=0, **kwargs):
        for sub in subs:
            self.subscribe(sub, qos)
        return self.mainloop()

    def mainloop(self):
        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc
