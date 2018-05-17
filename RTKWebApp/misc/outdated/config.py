

class RTKConfig(object):

    __defaults = {
            "filter": {
                    "filter_type": "kalman",
                    "filter": {},
                    "client": {
                            "host": "localhost",
                            "port": 1883,
                            "clean_session": True,
                            "userdata": None,
                            "transport": None
                        }
                }
        }

    def __init__(self, variant, id_=None):
        self.id = id_
        self._variant = variant

    def package(self):
        pass