from rtk.utils.server import RTKWebSocketHandler
from tornado.options import define, options
from tornado import web
import tornado.ioloop


define("port", default=8888, help="run on the given port", type=int)
define("address", default="localhost", help="address of given port", type=str)


class Application(web.Application):
    def __init__(self):
        handlers = [
            (r"/ws", RTKWebSocketHandler),
        ]
        super(Application, self).__init__(handlers)


if __name__ == "__main__":
    options.parse_command_line()
    app = Application()
    print "\n----------------------------------"
    print "RTKWebSocketHandler"
    print "----------------------------------"
    print "Demonstration Software Only"
    print "Launched @ {address}:{port}/ws".format(**{"address": options.address, "port": options.port})
    print "----------------------------------"
    app.listen(options.port, address=options.address)
    tornado.ioloop.IOLoop.current().start()

