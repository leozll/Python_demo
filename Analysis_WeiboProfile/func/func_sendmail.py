#  -*-  coding:  UTF-8  -*-
import logging
import smtplib
import datetime
from email.mime.text import MIMEText



global send_user
global email_host
global password

#password = "jsuxzayuqmzjbgga"
#email_host = "smtp.qq.com"
#send_user = "93073468@qq.com"

password = "zllongtw163"
email_host = "smtp.163.com"
send_user = "zllongtw@163.com"

def send_mail(user_list, sub, content):
    user = "lambda" + "<" + send_user + ">"
    message = MIMEText(content, _subtype='plain', _charset='utf-8')
    message['Subject'] = sub
    message['From'] = user
    message['To'] = ";".join(user_list)
    server = smtplib.SMTP_SSL()
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Start to login mail!')
    server.connect(email_host, 465)
    server.login(send_user, password)
    server.sendmail(user, user_list, message.as_string())
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' Send mail succeed!')
    server.close()


