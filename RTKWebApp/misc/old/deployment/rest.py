import pyrestful.rest
import tornado.ioloop
from rtk.api.web.rest import RESTHandler
import logging


class RESTLauncher(object):
    def __init__(self, level=logging.DEBUG, name="RTK-REST", address="127.0.0.1", port=8080):
        self._name = name
        self._address = address
        self._port = port
        self._log = logging.getLogger(name)
        logging.basicConfig(level=level)
        self._log.info("Setting up {name} service.".format(**{"name": name}))
        self._app = pyrestful.rest.RestService([RESTHandler])
        self._app.listen(port, address=address)
        self._log.info("Setup complete, launching {name} service @ http://{address}:{port}.".format(**{"name": self._name, "address": self._address, "port": self._port}))

    def launch(self):
        try:
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            self._log.info("Shutting down REST service.")
