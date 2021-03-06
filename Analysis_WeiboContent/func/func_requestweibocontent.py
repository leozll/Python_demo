#  -*-  coding:  UTF-8  -*-
import requests
import datetime
from retrying import retry

#wait_fixed 设置失败重试的间隔时间
#wait_random_min, wait_random_max 设置失败重试随机性间隔时间
#stop_max_delay 设置失败重试的最大时间, 单位毫秒，超出时间，则停止重试
#stop_max_attempt_number：用来设定最大的尝试次数，超过该次数就停止重试
#def retry_if_result_none(result):
#    #return "error" in result
#    return result["retcode"]!="000000"
#@retry(retry_on_result=retry_if_result_none, wait_fixed=1500, stop_max_attempt_number=2)
#
#def weibo_content(uid,d):
#
#    print (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'"'+ uid + '"解析中...')
#    url="http://api01.idataapi.cn:8000/post/weibo"
#    params = {
#        #'pageToken': '1',
#        'type': 'all',
#        #'kw': p_kw,
#        'uid': uid,
#        'date': d,
#        'apikey': 'GcqZA9GII0aGoyx83eOVBP7QizZ23pMzhBaa9tAOmBnFbAYHQIM0Da2BIm4oh9Eo'
#    }
#    headers = {
#        'Accept-Encoding': 'gzip',
#        'Connection': 'close'
#    }
#    j=requests.get(url, params=params, headers=headers).json()
#    return j

def retry_if_json_error(exception):
    return isinstance(exception, Exception)
@retry(retry_on_exception=retry_if_json_error, wait_fixed=1500, stop_max_attempt_number=2)

def weibo_content(uid,d):
    print (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'"'+ uid + '"解析中...')
    url="http://api01.idataapi.cn:8000/post/weibo"
    params = {
        #'pageToken': '1',
        'type': 'all',
        #'kw': p_kw,
        'uid': uid,
        'date': d,
        'apikey': 'GcqZA9GII0aGoyx83eOVBP7QizZ23pMzhBaa9tAOmBnFbAYHQIM0Da2BIm4oh9Eo'
    }
    headers = {
        'Accept-Encoding': 'gzip',
        'Connection': 'close'
    }
    j=requests.get(url, params=params, headers=headers).json()
    if j["retcode"]!="000000":
        raise Exception(str(j["retcode"])+" : "+j["message"])
    else:
        return j
