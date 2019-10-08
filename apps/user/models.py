from utils.extentions import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20))
    _password = db.Column(db.String(255))
    email = db.Column(db.String(50))
    active = db.Column(db.Boolean(), default=False)

    def __init__(self, username, password, eamil):
        self.username = username
        self.password = password
        self.eamil = eamil

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def authenticated(self, password):
        return check_password_hash(self.password, password)
