# -*- coding: utf-8 -*-
import logging
import datetime
import time
import oss2
import requests
import logging
import json
from lxml import etree


def handler(event, context):
    evt = json.loads(event)

    url_prefix = "http://news.zhixiaoren.com/list/1_"
    homepage_url = url_prefix + "1.html"
    oss_html_path = "process/zhixiaoren_html/"

    region = "cn-hangzhou-internal"
    bucketname = "leo-hangzhou"
    endpoint = 'oss-{0}.aliyuncs.com'.format(region)
    creds = context.credentials
    auth = oss2.StsAuth(creds.accessKeyId, creds.accessKeySecret, creds.securityToken)
    bucket = oss2.Bucket(auth, endpoint, bucketname)
    logger = logging.getLogger()
    logger.info(
        (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
            '%Y-%m-%d %H:%M:%S') + ' Step 1: Starting to parse url')
    try:
        json_key = evt['events'][0]['oss']['object']['key']
        news_url = eval(bucket.get_object(json_key).read().decode('utf-8'))
        print (news_url)
        logger.info(
            (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S') + ' Step 2: Start to parse ' + news_url)
        news_r = requests.get(news_url, timeout=10)  # 请求超时时间为10秒
        news_r.raise_for_status()  # 如果状态不是200，则引发异常
        news_r.encoding = news_r.apparent_encoding  # 配置编码
        html_file = oss_html_path + news_url.replace('http://news.zhixiaoren.com/', '')
        bucket.put_object(html_file, '{0}'.format(news_r.text))

        print (news_url)
    except Exception as e:
        print ("产生异常" + str(e))


if __name__ == "__main__":
    print(handler('1', '2'))