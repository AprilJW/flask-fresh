import time

from flask.views import MethodView
from flask import session, render_template, url_for, redirect, Response
from utils.extentions import db
from .models import User
from itsdangerous import JSONWebSignatureSerializer as Serializer, BadSignature
import re
from demo.config import SECRET_KEY
from utils.tasks import send_register_mail
from utils.auth import login, logout, request


class RegisterView(MethodView):
    def get(self):
        return render_template('register.html')

    def post(self):
        username = request.form.get('username')
        password = request.form.get('pwd')
        email = request.form.get('email')

        if not all([username, password, email]):
            return render_template('register.html', errmsg='数据不完整!')

        allow = request.form.get('allow')
        if allow != 'on':
            return render_template('register.html', **{'errmsg': '请同意协议!'})

        reg = "[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?"
        if not re.match(reg, email):
            return render_template('register.html', **{'errmsg': '邮箱不合法!'})

        if db.session.query(User).filter(User.username == username).first():
            return render_template('register.html', **{'errmsg': '用户名已被注册!'})

        if db.session.query(User).filter(User.email == email).first():
            return render_template('register.html', **{'errmsg': '邮箱已被注册!'})

        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()

        serializer = Serializer(SECRET_KEY)
        data = {'id': user.id, 'time': time.time()}
        token = serializer.dumps(data).decode()

        send_register_mail(email, username, token)

        return '666'


class LoginView(MethodView):
    def get(self):
        username = request.cookies.get('username', '')

        checked = 'checked' if username else ''

        return render_template('login.html', **{'username': username, 'checked': checked})

    def post(self):
        username = request.form.get('username')
        password = request.form.get('pwd')
        if not all([username, password]):
            return render_template('login.html', **{'errmsg': '数据不完整!'})

        user = User.authenticated(username=username, password=password)

        if not user:
            return render_template('login.html', **{'errmsg': '用户名或密码错误!'})

        if not user.active:
            return render_template('login.html', **{'errmsg': '用户未激活!'})

        login(user)

        next_url = request.args.get('next', url_for('goods.index'))

        response = redirect(next_url)

        remember = request.form.get('remember')

        if remember == 'on':
            response.set_cookie('username', username, max_age=7 * 24 * 3600)
        else:
            response.delete_cookie('username')

        return response


class ActiveView(MethodView):
    def get(self, token):
        serializer = Serializer(SECRET_KEY)
        try:
            data = serializer.loads(token.encode())
            user_id = data.get('id')
            user = db.session.query(User).filter(User.id == user_id).first()
            user.active = True
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.login'))
        except BadSignature:
            return Response('错误的请求链接!', status=403)


class LogoutView(MethodView):
    def get(self):
        logout()
        return redirect(url_for('user.login'))
