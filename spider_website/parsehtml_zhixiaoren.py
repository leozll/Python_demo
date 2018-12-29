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

    region = "cn-hangzhou-internal"
    bucketname = "leo-hangzhou"
    endpoint = 'oss-{0}.aliyuncs.com'.format(region)
    creds = context.credentials
    auth = oss2.StsAuth(creds.accessKeyId, creds.accessKeySecret, creds.securityToken)
    bucket = oss2.Bucket(auth, endpoint, bucketname)
    logger = logging.getLogger()
    logger.info(
        (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
            '%Y-%m-%d %H:%M:%S') + ' Step 1: Starting to parse html')
    try:
        print (0)
        html_key = evt['events'][0]['oss']['object']['key']
        print (1)
        news_html = bucket.get_object(html_key).read().decode('utf-8')
        print (2)
        logger.info(
            (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S') + ' Step 2: Start to parse ' + str(html_key))

        page_html = etree.HTML(news_html)
        # get items
        news_list = []
        news_list.append(page_html.xpath('//h1[@class="overf"]/text()')[0].replace(',','，')) #新闻标题
        news_list.append(page_html.xpath('//div[@class="div-l"]/span')[0].xpath('string(.)').replace('\n','').replace(' ','').strip().replace(',','，')) #新闻来源
        news_list.append(page_html.xpath('//div[@class="div-l"]/span')[1].text.replace(',','，')) #新闻时间
        news_list.append(str(page_html.xpath('//div[@id="news_content"]/node()')[1])[4:-3].replace(',','，'))   #新闻内容

        csv_file = html_key.replace('html', 'csv')
        bucket.put_object(csv_file, str(news_list))

    except Exception as e:
        print ("产生异常" + str(e))


if __name__ == "__main__":
    print(handler('1', '2'))