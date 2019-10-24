import smtplib
from email.mime.text import MIMEText
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS, DOMAIN
from config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT
import redis


def send_mail(subject, receiver, html_message):
    smtp = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    smtp.login(EMAIL_USER, EMAIL_PASS)
    subject = subject
    message = MIMEText(html_message, 'html', 'utf-8')
    message['From'] = EMAIL_USER
    message['To'] = receiver
    message['Subject'] = subject
    smtp.sendmail(EMAIL_USER, [receiver], message.as_string())
    smtp.quit()


def get_redis_connection(db=1, *args, **kwargs):
    coon = redis.StrictRedis(
        host=REDIS_HOST,
        password=REDIS_PASSWORD,
        db=db,
        port=REDIS_PORT,
        *args, **kwargs)
    return coon
