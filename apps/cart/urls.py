from . import views
from flask import Blueprint

blue_print = Blueprint('cart', __name__, url_prefix='/cart')

blue_print.add_url_rule('add', view_func=views.CartAddView.as_view('add'))
blue_print.add_url_rule('', view_func=views.CartInfoView.as_view('show'))
