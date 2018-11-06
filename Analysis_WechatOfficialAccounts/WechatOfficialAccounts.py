# -*- coding: utf-8 -*-
import logging
import datetime
#import func.func_sendmail
from func.func_sendmail import *


def handler(event, context):
    logger = logging.getLogger()
    logger.info('hello world')
    print (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print ('--------------------------------------------------------------------------------------')

    user_list = ['leo.zhai@bizfocus.cn']
    sub = "现在时间： " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = "该吃午饭了！！"
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' Start to send mail!')
    send_mail(user_list, sub, content)

if __name__ == "__main__":
    handler('1', '2')
