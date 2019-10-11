from utils.extentions import db

from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20))
    _password = db.Column(db.String(255))
    email = db.Column(db.String(50))
    active = db.Column(db.Boolean(), default=False)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    @classmethod
    def authenticated(cls, username, password):
        user = db.session.query(cls).filter(cls.username == username).first()
        if not user:
            return False
        return user if check_password_hash(user.password, password) else False

    @property
    def is_authenticated(self):
        return True
