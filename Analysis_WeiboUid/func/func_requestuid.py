#  -*-  coding:  UTF-8  -*-
import requests
from retrying import retry


#wait_fixed 设置失败重试的间隔时间
#wait_random_min, wait_random_max 设置失败重试随机性间隔时间
#stop_max_delay 设置失败重试的最大时间, 单位毫秒，超出时间，则停止重试
@retry(wait_fixed=1000, stop_max_delay=10000)

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