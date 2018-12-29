# -*- coding: utf-8 -*-
import logging
import datetime
import os
import oss2
import requests
import logging
from lxml import etree
import json
from multiprocessing import Pool

def handler(event, context):
    max_pages_num = 200
    pool_num= 10

    url_prefix = "http://www.pinguan.com/index?p="
    #homepage_url = url_prefix + "1.html"
    oss_url_path = "process/pinguan_url/"

    region = "cn-hangzhou-internal"
    bucketname = "leo-hangzhou"
    endpoint = 'oss-{0}.aliyuncs.com'.format(region)
    creds = context.credentials
    auth = oss2.StsAuth(creds.accessKeyId, creds.accessKeySecret, creds.securityToken)
    bucket = oss2.Bucket(auth, endpoint, bucketname)
    logger = logging.getLogger()
    logger.info(
        (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + ' Step 1: Start to request www.pinguan.com')
    try:
        #r = requests.get(homepage_url, timeout=10)  # 请求超时时间为10秒
        #r.raise_for_status()  # 如果状态不是200，则引发异常
        #r.encoding = r.apparent_encoding  # 配置编码
        #html = etree.HTML(r.text)
        # get pages number
        #pages_nums = html.xpath('//a[@class="pagesNum"]/text()')
        #pages_num = int(pages_nums[0].split('/')[1].strip())
        pages_num = 200
        pages_num = min(pages_num,max_pages_num)
        logger.info(
            (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S') + ' Step 2: Start to loop ' + str(pages_num) + ' pages')
        poo = Pool(pool_num)
        for p in range(0, pages_num):
            page_url = url_prefix + str(p + 1)

            poo.apply_async(request_page ,(oss_url_path,bucket,page_url,p,pages_num))
        poo.close()
        poo.join()
        print('All subprocesses done.')
        return p
    except Exception as e:
        logger.info(
            (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S') + '产生异常!!!' + str(e))
        return "产生异常" + str(e)


def request_page(oss_url_path,bucket,page_url,p,pages_num):
    try:
        print((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S') + ' Step 3.1 : (pid %s) page %d/%s...' % (os.getpid(),p + 1,pages_num + 1))
        page_r = requests.get(page_url, timeout=10)  # 请求超时时间为10秒
        page_r.raise_for_status()  # 如果状态不是200，则引发异常
        page_r.encoding = page_r.apparent_encoding  # 配置编码
        #page_html = etree.HTML(page_r.text)
        ## get news list
        news_list = json.loads(page_r.text)['data']
        for d in news_list:
            content_id = d['article_id']
            url_file = oss_url_path + 'content/' + str(content_id)
            content_url = 'http://www.pinguan.com/article/content/' + str(content_id)
            bucket.put_object(url_file, '{0}'.format(content_url))


        print((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
            '%Y-%m-%d %H:%M:%S') + ' Step 3.1 : (pid %s) page %d/%s is finished.' % (
                  os.getpid(), p + 1, pages_num + 1))
    except Exception as e:
        print((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S') + ' Step 3.1 : (pid %s) page %d/%s 产生异常!!!'% (
                os.getpid(), p + 1, pages_num + 1)  + str(e))

if __name__ == "__main__":
    handler('1', '2')