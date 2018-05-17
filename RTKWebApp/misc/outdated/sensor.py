from rtk.sensors import RTKSensor

s = RTKSensor.from_json(open("./data/sensor.json").read())
s.start()