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
            '%Y-%m-%d %H:%M:%S') + ' Step 1: Starting to parse html')
    try:
        html_key = evt['events'][0]['oss']['object']['key']
        html_url = "http://news.zhixiaoren.com/" + html_key.replace(oss_html_path, '')
        news_html = bucket.get_object(html_key).read().decode('utf-8')
        logger.info(
            (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S') + ' Step 2: Start to parse ' + str(html_key))

        page_html = etree.HTML(news_html)
        # get items
        news_list = []
        news_list.append(html_key.split('/')[-1].replace('.html',''))
        news_list.append(html_url)
        news_list.append(page_html.xpath('//div[@class="newsNav2"]/span/a/text()')[0]) #新闻类别1
        news_list.append(page_html.xpath('//div[@class="newsNav2"]/span/a/text()')[1]) #新闻类别2
        news_list.append(page_html.xpath('//div[@class="newsNav2"]/span/a/text()')[2].replace('\n','').replace('\t','')) #新闻类别3
        news_list.append(page_html.xpath('//h1[@class="overf"]/text()')[0].replace(',','，')) #新闻标题
        news_list.append(page_html.xpath('//div[@class="div-l"]/span')[0].xpath('string(.)').replace('\n','').replace(' ','').strip()) #新闻来源
        news_list.append(page_html.xpath('//div[@class="div-l"]/span')[1].text) #新闻时间

        news_list.append(html_key.replace('process', 'result')) #oss html
        
        #reg = r'http:\/\/[^\s,"]*\.jpg'
        reg = r'http://oss.zhixiaoren.com\/\/[^\s,"]*\.jpg'
        imgre = re.compile(reg)
        imglist = re.findall(imgre, str(page_html.xpath('//div[@id="news_content"]/node()')[1])[4:-3])
        
        #reg = r'http:\/\/[^\s,"]*\.png'
        reg = r'http://oss.zhixiaoren.com\/\/[^\s,"]*\.png'
        imgre = re.compile(reg)
        imglist = imglist+re.findall(imgre, str(page_html.xpath('//div[@id="news_content"]/node()')[1])[4:-3])
        
        
        for img in imglist:
          pic = urllib.request.urlopen(img).read()


          bucket.put_object(img.replace('http://oss.zhixiaoren.com','result/imgs/zhixiaoren'), pic)
        #news_list.append(';'.join(imglist).replace('http://oss.zhixiaoren.com','result/imgs/zhixiaoren')) #oss imgs
        news_list.append('imgs') #oss imgs
        news_list.append((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'))
        news_list.append(str(page_html.xpath('//div[@id="news_content"]/node()')[1])[4:-3])   #新闻内容
        news_list.append(etree.HTML(str(page_html.xpath('//div[@id="news_content"]/node()')[1])[4:-3]).xpath('string(.)').strip())   #新闻文本
        
        bucket.put_object(html_key.replace('process', 'result'), ('<html><head><meta charset="UTF-8"></head><body>'+str(page_html.xpath('//div[@id="news_content"]/node()')[1])[4:-3].replace(',','，')+'</body></html>').replace('http://oss.zhixiaoren.com','/result/imgs/zhixiaoren'))
        
        csv_file = html_key.replace('html', 'csv')
        bucket.put_object(csv_file, '\u0000'.join(news_list).replace('\n','').replace('\r',''))
        logger.info(
            (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S') + ' Step 4: finish parse ' + str(html_key))
    except Exception as e:
        print ("产生异常" + str(e))


if __name__ == "__main__":
    print(handler('1', '2'))