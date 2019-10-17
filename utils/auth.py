from utils.extentions import db
from functools import wraps
from flask import session, redirect
import flask
from demo.config import LOGIN_URL, AUTH_USER_MODEL
import importlib


def login(user):
    session['login'] = user.id


def logout():
    session.clear()


def initialize_user_model():
    app, user_model_class = AUTH_USER_MODEL.split('.')
    model = importlib.import_module('apps.%s.models' % app)

    user_model = getattr(model, user_model_class)

    return user_model


def get_current_user():
    user_id = session.get('login')
    if not user_id:
        user = AnonymousUser()
    else:
        user_model = initialize_user_model()
        user = db.session.query(user_model).filter(user_model.id == user_id).first()

    return user


class AnonymousUser(object):
    id = None
    pk = None
    username = ''

    @property
    def is_authenticated(self):
        return False

    @property
    def is_anonymous(self):
        return True


class Request(object):
    def __init__(self):
        self._request = flask.request

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
