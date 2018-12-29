# -*- coding: utf-8 -*-
import logging
import datetime
import time
import oss2
import requests
import logging
import json
import re
import urllib.request

from lxml import etree


def handler(event, context):
    evt = json.loads(event)
    oss_html_path = "process/zhixiaoren/zhixiaoren_html/"
    oss_imgs_path = "result/zhixiaoren/img/"

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
        html_key = evt['events'][0]['oss']['object']['key']
        html_url = "http://news.zhixiaoren.com/" + html_key.replace(oss_html_path, '')
        csv_file = html_key.replace('html', 'csv')

        if bucket.object_exists(csv_file):
            logger.info('------------------------- ' + csv_file + ' is existing in the process folder!')
            return -1
        news_html = bucket.get_object(html_key).read().decode('utf-8')
        logger.info(
            (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S') + ' Step 2: Start to parse ' + str(html_key))

        page_html = etree.HTML(news_html)
        # get items
        news_list = []
        news_list.append(page_html.xpath('//h1[@class="overf"]/text()')[0])  # title
        news_list.append(etree.HTML(str(page_html.xpath('//div[@id="news_content"]/node()')[1])[4:-3]).xpath(
            'string(.)').strip())  # content
        news_list.append(page_html.xpath('//div[@class="div-l"]/span')[1].text)  # publish time
        news_list.append('/'+html_key.replace('process', 'result'))  # oss html
        news_list.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))))  # insert_time
        sub_source = '直销人-' + \
                     page_html.xpath('//div[@class="newsNav2"]/span/a/text()')[2].replace('\n', '').replace('\t', '') + \
                     '-'+\
                     page_html.xpath('//div[@class="div-l"]/span/a/text()')[0]
        news_list.append(sub_source)  # sub source
        news_list.append(html_url)  # original html

        imglist = etree.HTML(str(page_html.xpath('//div[@id="news_content"]/node()')[1])[4:-3]).xpath('//img/@src')
        pic_list = []
        for img in imglist:
            if img[-3:] != 'gif':
                pic_list.append(img)
        for img in pic_list[:10]:
            pic = urllib.request.urlopen(img).read()
            pic_path = img.replace('http://oss.zhixiaoren.com/', oss_imgs_path)
            bucket.put_object(pic_path, pic)
        news_list.append(
            ';'.join(pic_list[:10]).replace('http://oss.zhixiaoren.com/', '/'+oss_imgs_path))  # oss imgs

        html_code = ('<html><head><meta charset="UTF-8"><link rel="stylesheet" href="/result/zhixiaoren/header/css/main.css"></head><body>' +
                     str(page_html.xpath('//div[@id="news_content"]/node()')[1])[4:-3] + '</body></html>'
                     ).replace('http://oss.zhixiaoren.com/', '/' + oss_imgs_path)
        bucket.put_object(html_key.replace('process', 'result'), html_code)

        bucket.put_object(csv_file, '\u0000'.join(news_list).replace('\n', '').replace('\r', ''))
        bucket.put_object(csv_file.replace('process', 'result'), '\u0000'.join(news_list).replace('\n', '').replace('\r', ''))
        logger.info(
            (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S') + ' Step 4: finish parse ' + str(html_key))
    except Exception as e:
        print("发生异常！" + str(e))


if __name__ == "__main__":
    print(handler('1', '2'))

