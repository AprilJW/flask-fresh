from . import views
from flask import Blueprint

blue_print = Blueprint('user', __name__, url_prefix='/user')

blue_print.add_url_rule('/login', view_func=views.LoginView.as_view('login'))
