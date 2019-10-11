from apps.user.models import User
from utils.extentions import db, app
from functools import wraps
from flask import session, redirect, request
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
