from .base import BaseHandler
import tornado.web
import tornado.escape

# Why?

class RTKMainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write("index.html")
