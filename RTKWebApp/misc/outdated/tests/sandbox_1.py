import json
from requests import Session

# creating and launching an RTKFilter instance using the web API.
filter_config = json.load(open("filter.json"))
JSON = json.dumps

rtk = Session()
rtk.post("https://localhost:8883/rtk/api/auth/", params=JSON({"username": "admin", "password":"********"}))
rtk.post("https://localhost:8883/rtk/api/create/filter/", data=JSON(filter_config))
rtk.post("https://localhost:8883/rtk/api/launch/filter/", data=JSON({"id": filter_config["id"]}))
rtk.get("https://localhost:8883/rtk/api/status/filter/", data=JSON({"id": filter_config["id"]}))

