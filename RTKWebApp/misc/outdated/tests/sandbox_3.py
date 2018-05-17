import requests
import json
import time

s = requests.Session()
r1 = s.post("http://localhost:8888/rtk/api/auth/", params={"username": "admin", "password": "scrimshaw"})
r2 = s.post("http://localhost:8888/rtk/api/create/thread/", data=json.dumps({"id": 4}))
r3 = s.post("http://localhost:8888/rtk/api/create/thread/", data=json.dumps({"id": 5}))
time.sleep(20)
r4 = s.post("http://localhost:8888/rtk/api/destroy/thread/", data=json.dumps({"id": 4}))
time.sleep(10)
r5 = s.post("http://localhost:8888/rtk/api/destroy/thread/", data=json.dumps({"id": 5}))
print(r5.content)