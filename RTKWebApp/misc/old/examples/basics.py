from rtk.api import API
import json
import time

api = API(target="http://localhost:8080/rtk")
data = json.dumps(json.load(open("../../data/sensor.json", "r")))
api.post.create.sensor(data=data)
sensor_id = api.instances(unpack=True)["payload"][0]["id"]
api.post.start(params="i="+str(sensor_id))

# do stuff...
time.sleep(10)

print api.post.stop(params="i="+str(sensor_id), unpack=True)
