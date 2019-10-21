from flask import Blueprint
from . import views

blue_print = Blueprint('order', __name__, url_prefix='/order')

blue_print.add_url_rule('place', view_func=views.OrderPlaceView.as_view('place'))
