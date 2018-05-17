import requests
import json
import time

path = "http://localhost:8883"
auth = {"username": "admin", "password": "scrimshaw"}
sensor = json.load(open("./sensor.json"))
raw = json.dumps(sensor)
sid = json.dumps({"id": sensor["id"]})

s = requests.Session()
r1 = s.post(path+"/rtk/api/auth/", params=auth)
print(r1.content)
r2 = s.post(path+"/rtk/api/create/sensor/", data=raw)
print(r2.content)
r3 = s.post(path+"/rtk/api/launch/sensor/", data=sid)
print(r3.content)
r4 = s.post(path+"/rtk/api/stop/sensor/", data=sid)
print(r4.content)
r5 = s.post(path+"/rtk/api/destroy/sensor/", data=sid)
print(r5.content)

"""
{
  "id": "468a1687-0829-4e6b-a5b6-cb98dfa62509",
  "type": "RTKSensor",
  "broker": {"host": "localhost", "port": 1883},
  "publish_to": "sensors/RTK:468a1687-0829-4e6b-a5b6-cb98dfa62509",
  "measurements": {
    "temperature": {"dims": "F"}
  }
}
rtk/api/create/filter
rtk/api/create/sensor
rtk/api/delete/filter
rtk/api/delete/sensor
rtk/api/data/filter
rtk/api/data/sensor
rtk/api/auth

rtk/network
rtk/monitor
rtk/creator/filter
rtk/creator/sensor

r1 = s.post("http://localhost:8883/rtk/api/auth/", params={"username": "admin", "password": "scrimshaw"})
r2 = s.post("http://localhost:8883/rtk/api/create/sensor/", data=json.dumps({"id": 1, "config": {"address": "localhost:8888",
                                                                                                 "path": "ws",
                                                                                                 "header": {"socket": "thing"}}}))
r3 = s.post("http://localhost:8883/rtk/api/launch/sensor/", data=json.dumps({"id": 1}))
print(r2.content)
print(r3.content)
time.sleep(5)
r4 = s.post("http://localhost:8883/rtk/api/destroy/sensor/", data=json.dumps({"id": 1}))
print(r4.content)

"""
