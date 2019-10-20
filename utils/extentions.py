from flask_sqlalchemy import SQLAlchemy
from demo.app import create_app
from flask_session import Session
from flask_admin import Admin
from flask_wtf import CSRFProtect

app = create_app()

db = SQLAlchemy(app)

Session(app)

admin = Admin(app, name='fresh', template_mode='bootstrap3')

CSRFProtect(app)
