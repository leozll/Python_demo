# -*- coding: utf-8 -*-
import logging
import datetime
import time
import sys
import os
import csv

sys.path.append(os.curdir + '/func/packages/')
from func.func_requestweibocontent import *
from func.func_ossread import *
from func.func_ossappend import *
from func.func_ossput import *
from func.func_ossget import *
from func.func_sendmail import *
from func.func_nosql import *


def handler(event, context):
    uid_count = 60
    d_list = [201811]

    runtime_duration = 550
    runtime_start = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))

    datekey_uid = int((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y%m%d'))
    logger = logging.getLogger()
    logger.info(
        (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + ' Start WeiboUid')
    print('--------------------------------------------------------------------------------------')
    tmpdir = '/tmp/weibo/'
    os.system("rm -rf /tmp/*")
    os.mkdir(tmpdir)
    tmp_content_list = tmpdir + 'weibo_content_list.csv'

    # load parameters
    region = "cn-shanghai-internal"
    bucketname = "leo-demo"
    oss_uid_list = "configuration/weibo_uid_list"
    oss_content_list = "result/" + str(datekey_uid) + "/weibo_content_list.csv"

    instance_name = 'leonosql'
    ts_log = 'table_store.log'
    tbl = 'log_weibo'
    # ts_endpoint = 'https://leonosql.cn-shanghai.ots.aliyuncs.com'
    ts_region = 'cn-shanghai.ots'
    ts_endpoint = 'https://{0}.{1}.aliyuncs.com'.format(instance_name, ts_region)
    access_key_id = 'LTAIi3mUQglhfB3D'
    access_key_secret = 'y4acQJO0QkoCbaPipQDFD2idfNOVqJ'

    endpoint = 'oss-{0}.aliyuncs.com'.format(region)
    creds = context.credentials
    auth = oss2.StsAuth(creds.accessKeyId, creds.accessKeySecret, creds.securityToken)
    bucket = oss2.Bucket(auth, endpoint, bucketname)
    if bucket.object_exists(oss_content_list):
        bucket.get_object_to_file(oss_content_list, tmp_content_list)

    # get the weibo uids
    uids = []
    logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
        '%Y-%m-%d %H:%M:%S') + ' Step 1 : get weibo uids from oss')
    # if the uid_list is not exists
    if bucket.object_exists(oss_uid_list):
        content = bucket.get_object(oss_uid_list)
        uids = content.read().decode('utf-8').split("\r\n")
        uids.sort()
    else:
        logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
            '%Y-%m-%d %H:%M:%S') + ' ERROR!!! cant find uids file from oss')
        exit(1)
    # uids=["1321603287"]

    # initialize the uids
    logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
        '%Y-%m-%d %H:%M:%S') + ' Step 2 : initialize the uids status')
    # connect to the table store
    ots_client = OTSClient(ts_endpoint, access_key_id, access_key_secret, instance_name, socket_timeout=10,
                           logger_name=ts_log)
    for uid in uids:
        pk = [('uid', int(uid))]
        cols = ['status']
        if get_col(ots_client, tbl, pk, cols, None) == 'NoData':
            attr = [('status', 'waiting'), ('update_timestamp',
                                            (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                                                '%Y-%m-%d %H:%M:%S')),
                    ('update_time', int(time.time()))]
            put_row(ots_client, tbl, pk, attr)

    # get last runtime
    logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
        '%Y-%m-%d %H:%M:%S') + ' Step 3 : get the last runtime status')
    pk = [('uid', datekey_uid)]
    checkpoint = 0
    last_runtime = int(time.time())
    last_runtimestamp = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    # if no last runtime status record, initialize
    if get_col(ots_client, tbl, pk, ['update_time'], None) == 'NoData':
        attr = [('name', datekey_uid), ('status', ','.join(uids)), ('update_timestamp', last_runtimestamp),
                ('update_time', last_runtime),
                ('checkpoint', checkpoint)]
        put_row(ots_client, tbl, pk, attr)
    else:
        cols = ['status']
        # check if the weibo uids is changed, if not same
        if get_col(ots_client, tbl, pk, cols, None) != ','.join(uids):
            # initialize
            attr = [('name', datekey_uid), ('status', ','.join(uids)), ('update_timestamp', last_runtimestamp),
                    ('update_time', last_runtime),
                    ('checkpoint', checkpoint)]
            put_row(ots_client, tbl, pk, attr)
        else:
            cols = ['checkpoint']
            checkpoint = get_col(ots_client, tbl, pk, cols, None)
    logger.info(
        (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
            '%Y-%m-%d %H:%M:%S') + ' last runtime checkpoint is ' + str(checkpoint))

    # loop uid to analysis
    logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
        '%Y-%m-%d %H:%M:%S') + ' Step 4 : start to analysis weibo content')
    if checkpoint > len(uids) and get_col(ots_client, tbl, pk, ['name'], None) == datekey_uid:
        logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
            '%Y-%m-%d %H:%M:%S') + ' Step 5 : today all the uids are analysed! exit the script!')
        exit(0)
    if checkpoint + uid_count > len(uids):
        endp = len(uids)
    else:
        endp = checkpoint + uid_count
    for i in range(checkpoint, endp):
        logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
            '%Y-%m-%d %H:%M:%S') + ' Step 5 (' + str(i + 1) + '/' + str(uid_count) + ') : start to analyse uid: ' +
                    uids[i])
        for d in d_list:

            # if it will be overtime
            runtime_now = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
            runtime_seconds = (runtime_now - runtime_start).seconds
            if runtime_seconds > runtime_duration:
                if os.path.exists(tmp_content_list):
                    bucket.put_object_from_file(oss_content_list, tmp_content_list)
                # if finished
                pk = [('uid', int(uids[i]))]
                attr = [('name', int(uids[i])), ('status', 'finish'), (
                    'update_timestamp',
                    (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')),
                        ('update_time', int(time.time()))]
                put_row(ots_client, tbl, pk, attr)
                # if fi nished
                pk = [('uid', datekey_uid)]
                # overtime - update checkpoint to checkpoint+i
                attr = [('name', datekey_uid), ('status', ','.join(uids)), (
                    'update_timestamp',
                    (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')),
                        ('update_time', int(time.time())),
                        ('checkpoint', checkpoint + i)]
                put_row(ots_client, tbl, pk, attr)

                logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                    '%Y-%m-%d %H:%M:%S') + ' Step 6 : script has been running for ' + str(
                    runtime_seconds) + ' seconds...it will stop noow')
                exit(0)

            try:
                loop_starttime = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
                content_list = []
                content_list.append(uids[i])
                # get the weibo content
                content_j = weibo_content(uids[i], d)
                # 怎么判断pageToken
                # if content_j['hasNext']:
                if content_j["retcode"] != "000000":
                    logger.info(
                        (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                            '%Y-%m-%d %H:%M:%S') + '"' + str(uids[i]) + '"异常!!!...：' + str(
                            content_j['message']))

                else:
                    print(' starting to write ' + str(uids[i]) + '...')
                    content = content_j['data'][0]
                    content_list.append(content['id'])  # 文章id
                    content_list.append(content['url'])  # 文章链接
                    content_list.append(content['publishDateStr'].replace("T", " "))  # 发布时间／北京时间
                    # content_list.append(content['edit_at'])  # 最后编辑时间
                    content_list.append(content['shareCount'])  # 转发数
                    content_list.append(content['commentCount'])  # 评论数
                    content_list.append(content['likeCount'])  # 点赞数
                    content_list.append(content['content'].replace("\n", ""))  # 文章内容
                    if content['imageURLs'] is not None:
                        content_list.append(';'.join(content['imageURLs']))  # 图片链接
                    else:
                        content_list.append('')
                    if 'retweeted_status' in content['mblog']:
                        content_list.append(content['mblog']['retweeted_status']['user']['id'])  # 转发作者uid
                        content_list.append(content['mblog']['retweeted_status']['id'])  # 转发文章id
                        content_list.append(content['mblog']['retweeted_status']['created_at'])  # 转发文章发布时间
                        content_list.append(content['mblog']['retweeted_status']['text'].replace("\n", ""))  # 转发内容
                        if content['mblog']['retweeted_status']['pic_urls'] is not None:
                            if content['mblog']['retweeted_status']['pic_urls'] != []:
                                content_list.append(';'.join(
                                    list(content['mblog']['retweeted_status']['pic_urls'][0].values())))  # 转发内容图片
                        else:
                            content_list.append('')
                    else:
                        content_list.append('')
                        content_list.append('')
                        content_list.append('')
                        content_list.append('')
                        content_list.append('')
                    with open(tmp_content_list, 'a', newline='') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow(content_list)
                    if ((datetime.datetime.utcnow() + datetime.timedelta(
                            hours=8)) - loop_starttime).microseconds < 1000:
                        print('toooooo fast!!! sleep ' + str(
                            1 - ((datetime.datetime.utcnow() + datetime.timedelta(
                                hours=8)) - loop_starttime).microseconds / 1000) + ' microseconds......')
                        time.sleep(1 - ((datetime.datetime.utcnow() + datetime.timedelta(
                            hours=8)) - loop_starttime).microseconds / 1000)
            except Exception  as e:
                logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                    '%Y-%m-%d %H:%M:%S') + '"' + str(uids[i]) + '"解析失败????...：' + str(e))

        if os.path.exists(tmp_content_list):
            bucket.put_object_from_file(oss_content_list, tmp_content_list)
        # if finished
        pk = [('uid', int(uids[i]))]
        attr = [('name', int(uids[i])), ('status', 'finish'), (
            'update_timestamp',
            (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')),
                ('update_time', int(time.time()))]
        put_row(ots_client, tbl, pk, attr)
    # if fi nished
    pk = [('uid', datekey_uid)]
    attr = [('name', datekey_uid), ('status', ','.join(uids)), (
        'update_timestamp', (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')),
            ('update_time', int(time.time())),
            ('checkpoint', checkpoint + uid_count)]
    put_row(ots_client, tbl, pk, attr)

    # pk=[('uid',100)]
    # attr = [('name', 'leo'), ('status', 'running'),('money',2000)]
    # list_table(ots_client)
    # put_row(ots_client,tbl,pk,attr)
    # cols = ['status']
    # print (get_log_status(ots_client, tbl, pk, cols,SingleColumnCondition("status", 'running1', ComparatorType.EQUAL)))


if __name__ == "__main__":
    handler('1', '2')