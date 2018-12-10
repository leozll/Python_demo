#-*-coding:utf8-*-

import string
import sys
import os
import urllib
from bs4 import BeautifulSoup
import requests
import shutil
import time
from lxml import etree
import csv
import random
import datetime
#reload(sys)
#sys.setdefaultencoding('utf-8')
#if(len(sys.argv)>=2):
#        user_id = (int)(sys.argv[1])
#else:
#        user_id = (int)(raw_input(u"please_input_id: "))
headers = {"Cookie": "SINAGLOBAL=9336210156603.25.1536404794441; UOR=,,login.sina.com.cn; _s_tentry=login.sina.com.cn; Apache=5828895455932.55.1544019181873; ULV=1544019181932:51:3:2:5828895455932.55.1544019181873:1544011518789; login_sid_t=6b76ad6d88fdb757291ed33da16c236a; cross_origin_proto=SSL; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWp-N25.LI6Pvm6x9N549X05JpX5K2hUgL.FoqReK-c1K-p1K52dJLoI7YLxK.L1h-L1h9RdLvzx2nt; ALF=1575555202; SSOLoginState=1544019203; SCF=Ag9BwHY1vJCyYgSSCCi0oxmq3VPC68qoF4Z3UzC63-SfdQG6vT0NEdmd5eYoClnHFHYYI4hRxC-3gi2nzIoNg0E.; SUB=_2A25xA61UDeRhGeBG6lcX-SvNwjyIHXVSeJmcrDV8PUNbmtBeLWXEkW9NRjezh5PtW4DEQ3xuCmlBxaW1E4pGhuSE; SUHB=0oUosgTj4dagi0; un=17825380369; wvr=6"}

for pagenum in range(0,100):
    tmp_profile_list = 'hufu'

    #meizhuang
    #url = 'https://s.weibo.com/user?q=%E7%BE%8E%E5%A6%86&Refer=weibo_user&page='+str(pagenum)

    #shishang
    url = 'https://s.weibo.com/user?q=%E6%97%B6%E5%B0%9A&Refer=weibo_user&page=' + str(pagenum)

    # hufu
    url = 'https://s.weibo.com/user?q=%E6%8A%A4%E8%82%A4&Refer=weibo_user&page=' + str(pagenum)

    r = requests.get(url, headers = headers,verify=False)
    print (u'cookie读入成功')

    #r.encoding = r.apparent_encoding  # 配置编码
    html = etree.HTML(r.text)
    urls = html.xpath('//a[@class="name"]/@href')
    l = len(urls)
    infos = html.xpath('//div[@class="info"]')

    for n in range(0,l):
        info = infos[n]

        url = urls[n]
        uid = info.xpath('p/span/a/@href')[0].split('/')[3]
        name = info.xpath('div/a[@class="name"]')[0].xpath('string(.)').strip()
        if len(info.xpath('div/a[@target="_blank"]/@title'))==0:
            title = ''
        else:
            title = info.xpath('div/a[@target="_blank"]/@title')[0]
        addr = info.xpath('p')[0].xpath('string(.)').replace('个人主页','').strip()
        if len(info.xpath('p')[1].xpath('span')) == 0:
            com = info.xpath('p')[1].xpath('string(.)').strip()
        else :
            com = ''
        follow = info.xpath('p/span/a/text()')[0]
        fans = info.xpath('p/span/a/text()')[1]
        p = info.xpath('p/span/a/text()')[2]
        comment = ''
        label = ''
        for c in info.xpath('p/text()'):
            if c.startswith(u"简介："):
                comment = c
        for c in info.xpath('p'):
            if c.text == u"标签：":
                #label = c.xpath('string(.)').strip()
                label = " ".join(c.xpath('a/text()'))

        result = "|".join([uid,url,name,title,addr,com,follow,fans,p,comment,label])

        with open(tmp_profile_list, 'a', newline='',encoding='utf-8') as f:
            f.write(result+'\n')
    print (str(pagenum)+' is ok...'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    time.sleep(random.randint(5,10))