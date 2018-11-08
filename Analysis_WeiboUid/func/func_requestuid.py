#  -*-  coding:  UTF-8  -*-
import requests
import json

def get_uid(p_url):
    url="http://api01.idataapi.cn:8000/profile/weibo"
    params = {
        'pageToken': '1',
        'type': '1',
        #'url': 'https://weibo.com/chcedo',
        'url': p_url,
        'apikey': 'GcqZA9GII0aGoyx83eOVBP7QizZ23pMzhBaa9tAOmBnFbAYHQIM0Da2BIm4oh9Eo'
    }
    headers = {
        'Accept-Encoding': 'gzip',
        'Connection': 'close'
    }

    return requests.get(url, params=params, headers=headers).json()['data'][0]