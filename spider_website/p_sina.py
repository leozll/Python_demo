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
    oss_html_path = "process/sina_html/"

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
        html_url = "http://" + html_key.replace(oss_html_path, '')
        news_html = bucket.get_object(html_key).read().decode('utf-8')
        logger.info(
            (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S') + ' Step 2: Start to parse ' + str(html_key))

        page_html = etree.HTML(news_html)
        # get items
        news_list = []
        news_list.append(html_key.split('/')[-1].replace('.html', ''))
        news_list.append(html_url)
        news_list.append(page_html.xpath('//div[@class="channel-path"]/a/text()')[0])  # 新闻类别1
        news_list.append(page_html.xpath('//div[@class="channel-path"]/a/text()')[1])  # 新闻类别2
        news_list.append(page_html.xpath('//div[@class="channel-path"]/a/text()')[2])  # 新闻类别3
        news_list.append(page_html.xpath('//h1[@class="main-title"]/text()')[0].replace(',', '，'))  # 新闻标题
        news_list.append(page_html.xpath('//div[@class="date-source"]/span/text()')[1])  # 新闻来源
        news_list.append(page_html.xpath('//div[@class="date-source"]/span/text()')[1].replace('年','-').replace('月','-').replace('日','')+':00')  # 新闻时间

        news_list.append(html_key.replace('process', 'result'))  # oss html


        content_html = str(etree.tostring(page_html.xpath('//div[@class="article"]')[0], encoding='utf-8'))
        content_text = page_html.xpath('string(//div[@class="article"])').replace("""window.sina_survey_config = {
    					surveyCss: true,               //调查问答样式true, false, http （不使用默认样式配置false或者不传此参数）
    					resultCss: true,               //调查结果样式true, false, http （不使用默认样式配置false或者不传此参数）
    					source: 'vote'               //通过来源设置图片宽高 sina(手浪), vote(默认)
					}
				
""","")
        print(content_text)
        # reg = r'http:\/\/[^\s,"]*\.jpg'
        reg = r'http://n.sinaimg.cn/\/\/[^\s,"]*\.jpg'
        imgre = re.compile(reg)

        imglist = re.findall(imgre, content_html)

        # reg = r'http:\/\/[^\s,"]*\.png'
        reg = r'http://n.sinaimg.cn/\/\/[^\s,"]*\.png'
        imgre = re.compile(reg)
        imglist = imglist + re.findall(imgre, content_html)
        reg = r'http://n.sinaimg.cn/\/\/[^\s,"]*\.gif'
        imgre = re.compile(reg)
        imglist = imglist + re.findall(imgre, content_html)

        pic_list = []
        for img in imglist:
            if img[-3:]!='gif':
                pic_list.append(img)
        for img in pic_list[:10]:
            pic = urllib.request.urlopen(img).read()
            bucket.put_object(img.replace('http://n.sinaimg.cn', 'result/imgs/sina'), pic)

        news_list.append(';'.join(pic_list[:10]).replace('http://n.sinaimg.cn','result/imgs/sina')) #oss imgs
        news_list.append((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'))
        news_list.append(content_html)  # 新闻内容
        news_list.append(content_text)  # 新闻文本

        bucket.put_object(html_key.replace('process', 'result'), (
                '<html><head><meta charset="UTF-8"></head><body>' + content_html + '</body></html>').replace(
            'http://n.sinaimg.cn', '/result/imgs/sina'))

        csv_file = html_key.replace('html', 'csv')
        bucket.put_object(csv_file, '\u0000'.join(news_list).replace('\n', '').replace('\r', ''))
        logger.info(
            (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S') + ' Step 4: finish parse ' + str(html_key))
    except Exception as e:
        print("产生异常" + str(e))

    if __name__ == "__main__":
        print(handler('1', '2'))