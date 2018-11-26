# -*- coding: utf-8 -*-
import logging
import datetime
import time
import sys
import os
import json
import oss2
from tablestore import *

sys.path.append(os.curdir + '/func/packages/')
from func.func_requestweibocontent import *
from func.func_sendmail import *
from func.func_nosql import *


def handler(event, context):
    evt = json.loads(event)
    #print(evt)
    datekey_uid = int((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y%m%d'))
    oss_json_path = "process/weibo_json/"
    oss_csv_path = "process/weibo_csv/"
    oss_json_result = "result/weibo_json/"

    logger = logging.getLogger()
    logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + '--------------------------------------------------------------------------------------')
    logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + ' Start parse the oss json file......')

    bucketname = evt['events'][0]['oss']['bucket']['name']
    region = evt['events'][0]['region']
    endpoint = 'oss-{0}.aliyuncs.com'.format(region)
    creds = context.credentials
    access_key_id = creds.accessKeyId
    access_key_secret = creds.accessKeySecret
    auth = oss2.StsAuth(access_key_id, access_key_secret, creds.securityToken)
    bucket = oss2.Bucket(auth, endpoint, bucketname)

    # connect to the table store
    instance_name = 'leo-ts-hangzhou'
    ts_log = 'table_store.log'
    tbl = 'log_parse_json'
    err_tbl = 'log_parse_json_error'
    #ts_endpoint = 'https://{0}.{1}.ots-internal.aliyuncs.com'.format(instance_name, region)
    #ots_client = OTSClient(ts_endpoint, access_key_id, access_key_secret, instance_name, socket_timeout=10,logger_name=ts_log)

    access_key_id = 'LTAIi3mUQglhfB3D'
    access_key_secret = 'y4acQJO0QkoCbaPipQDFD2idfNOVqJ'
    ts_endpoint = 'https://{0}.{1}.ots.aliyuncs.com'.format(instance_name, region)
    ots_client = OTSClient(ts_endpoint, access_key_id, access_key_secret, instance_name, socket_timeout=10,logger_name=ts_log)



    # get object from event when post object
    json_key = evt['events'][0]['oss']['object']['key']
    json_file_meta = bucket.get_object_meta(json_key)
    content_length = json_file_meta.content_length
    last_modified = json_file_meta.last_modified
    logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + ' Step 1: found file ' + json_key + '(modified: ' + str(last_modified) + ')')
    pk = [('datekey', datekey_uid), ('jsonkey', json_key)]
    attr = [('name', json_key),
            ('length', content_length),
            ('last_modified', last_modified),
            ('status', 'ready'),
            ('update_timestamp',(datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')),
            ('update_time', int(time.time()))]
    put_row(ots_client, tbl, pk, attr)

    logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + ' Step 2: start to parse ' + json_key )

    #read the file
    #print (bucket.get_object(json_key).read().decode('utf-8'))
    content_str = bucket.get_object(json_key).read().decode('utf-8')
    content = eval(content_str)
    content_list = []
    content_list.append(content['id'])  # 文章id
    content_list.append(content['url'])  # 文章链接
    content_list.append(content['mblog']['localPublishDateStr'])  # 发布时间／北京时间
    if 'edit_at' in content:
        content_list.append(content['edit_at'])  # 最后编辑时间
    else:
        content_list.append('')
    content_list.append(content['shareCount'])  # 转发数
    content_list.append(content['commentCount'])  # 评论数
    content_list.append(content['likeCount'])  # 点赞数
    content_list.append(content['content'].replace("\n", ""))  # 文章内容
    content_list.append(content['mblog']['source'])  # 来自
    if content['imageURLs'] is not None:
        content_list.append(';'.join(content['imageURLs']))  # 图片链接
    else:
        content_list.append('')
    if 'retweeted_status' in content['mblog']:
        content_list.append(content['mblog']['retweeted_status']['user']['id'])  # 转发作者uid
        content_list.append(content['mblog']['retweeted_status']['id'])  # 转发文章id
        content_list.append(content['mblog']['retweeted_status']['created_at'])  # 转发文章发布时间
        content_list.append(content['mblog']['retweeted_status']['text'].replace("\n", ""))  # 转发内容
        content_list.append(content['mblog']['retweeted_status']['reposts_count'])  # 转发文章转发数
        content_list.append(content['mblog']['retweeted_status']['comments_count'])  # 转发文章评论数
        content_list.append(content['mblog']['retweeted_status']['attitudes_count'])  # 转发文章点赞数
        if content['mblog']['retweeted_status']['pic_urls'] is not None:
            if content['mblog']['retweeted_status']['pic_urls'] != []:
                content_list.append(';'.join(
                    list(content['mblog']['retweeted_status']['pic_urls'][0].values())))  # 转发内容图片
        else:
            content_list.append('')
        content_list.append(content['mblog']['retweeted_status']['source'])  # 转发文章来自
    else:
        content_list.append('')
        content_list.append('')
        content_list.append('')
        content_list.append('')
        content_list.append('')
        content_list.append('')
    content_list.append((datetime.datetime.utcnow() + datetime.timedelta(
        hours=8)))

    csv_file = json_key.replace('json','csv')

    logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + ' Step 3: unload result to ' + csv_file )
    #unload the csv file
    bucket.put_object(csv_file, str(content_list))
    result_json = json_key.replace('process', 'result')
    # copy json file from process to result
    bucket.put_object(result_json, content_str)
    # delete process json file
    bucket.delete_object(json_key)

    pk = [('datekey', datekey_uid), ('jsonkey', json_key)]
    attr = [('name', json_key),
            ('length', content_length),
            ('last_modified', last_modified),
            ('status', 'finish'),
            ('update_timestamp',(datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')),
            ('update_time', int(time.time()))]
    #update log
    put_row(ots_client, tbl, pk, attr)
    logger.info((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + ' Step 4: ' + csv_file +' is ready!')

    return 'Congratulations! ' + (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    handler('1', '2')
