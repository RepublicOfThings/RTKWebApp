from .. import websockets, simulations


class RTKTemperatureSensor(websockets.RTKWebSocketSensor):
    def __init__(self, config={}, *args, **kwargs):
        sim = simulations.SimulatedTemperatureSensor(**config)
        super(RTKTemperatureSensor, self).__init__(sim=sim, *args, **kwargs)
