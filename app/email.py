# -*- coding: utf-8 -*-

from flask_mail import Mail, Message
from flask import render_template
from threading import Thread
from app import mail
from manage import app

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    """
    发送电子邮件,利用线程异步发送
    :param to:
    :param subject:
    :param template:
    :param kwargs:
    :return:
    """
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
