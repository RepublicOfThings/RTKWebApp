from .base import BaseHandler
import tornado.escape
import tornado.web


class AuthLoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        pass

    def authenticate(self, password, username):
        if username == "admin" and password == "scrimshaw":
            return True
        return False

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        auth = self.authenticate(password, username)
        if auth:
            self.set_current_user(username)
            self.redirect(self.get_argument("next", "/"))
        else:
            raise tornado.web.HTTPError(403)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))
