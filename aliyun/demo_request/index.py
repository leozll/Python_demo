# -*- coding: utf-8 -*-
import logging
import sys
import os
sys.path.append(os.curdir+'/tmp/code/')
#from tmp.code.requests import *
import requests

def use_params_urllib2():
    # 构建请求参数
    params = urllib.parse.urlencode({'pageToken': '1', 'type': 'all', 'uid': '1826792401','apikey':'GcqZA9GII0aGoyx83eOVBP7QizZ23pMzhBaa9tAOmBnFbAYHQIM0Da2BIm4oh9'})
    print ('Request Params:')
    print (params)
    # 发送请求
    response = request.urlopen('?'.join([URL_GET, '%s']) % params)
    # 处理响应
    print ('>>>>>>Response Headers:')
    print (response.info())
    print ('Status Code:')
    print (response.getcode())
    print ('>>>>>>>Response Body:')
    json_obj = r.json()


def handler(event, context):
    logger = logging.getLogger()
    logger.info('hello world')
    use_params_urllib2()
    return 'hello world'


#handler(1, 2)


# 请求示例 url 默认请求参数已经做URL编码
url = "http://api01.idataapi.cn:8000/post/weibo?pageToken=1&type=all&uid=1826792401&apikey=GcqZA9GII0aGoyx83eOVBP7QizZ23pMzhBaa9tAOmBnFbAYHQIM0Da2BIm4oh9Eo"
headers = {
"Accept-Encoding": "gzip",
"Connection": "close"
}
if __name__ == "__main__":
    r = requests.get(url, headers=headers)
    json_obj = r.json()
    print(json_obj)