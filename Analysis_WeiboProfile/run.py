# -*- coding: utf-8 -*-
import logging
import datetime
import time
import sys
import os

sys.path.append(os.curdir + '/func/packages/')
from func.func_requestweiboprofile import *
from func.func_ossread import *


def handler(event, context):
    logger = logging.getLogger()
    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Start WeiboUid')
    print('--------------------------------------------------------------------------------------')
    tmpdir = '/tmp/weibo/'
    os.system("rm -rf /tmp/*")
    os.mkdir(tmpdir)
    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' tmpdir is ready')




    #load parameters
    region = "cn-shanghai-internal"
    bucketname = "leo-demo"
    oss_brand_list = "configuration/weibo_brand_list"
    oss_profile_list = "configuration/weibo_profile_list.csv"
    oss_status = "configuration/weibo_status"
    analysis_count=10

    #check analysis status
    status = oss_read(context, region, bucketname, oss_status)
    #if no status file, start from row 1
    if status=="ObjectNotExists":
        logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' This is first run...')
        analysis_start = 1
    else:
        analysis_start = int(status.strip("\r\n"))

    #request webi profile
    brand_list=oss_read(context, region, bucketname, oss_brand_list)
    #if no brand file, exit -1
    if brand_list=="ObjectNotExists":
        logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Brand file is missing!!!...')
        return -1
    else:
        brand_list = brand_list.split("\r\n")[analysis_start-1:analysis_start+analysis_count-1]
        for brnd_kw in brand_list:
            profile_j = weibo_profile(brnd_kw)
            if profile_j["retcode"]=="100005":
                logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + brnd_kw+'不存在!!!...')
            else:
                profile = weibo_profile(brnd_kw)['data'][0]
                profile_info=""
                for v in profile.values():
                    profile_info=v+','+profile_info
                oss_append(context, region, bucketname, oss_profile_list, data)
    user_list = ['leo.zhai@bizfocus.cn']
    sub = "现在时间： " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = "该吃午饭了！！"
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Start to send mail!')
    # send_mail(user_list, sub, content)


if __name__ == "__main__":
    handler('1', '2')
