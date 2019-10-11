import smtplib
from email.mime.text import MIMEText
from demo.config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS, DOMAIN


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



