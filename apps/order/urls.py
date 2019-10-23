from flask import Blueprint
from . import views

blue_print = Blueprint('order', __name__, url_prefix='/order')

blue_print.add_url_rule('place', view_func=views.OrderPlaceView.as_view('place'))
blue_print.add_url_rule('commit', view_func=views.OrderCommitView.as_view('commit'))
blue_print.add_url_rule('pay', view_func=views.OrderPayView.as_view('pay'))
blue_print.add_url_rule('check', view_func=views.OrderCheckView.as_view('check'))

