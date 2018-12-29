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
    oss_html_path = "process/pinguan_html/"

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
    if 1==1:
        html_key = evt['events'][0]['oss']['object']['key']
        html_url = "http://www.pinguan.com/" + html_key.replace(oss_html_path, '')
        news_html = bucket.get_object(html_key).read().decode('utf-8')
        logger.info(
            (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S') + ' Step 2: Start to parse ' + str(html_key))

        page_html = etree.HTML(news_html)
        # get items
        news_list = []
        news_list.append(html_key.split('/')[-1].replace('.html', ''))
        news_list.append(html_url)
        news_list.append(page_html.xpath('//div[@class="source"]/span[@class="mark"]/span/text()')[0])  # 新闻类别1
        news_list.append(page_html.xpath('//div[@class="source"]/span[@class="mark"]/span/text()')[0])  # 新闻类别2
        news_list.append(page_html.xpath('//div[@class="source"]/span[@class="mark"]/span/text()')[0])  # 新闻类别3
        news_list.append(page_html.xpath('//h2[@id="title"]/text()')[0].replace(',', '，'))  # 新闻标题
        news_list.append(
            page_html.xpath('//div[@class="source"]/span[@class="info"]/span/a/text()')[0])  # 新闻来源
        pubdate = str(page_html.xpath('//div[@class="source"]/span[@class="info"]/span[@class="pubdate"]/text()')[0])
        if pubdate.find('小时前')==-1:
            pubdate = pubdate + ' 00:00:00'
        else:
            pubdate = int(pubdate.replace('小时前',''))
            pubdate = (datetime.datetime.utcnow() + datetime.timedelta(hours=8-pubdate)).strftime('%Y-%m-%d %H:%M:%S')
        news_list.append(pubdate)  # 新闻时间

        news_list.append(html_key.replace('process', 'result'))  # oss html

        content_html = str(etree.tostring(page_html.xpath('//div[@class="main_con"]')[0], encoding='utf-8'))
        
        content_text = page_html.xpath('//div[@class="main_con"]')[0].xpath('string(.)')
        # reg = r'http:\/\/[^\s,"]*\.jpg'
        reg = r'http://image.pinguan.com/\/\/[^\s,"]*\.jpg'
        imgre = re.compile(reg)

        imglist = re.findall(imgre, content_html)

        # reg = r'http:\/\/[^\s,"]*\.png'
        reg = r'http://image.pinguan.com/\/\/[^\s,"]*\.png'
        imgre = re.compile(reg)
        imglist = imglist + re.findall(imgre, content_html)

        for img in imglist:
            pic = urllib.request.urlopen(img).read()

            bucket.put_object('result/imgs/pinguan' + img, pic)
        # news_list.append(';'.join(imglist).replace('http://image.pinguan.com','result/imgs/pinguan')) #oss imgs
        news_list.append('imgs')  # oss imgs
        news_list.append((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'))
        news_list.append(content_html)  # 新闻内容
        news_list.append(content_text)  # 新闻文本

        bucket.put_object(html_key.replace('process', 'result'), (
                '<html><head><meta charset="UTF-8"></head><body>' + content_html + '</body></html>').replace(
            'http://image.pinguan.com', '/result/imgs/pinguan'))

        csv_file = html_key.replace('html', 'csv')
        bucket.put_object(csv_file, '\u0000'.join(news_list).replace('\n', '').replace('\r', ''))
        logger.info(
            (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S') + ' Step 4: finish parse ' + str(html_key))
    #except Exception as e:
    #    print("产生异常" + str(e))

    if __name__ == "__main__":
        print(handler('1', '2'))