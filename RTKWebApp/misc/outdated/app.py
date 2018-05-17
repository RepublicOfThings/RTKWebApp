import tornado.web
from .auth import AuthLoginHandler
from .api import APIHandler


RTK_HANDLERS = [
    (r'/rtk/api/', APIHandler),
    (r'/rtk/api/(\w+)/$', APIHandler),
    (r'/rtk/api/(\w+)/(\w+)/$', APIHandler),
    (r'/rtk/api/auth/$', AuthLoginHandler),
    ]

AUTH_PATH = r'/rtk/api/auth/$'
SECRET_COOKIE = "lemonade"


class RTKRESTApplication(tornado.web.Application):
    def __init__(self):
        super(RTKRESTApplication, self).__init__(RTK_HANDLERS,
                                                 cookie_secret=SECRET_COOKIE,
                                                 login_url=AUTH_PATH)
