from . import views
from flask import Blueprint

blue_print = Blueprint('cart', __name__, url_prefix='/cart')

blue_print.add_url_rule('add', view_func=views.CartAddView.as_view('add'))
blue_print.add_url_rule('', view_func=views.CartInfoView.as_view('show'))
blue_print.add_url_rule('update', view_func=views.CartUpdateView.as_view('update'))
blue_print.add_url_rule('delete', view_func=views.CartDeleteView.as_view('delete'))
