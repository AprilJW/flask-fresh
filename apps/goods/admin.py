from flask_admin.contrib.sqla import ModelView
from utils.extentions import admin, db
from .models import *

admin.add_view(ModelView(GoodsModel, db.session))
admin.add_view(ModelView(GoodsSKU, db.session))
admin.add_view(ModelView(GoodsType, db.session))
