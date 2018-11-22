# -*- coding: utf-8 -*-
import logging
import datetime
import time
import oss2
import requests
from lxml import etree


def handler(event, context):
    url_prefix = "http://news.zhixiaoren.com/list/1_"
    homepage_url = url_prefix + "1.html"
    is_initialization = 1
    oss_html_path = "process/zhixiaoren_html/"

    region = "cn-hangzhou-internal"
    bucketname = "leo-hangzhou"
    endpoint = 'oss-{0}.aliyuncs.com'.format(region)
    creds = context.credentials
    auth = oss2.StsAuth(creds.accessKeyId, creds.accessKeySecret, creds.securityToken)
    bucket = oss2.Bucket(auth, endpoint, bucketname)

    try:
        r = requests.get(homepage_url, timeout=10)  # 请求超时时间为10秒
        r.raise_for_status()  # 如果状态不是200，则引发异常
        r.encoding = r.apparent_encoding  # 配置编码
        html = etree.HTML(r.text)
        # get pages number
        pages_nums = html.xpath('//a[@class="pagesNum"]/text()')
        pages_num = int(pages_nums[0].split('/')[1].strip())
        print(pages_num)
        for p in range(0, pages_num):
            page_url = url_prefix + str(p + 1) + ".html"
            page_r = requests.get(page_url, timeout=10)  # 请求超时时间为10秒
            page_r.raise_for_status()  # 如果状态不是200，则引发异常
            page_r.encoding = page_r.apparent_encoding  # 配置编码
            page_html = etree.HTML(page_r.text)
            print(page_html)
            # get news list
            news_list = page_html.xpath('//ul[@class="b-TopNew-ul fix"]/li/div/a/@href')
            for news_url in news_list:
                news_r = requests.get(news_url, timeout=10)  # 请求超时时间为10秒
                news_r.raise_for_status()  # 如果状态不是200，则引发异常
                news_r.encoding = news_r.apparent_encoding  # 配置编码
                html_file = oss_html_path + news_url
                bucket.put_object(html_file, '{0}'.format(news_r.text))
        return p
    except Exception as e:
        return "产生异常" + str(e)


if __name__ == "__main__":
    print(handler('1', '2'))