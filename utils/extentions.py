from flask_sqlalchemy import SQLAlchemy

from flask_session import Session
from flask_admin import Admin
from flask_wtf import CSRFProtect

db = SQLAlchemy()

session = Session()

admin = Admin(name='fresh', template_mode='bootstrap3')

csrf = CSRFProtect()
