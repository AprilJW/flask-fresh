from flask.views import MethodView
from flask import session, render_template


class LoginView(MethodView):
    def get(self):
        return 'render_template()'

    def post(self):
        pass
