from rtk.filters import RTKFilter
from rtk.core import RTKMQTTClient


f = RTKFilter.from_json("./data/filter.json")
f.start()