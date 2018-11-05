#  -*-  coding:  UTF-8  -*-
import logging
import smtplib
import datetime
from email.mime.text import MIMEText


class SendEmail:
    global send_user
    global email_host
    global password
    # password = "zllong3325"
    password = "jsuxzayuqmzjbgga"
    email_host = "smtp.qq.com"
    send_user = "93073468@qq.com"

    def send_mail(self, user_list, sub, content):
        user = "猜猜我是谁" + "<" + send_user + ">"
        message = MIMEText(content, _subtype='plain', _charset='utf-8')
        message['Subject'] = sub
        message['From'] = user
        message['To'] = ";".join(user_list)
        server = smtplib.SMTP_SSL()
        server.connect(email_host, 465)
        server.login(send_user, password)
        server.sendmail(user, user_list, message.as_string())
        server.close()


def handler(event, context):
    logger = logging.getLogger()
    logger.info('hello world')

    send = SendEmail()
    user_list = ['leo.zhai@bizfocus.cn']
    sub = "现在时间： " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = "该吃午饭了！！"
    send.send_mail(user_list, sub, content)

