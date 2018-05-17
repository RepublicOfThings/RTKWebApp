import tornado.web
from rtk.core import HubHandler
from tornado.options import define, options
import tornado.options
import tornado.ioloop


define("port", default=8888, help="run on the given port", type=int)
define("address", default="localhost", help="address of given port", type=str)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/ws", HubHandler),
        ]
        super(Application, self).__init__(handlers)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port, address=options.address)
    tornado.ioloop.IOLoop.current().start()
