#  -*-  coding:  UTF-8  -*-
#from func.code import requests
import requests
def get_uid():

    # 请求示例 url 默认请求参数已经做URL编码
    url = "http://api01.idataapi.cn:8000/profile/weibo?pageToken=1&type=1&url=https%3A%2F%2Fweibo.com%2Fchcedo&apikey=GcqZA9GII0aGoyx83eOVBP7QizZ23pMzhBaa9tAOmBnFbAYHQIM0Da2BIm4oh9Eo"
    headers = {
    "Accept-Encoding": "gzip",
    "Connection": "close"
    }

    r = requests.get(url, headers=headers)
    json_obj = r.json()
    return json_obj