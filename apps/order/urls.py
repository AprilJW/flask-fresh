from flask import Blueprint

blue_print = Blueprint('order', __name__, url_prefix='/')

# blue_print.add_url_rule('', view_func=views.IndexView.as_view('index'))
# blue_print.add_url_rule('goods/<int:pk>', view_func=views.DetailView.as_view('detail'))