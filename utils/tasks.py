import config
from config import DOMAIN
from .tools import send_mail
from celery import Celery

broker = 'redis://:{PASSWORD}@{HOST}/8'.format(
    PASSWORD=config.REDIS_PASSWORD,
    HOST=config.REDIS_HOST
)
app = Celery('utils.tasks', broker=broker)


@app.task
def send_register_mail(to_email, username, token):
    subject = '生鲜商城欢迎信息'
    html_message = '<h1>{}, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/><a href="{}/user/active/{}" style="color: green">点击激活</a>'.format(
        username, DOMAIN, token)
    send_mail(subject, to_email, html_message)
