# -*- coding: utf-8 -*-
import logging
import datetime
import oss2
from itertools import islice

import sys
import os

sys.path.append(os.curdir + '/func/packages/')
from func.func_requestuid import *
from func.func_write2file import *


def handler(event, context):
    endpoint = 'oss-cn-beijing-internal.aliyuncs.com'
    bucket = 'analysis-demo.oss-cn-beijing-internal.aliyuncs.com'
    creds = context.credentials
    uid_list_file = 'tmp/weibo_uid_list'
    uid_list = []

    logger = logging.getLogger()
    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Start WeiboUid')
    print('--------------------------------------------------------------------------------------')

    auth = oss2.StsAuth(creds.accessKeyId, creds.accessKeySecret, creds.securityToken)
    bucket = oss2.Bucket(auth, endpoint, bucket)

    bucket.get_object_to_file('configuration/weibo_url_list', uid_list_file)

    with open(uid_list_file, 'r') as f_uid:
        l_uid = f_uid.readlines()
    for i in range(0, len(l_uid)):
        uid_list.append(get_uid(l_uid[i].rstrip('\n'))['id'] + '\n')

    write_to_file(uid_list, uid_list_file, 'w')

    user_list = ['leo.zhai@bizfocus.cn']
    sub = "现在时间： " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = "该吃午饭了！！"
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Start to send mail!')
    # send_mail(user_list, sub, content)


if __name__ == "__main__":
    handler('1', '2')
