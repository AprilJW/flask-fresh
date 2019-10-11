from apps.user.models import User
from utils.extentions import db
from functools import wraps
from flask import session, redirect
from flask import request as req
from demo.config import LOGIN_URL


def login(user):
    session['login'] = user.id


def logout():
    session.clear()


class AnonymousUser(object):

    @property
    def is_authenticated(self):
        return False


def get_current_user():
    user_id = session.get('login')
    if not user_id:
        user = AnonymousUser()
    else:
        user = db.session.query(User).filter(User.id == user_id).first()

    return user


class Request(object):
    def __init__(self,):
        self._request = req

    def __getattr__(self, item):
        try:
            return getattr(self._request, item)
        except AttributeError:
            return self.__getattribute__(item)

    @property
    def user(self):
        user = get_current_user()
        return user


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if user.is_authenticated:
            return func(*args, **kwargs)
        else:
            next_url = request.path
            redirect_url = '%s?next=%s' % (LOGIN_URL, next_url) if next_url != LOGIN_URL else LOGIN_URL
            return redirect(redirect_url)

    return wrapper


request = Request()
