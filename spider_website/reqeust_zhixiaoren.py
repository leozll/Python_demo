# -*- coding: utf-8 -*-
import logging
import datetime
import time
import oss2
import requests
import logging
from lxml import etree


def handler(event, context):
    max_pages_num = 100

    url_prefix = "http://news.zhixiaoren.com/list/1_"
    homepage_url = url_prefix + "1.html"
    oss_url_path = "process/zhixiaoren_url/"

    region = "cn-hangzhou-internal"
    bucketname = "leo-hangzhou"
    endpoint = 'oss-{0}.aliyuncs.com'.format(region)
    creds = context.credentials
    auth = oss2.StsAuth(creds.accessKeyId, creds.accessKeySecret, creds.securityToken)
    bucket = oss2.Bucket(auth, endpoint, bucketname)
    logger = logging.getLogger()
    logger.info(
        (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + ' Step 1: Start to request news.zhixiaoren.com')
    try:
        r = requests.get(homepage_url, timeout=10)  # 请求超时时间为10秒
        r.raise_for_status()  # 如果状态不是200，则引发异常
        r.encoding = r.apparent_encoding  # 配置编码
        html = etree.HTML(r.text)
        # get pages number
        pages_nums = html.xpath('//a[@class="pagesNum"]/text()')
        pages_num = int(pages_nums[0].split('/')[1].strip())
        pages_num = min(pages_num,max_pages_num)
        logger.info(
            (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S') + ' Step 2: Start to loop ' + str(pages_num) + ' pages')
        for p in range(0, pages_num):
            print ('starting page ' + str(p+1))
            page_url = url_prefix + str(p + 1) + ".html"
            page_r = requests.get(page_url, timeout=10)  # 请求超时时间为10秒
            page_r.raise_for_status()  # 如果状态不是200，则引发异常
            page_r.encoding = page_r.apparent_encoding  # 配置编码
            page_html = etree.HTML(page_r.text)
            # get news list
            news_list = page_html.xpath('//ul[@class="b-TopNew-ul fix"]/li/div/a/@href')
            for news_url in news_list:
                url_file = oss_url_path + news_url.replace('http://news.zhixiaoren.com/','')
                bucket.put_object(url_file, '{0}'.format(news_url))
            logger.info(
                (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                    '%Y-%m-%d %H:%M:%S') + ' Step 3: (' + str(p+1) + '/' + str(pages_num+1) + ') Page' + str(p+1) + ' is finished...')
        return p
    except Exception as e:
        logger.info(
            (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S') + '产生异常!!!' + str(e))
        return "产生异常" + str(e)


if __name__ == "__main__":
    print(handler('1', '2'))