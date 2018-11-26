# -*- coding: utf-8 -*-
import logging
import datetime
import time
import sys
import os
import oss2

sys.path.append(os.curdir + '/func/packages/')
from func.func_requestweibocontent import *
from func.func_sendmail import *
from func.func_nosql import *


def handler(event, context):
    uid_count = 100
    d_list = [201801,201802,201803,201804,201805]
    #d_list = [201801,201802,201803,201804,201805,201806,201807,201808,201809,201810,201811]
    user_list = ['leo.zhai@bizfocus.cn']

    tmpdir = '/tmp/weibo/'
    # oss
    region = "cn-hangzhou-internal"
    bucketname = "leo-hangzhou"
    oss_uid_list = "configuration/weibo_uid_list"
    oss_json_path = "process/weibo_json/"

    #table storehang'zhou
    instance_name = 'leo-ts-hangzhou'
    ts_log = 'table_store.log'
    tbl = 'log_weibo'
    err_tbl = 'log_weibo_error'
    ts_region = 'cn-hangzhou.ots'
    ts_endpoint = 'https://{0}.{1}.aliyuncs.com'.format(instance_name, ts_region)
    access_key_id = 'LTAIi3mUQglhfB3D'
    access_key_secret = 'y4acQJO0QkoCbaPipQDFD2idfNOVqJ'

    datekey_uid = int((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y%m%d'))
    os.system("rm -rf /tmp/*")
    os.mkdir(tmpdir)

    logger = logging.getLogger()
    logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + '--------------------------------------------------------------------------------------')
    logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + ' Start WeiboUid')


    endpoint = 'oss-{0}.aliyuncs.com'.format(region)
    creds = context.credentials
    auth = oss2.StsAuth(creds.accessKeyId, creds.accessKeySecret, creds.securityToken)
    bucket = oss2.Bucket(auth, endpoint, bucketname)


    # get the weibo uids
    uids = []
    logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + ' Step 1 : get weibo uids from oss')
    # if the uid_list is not exists
    if bucket.object_exists(oss_uid_list):
        content = bucket.get_object(oss_uid_list)
        uids = content.read().decode('utf-8').split("\r\n")
        uids.sort()
    else:
        logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + ' ERROR!!! cant find uids file from oss')
        exit(1)
    #uids=["1817559703"]

    # initialize the uids
    logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + ' Step 2 : initialize the uids status')
    # connect to the table store
    ots_client = OTSClient(ts_endpoint, access_key_id, access_key_secret, instance_name, socket_timeout=10,logger_name=ts_log)
    for uid in uids:
        pk = [('uid', int(uid))]
        #if no this uid
        if get_col(ots_client, tbl, pk, ['status'], None) == 'NoData':
            attr = [('status', 'waiting'),
                    ('update_timestamp',(datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')),
                    ('update_time', int(time.time()))]
            put_row(ots_client, tbl, pk, attr)

    # get last runtime
    logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + ' Step 3 : get the last runtime status')
    pk = [('uid', datekey_uid)]
    checkpoint = 0
    last_runtime = int(time.time())
    last_runtimestamp = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    # if no last runtime status record, initialize
    if get_col(ots_client, tbl, pk, ['update_time'], None) == 'NoData' or get_col(ots_client, tbl, pk, ['status'], None) != ','.join(uids):
        attr = [('name', datekey_uid), ('status', ','.join(uids)),
                ('update_timestamp', last_runtimestamp),
                ('update_time', last_runtime),
                ('checkpoint', checkpoint)]
        put_row(ots_client, tbl, pk, attr)
        #if no change, get the last checkpoint
    else:
        cols = ['checkpoint']
        checkpoint = get_col(ots_client, tbl, pk, cols, None)
    logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + ' last runtime checkpoint is ' + str(checkpoint))

    # loop uid to analysis
    logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + ' Step 4 : start to analysis weibo content')
    #if all the uids are analysed today
    if checkpoint >= len(uids) and get_col(ots_client, tbl, pk, ['name'], None) == datekey_uid:
        logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + ' Step 5 :  all the uids are analysed today! exit the script! (checkpoint:' + str(checkpoint) + ' totally:' + str(len(uids)) + ')')
        return 'Congratulations! no uids are left! ' + (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
            '%Y-%m-%d %H:%M:%S')
    #if this is the last run
    if checkpoint + uid_count > len(uids):
        endp = len(uids)
    else:
        endp = checkpoint + uid_count

    #loop current run
    for i in range(checkpoint, endp):
        logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + ' Step 5 (' + str(i + 1) + '/' + str(endp) + ') : start to analyse uid: ' + uids[i])
        request_status = ''
        #loop the months
        for d in d_list:
            try:
                logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                    '%Y-%m-%d %H:%M:%S') + ' Step 5.1 start to analyse uid: ' + uids[i] + ' date: ' + str(d))
                loop_starttime = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
                # get the weibo content
                request_page = 1
                global  content_j
                page_hasNext = True
                # 怎么判断pageToken
                while page_hasNext:
                    content_j = weibo_content(uids[i], d ,request_page)
                    page_hasNext = content_j['hasNext']
                    request_status = content_j["retcode"]

                    print ('start to unload page ' + str(request_page) + '......')
                    for content_data in content_j['data']:
                        publish_year = content_data['mblog']['localPublishDateStr'][0:4]
                        publish_month = content_data['mblog']['localPublishDateStr'][5:7]
                        publish_date = content_data['mblog']['localPublishDateStr'][8:10]
                        json_file = oss_json_path + publish_year + '/' + publish_month + '/' + publish_date + '/' + str(uids[i]) + '/'+ content_data['id'] + '.json'
                        #bucket.put_object(json_file, json.dumps(content_data))
                        bucket.put_object(json_file, '{0}'.format(content_data))

                    print('page ' + str(request_page) + " finished......")
                    time.sleep(1)
                    request_page = request_page + 1

                print(str(uids[i]) + str(d) + '解析完毕......')
            except Exception  as e:
                request_status = str(e)
                pk = [('uid', int(uids[i])), ('datekey', datekey_uid)]
                attr = [('error_log', str(e)),
                        ('update_timestamp',(datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')),
                        ('update_time', int(time.time()))]
                put_row(ots_client, err_tbl, pk, attr)
                logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + '"' + str(uids[i]) + ' ' + str(d) +' "解析失败????...：' + str(e))
            time.sleep(1)
        # if finished
        pk = [('uid', int(uids[i]))]
        attr = [('name', int(uids[i])),
                ('status', str(request_status)),
                ('update_timestamp',(datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')),
                ('update_time', int(time.time()))]
        put_row(ots_client, tbl, pk, attr)
        # if finished
        pk = [('uid', datekey_uid)]
        attr = [('name', datekey_uid),
                ('status', ','.join(uids)),
                ('update_timestamp', (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')),
                ('update_time', int(time.time())),
                ('checkpoint', i)]
        put_row(ots_client, tbl, pk, attr)

    #sub = str(len(uids)) + ' uids are requested finished! pls check the log?'
    #content = 'log link : XXXXX?'
    #send_mail(user_list, sub, content)
    if checkpoint >= len(uids) and get_col(ots_client, tbl, pk, ['name'], None) == datekey_uid:
        logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + ' Step 6 :  all the uids are analysed today! exit the script! (checkpoint:' + str(checkpoint) + ' totally:' + str(len(uids)) + ')')
        sub = str(len(uids)) + ' uids are requested finished! pls check the log?'
        content = 'log link : XXXXX?'
        send_mail(user_list, sub, content)
    return 'Congratulations! ' + (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
if __name__ == "__main__":
    handler('1', '2')
