# -*- coding: utf-8 -*-
# -*- author: Charlie -*-

import urllib2
import time

# 设置总页数
totalPageNum = 92

# 设置文件存放目录
filePath = 'D:\MobileInfo\JingDong\PhoneListPage'

# 获取当前页码，手机list信息
def getPageInfo(pageNum):
    url = "http://list.jd.com/list.html?cat=9987,653,655&page=" + str(pageNum) + "&trans=1&JL=6_0_0#J_main"
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    html =  response.read()

    # 将html信息写入txt文件
    thisFilePath = filePath + "\\" + str(pageNum) + ".txt"
    f = open(thisFilePath, 'w')

    f.write(html)
    f.close()

for i in range(0, totalPageNum):
    getPageInfo(i+1)
    time.sleep(5)