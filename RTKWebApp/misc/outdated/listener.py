from rtk.core import RTKMQTTClient


c = RTKMQTTClient(host="iot.eclipse.org")
c.subscribe("/rtk/mqtt/f:e2ddaccf-710c-48ca-a602-95a5e590ac6a")
c.run_forever()
