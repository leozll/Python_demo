# -*- coding: utf-8 -*-
# -*- author: Charlie -*-

import urllib2
import time
import MySQLdb

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

ISOTIMEFORMAT = '%Y-%m-%d %X'

# 设置文件存放目录
filePath = 'D:\MobileInfo\JingDong\PhoneDetailPage'


# 获取所有link
def getPhoneLinks():
    try:
        conndb = MySQLdb.connect("localhost", "root", "12345678", "jingdong", charset="utf8")
        cursor = conndb.cursor()

        cursor.execute("SELECT pageLink FROM jingdong.phonepagelink")

        data = cursor.fetchall()
        linkList = []
        for i in range(0, len(data)):
            linkList.append(data[i][0])

        return linkList
    except Exception, ex:
        print str(ex)


# 获取手机详情页
def getPhonePage(link):
    try:
        para = link.split('/', 3)[3].split('.', 1)[0]

        request = urllib2.Request('http:'+ link)
        response = urllib2.urlopen(request)
        html = response.read().decode('gb18030').encode('utf8')

        # 将html信息写入txt文件
        thisFilePath = filePath + "\\" + para + ".txt"
        f = open(thisFilePath, 'w')

        f.write(html)
        f.close()

    except Exception, ex:
        print (link + " ----------- Exception!!!!---------" + time.strftime(ISOTIMEFORMAT, time.localtime()))

#------------- Main Function ---------------#
linkList = getPhoneLinks()

for i in range(0, len(linkList)):
    getPhonePage(linkList[i])
    print (str(i) + "----- Done! " + time.strftime(ISOTIMEFORMAT, time.localtime()))
    time.sleep(3)
