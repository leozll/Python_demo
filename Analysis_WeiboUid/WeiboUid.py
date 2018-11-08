# -*- coding: utf-8 -*-
import logging
import datetime
import time
import oss2
from itertools import islice

import sys
import os

sys.path.append(os.curdir + '/func/packages/')
from func.func_requestuid import *
from func.func_write2file import *


def handler(event, context):
    logger = logging.getLogger()
    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Start WeiboUid')
    print('--------------------------------------------------------------------------------------')
    print(get_uid('https://weibo.com/chcedo')['id'] + '\n')

    tmpdir = '/tmp/download/'
    os.system("rm -rf /tmp/*")
    os.mkdir(tmpdir)
    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' tmpdir is ready')

    endpoint = 'oss-cn-shanghai-internal.aliyuncs.com'
    bucketname = 'leo-demo'
    creds = context.credentials
    url_list_file = 'weibo_url_list'
    auth = oss2.StsAuth(creds.accessKeyId, creds.accessKeySecret, creds.securityToken)
    bucket = oss2.Bucket(auth, endpoint, bucketname)
    bucket.get_object_to_file('configuration/weibo_url_list', tmpdir + url_list_file)
    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' weibo_url_list is ready')

    uid_list_file = tmpdir+'weibo_uid_list'
    uid_list = []

    with open(tmpdir + url_list_file, 'r') as f_uid:
        l_uid = f_uid.readlines()
    for i in range(0, len(l_uid)):
        print('---' + str(i+1) + '/' + str(len(l_uid)) + '---')
        print('---' + l_uid[i].rstrip('\n'))
        print('---' + get_uid(l_uid[i].rstrip('\n'))['id'])
        time.sleep(1)
        uid_list.append(get_uid(l_uid[i].rstrip('\n'))['id'] + '\n')

    write_to_file(uid_list, uid_list_file, 'w')

    bucket.put_object('configuration/weibo_uid_list', uid_list_file)

    user_list = ['leo.zhai@bizfocus.cn']
    sub = "现在时间： " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = "该吃午饭了！！"
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Start to send mail!')
    # send_mail(user_list, sub, content)


if __name__ == "__main__":
    handler('1', '2')
