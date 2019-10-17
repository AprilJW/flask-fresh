from sqlalchemy.orm import relationship

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

    @property
    def is_anonymous(self):
        return False


class Address(db.Model):
    """地址模型类"""
    __tablename__ = 'df_address'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    # user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='所属用户')
    user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    # receiver = models.CharField(max_length=20, verbose_name='收件人')
    receiver = db.Column(db.String(20), nullable=False)
    # addr = models.CharField(max_length=256, verbose_name='收件地址')
    addr = db.Column(db.String(256), nullable=False)
    # zip_code = models.CharField(max_length=6, null=True, verbose_name='邮政编码')
    zip_code = db.Column(db.String(6))
    # phone = models.CharField(max_length=11, verbose_name='联系电话')
    phone = db.Column(db.String(11), nullable=False)
    # is_default = models.BooleanField(default=False, verbose_name='是否默认')
    is_default = db.Column(db.Boolean, default=False)

    _user = relationship('User', backref='_address')