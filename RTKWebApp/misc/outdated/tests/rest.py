import tornado.web
from tornado.options import define, options
import tornado.options
import tornado.ioloop
from rtk.core.rest import app


define("port", default=8883, help="run on the given port", type=int)
define("address", default="localhost", help="address of given port", type=str)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = app.RTKRESTApplication()
    app.listen(options.port, address=options.address)
    tornado.ioloop.IOLoop.current().start()
