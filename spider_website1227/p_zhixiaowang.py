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
    oss_html_path = "process/zhixiaowang_html/"

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
        html_url = "http://news.zhixiaowang.com/" + html_key.replace(oss_html_path, '')
        news_html = bucket.get_object(html_key).read().decode('utf-8')
        logger.info(
            (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S') + ' Step 2: Start to parse ' + str(html_key))

        page_html = etree.HTML(news_html)
        # get items
        news_list = []
        news_list.append(html_key.split('/')[-1].replace('.html', ''))  #id
        news_list.append(html_url)  #url
        news_list.append(page_html.xpath('//div[@id="dangqian"]/a/text()')[0])  # 新闻类别1
        news_list.append(page_html.xpath('//div[@id="dangqian"]/a/text()')[1])  # 新闻类别2
        news_list.append(page_html.xpath('//div[@id="dangqian"]/a/text()')[2])  # 新闻类别3
        news_list.append(page_html.xpath('//div[@class="title"]/h1/text()')[0].replace(',', '，'))  # 新闻标题
        news_list.append(page_html.xpath('//div[@class="title"]/p/text()')[0].split(':')[-1].strip())  # 新闻来源
        news_list.append(page_html.xpath('//div[@class="title"]/p/text()')[0].split(': ')[1].replace('作者','').strip())  # 新闻时间
        news_list.append(html_key.replace('process', 'result'))  # oss html


        content_html = str(etree.tostring(page_html.xpath('//div[@id="endtext"]')[0], encoding = "gb2312", pretty_print = True, method = "html"))
        content_text = page_html.xpath('//div[@id="endtext"]')[0].xpath('string(.)')
        # reg = r'http:\/\/[^\s,"]*\.jpg'
        reg = r'http://oss.zhixiaowang.com\/\/[^\s,"]*\.jpg'
        imgre = re.compile(reg)

        imglist = re.findall(imgre,content_html)


        # reg = r'http:\/\/[^\s,"]*\.png'
        reg = r'http://oss.zhixiaowang.com\/\/[^\s,"]*\.png'
        imgre = re.compile(reg)
        imglist = imglist + re.findall(imgre, content_html)

        for img in imglist:
            pic = urllib.request.urlopen(img).read()
            bucket.put_object(img.replace('http://oss.zhixiaowang.com','result/imgs/zhixiaowang'), pic)
        # news_list.append(';'.join(imglist).replace('http://oss.zhixiaowang.com','result/imgs/zhixiaowang')) #oss imgs
        news_list.append('imgs')  # oss imgs
        news_list.append((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'))
        news_list.append(content_html)  # 新闻内容
        news_list.append(content_text)  # 新闻文本

        bucket.put_object(html_key.replace('process', 'result'), (
                    '<html><head><meta charset="gbk"></head><body>' + content_html + '</body></html>').replace(
            'src="/uploadfile', 'src="/result/imgs/zhixiaowang/uploadfile'))

        csv_file = html_key.replace('html', 'csv')
        bucket.put_object(csv_file, '\u0000'.join(news_list).replace('\n', '').replace('\r', ''))
        logger.info(
            (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S') + ' Step 4: finish parse ' + str(html_key))
    #except Exception as e:
    #    print("产生异常" + str(e))


if __name__ == "__main__":
    print(handler('1', '2'))