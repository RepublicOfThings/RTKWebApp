from rtk.web import RTKWebSocketHandler
from tornado.options import define, options
import tornado.ioloop as ioloop
import tornado.web


define("port", default=8888, help="run on the given port", type=int)
define("address", default="localhost", help="address of given port", type=str)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/ws", RTKWebSocketHandler),
        ]
        super(Application, self).__init__(handlers)


if __name__ == "__main__":
    options.parse_command_line()
    app = Application()
    app.listen(options.port, address=options.address)
    ioloop.IOLoop.current().start()
