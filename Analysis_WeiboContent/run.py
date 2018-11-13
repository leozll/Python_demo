# -*- coding: utf-8 -*-
import logging
import datetime
import time
import sys
import os
import csv

sys.path.append(os.curdir + '/func/packages/')
from func.func_requestweiboprofile import *
from func.func_ossread import *
from func.func_ossappend import *
from func.func_ossput import *
from func.func_ossget import *
from func.func_sendmail import *
from func.func_nosql import *

def handler(event, context):

    uid_count=10

    logger = logging.getLogger()
    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Start WeiboUid')
    print('--------------------------------------------------------------------------------------')
    tmpdir = '/tmp/weibo/'
    os.system("rm -rf /tmp/*")
    os.mkdir(tmpdir)
    tmp_profile_list = tmpdir + 'weibo_profile_list.csv'

    # load parameters
    region = "cn-shanghai-internal"
    bucketname = "leo-demo"
    oss_uid_list = "configuration/weibo_uid_list"
    oss_profile_list = "configuration/weibo_profile_list.csv"
    oss_status = "logs/weibo_status"
    analysis_count = 100

    ts_endpoint = 'https://leonosql.cn-shanghai.ots.aliyuncs.com'
    access_key_id='LTAIi3mUQglhfB3D'
    access_key_secret='y4acQJO0QkoCbaPipQDFD2idfNOVqJ'
    instance_name='leonosql'
    ts_log='table_store.log'

    endpoint = 'oss-{0}.aliyuncs.com'.format(region)
    creds = context.credentials
    auth = oss2.StsAuth(creds.accessKeyId, creds.accessKeySecret, creds.securityToken)
    bucket = oss2.Bucket(auth, endpoint, bucketname)

    tbl = 'log_weibo'

    #get the weibo uids
    uids=[]
    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Step 1 : get weibo uids from oss')
    #if the uid_list is not exists
    if bucket.object_exists(oss_uid_list):
        content = bucket.get_object(oss_uid_list)
        uids = content.read().decode('utf-8').split("\r\n").sort()
    else :
        logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ERROR!!! cant find uids file from oss')
        exit(1)

    #initialize the uids
    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Step 2 : initialize the uids status')
    #connect to the table store
    ots_client = OTSClient(ts_endpoint, access_key_id, access_key_secret, instance_name, socket_timeout=10,logger_name=ts_log)
    for uid in uids:
        pk = [('uid',int(uid))]
        cols = ['status']
        if get_col(ots_client, tbl, pk, cols, None) == 'NoData':
            attr = [('status', 'waiting'),('update_timestamp',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),('update_time',int(time.time()))]
            put_row(ots_client, tbl, pk, attr)

    #get last runtime
    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Step 3 : get the last runtime status')
    pk = [('uid',0)]
    checkpoint = 0
    last_runtime = int(time.time())
    last_runtimestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #if no last runtime status record, initialize
    if get_col(ots_client, tbl, pk, ['update_time'], None) == 'NoData':
        attr = [('status', uids),('update_timestamp',last_runtimestamp),('update_time',last_runtime),('checkpoint', checkpoint)]
        put_row(ots_client, tbl, pk, attr)
    else:
        cols = ['status']
        #check if the weibo uids is changed, if not same
        if get_col(ots_client, tbl, pk, cols, None)! = uids:
            #initialize
            attr = [('status', uids), ('update_timestamp', last_runtimestamp), ('update_time', last_runtime),
                    ('checkpoint', checkpoint)]
            put_row(ots_client, tbl, pk, attr)
        else:
            cols = ['checkpoint']
            checkpoint=get_col(ots_client, tbl, pk, cols, None)
    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' last runtime checkpoint is '+checkpoint)

    #loop uid to analysis
    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Step 4 : start to analysis weibo content')
    for i in range(checkpoint,checkpoint+uid_count):
        print ('start '+str(i)+'/'+str(uid_count)+' - uid: '+uids[i])

        content_list=[]
        content_list.append(uid)
        #get the weibo content
        content_j = weibo_content(uid, d)
        time.sleep(1)
        if content_j["retcode"] != "000000":
            logger.info(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '"' + str(uid) + '"异常!!!...：' + str(
                    content_j['message']))
        else:
            logger.info(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' starting to analyse ' + str(uid) + '...')
            content = content_j['data'][0]
            content_list.append(content['id'])  #文章id
            content_list.append(content['publishDateStr'].replace("T", " "))  # 发布时间／北京时间
            content_list.append(content['shareCount']) #转发数
            content_list.append(content['commentCount'])    #评论数
            content_list.append(content['likeCount'])  #点赞数
            content_list.append(content['content'])  #文章内容
            content_list.append(content['url']) #文章链接
            content_list.append(';'.join(content['imageURLs'])) #图片链接
            if content.has_key('retweeted_status')：
            content_list.append(content['retweeted_status']['text']) #转发内容

        #if finished
        pk = [('uid',uids[i])]
        attr = [('status', 'finish'),('update_timestamp',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),('update_time',int(time.time()))]
        put_row(ots_client, tbl, pk, attr)



    #pk=[('uid',100)]
    #attr = [('name', 'leo'), ('status', 'running'),('money',2000)]
    #list_table(ots_client)
    #put_row(ots_client,tbl,pk,attr)
    #cols = ['status']
    #print (get_log_status(ots_client, tbl, pk, cols,SingleColumnCondition("status", 'running1', ComparatorType.EQUAL)))


if __name__ == "__main__":
    handler('1', '2')
