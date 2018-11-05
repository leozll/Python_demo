# -*- coding: utf-8 -*-
# -*- author: Charlie -*-

import urllib2
import os
import sys
import time
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf-8')

ISOTIMEFORMAT = '%Y-%m-%d %X'

# 存放文件的位置
filePath = "D:\MobileInfo\JingDong\PhoneDetailPage"

# u'D:\\MobileInfo\\JingDong\\PhoneDetailPage\\10000055606.txt'

# 获取目录下所有文件的文件名list
def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir.decode('gbk').split('\\')[4].split('.', 1)[0])
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码
            # if s == "xxx":
            # continue
            newDir = os.path.join(dir, s)
            GetFileList(newDir, fileList)
    return fileList


# 获取当前手机评论总页数
def getMaxPage(para):
    try:
        url = 'http://sclub.jd.com/comment/productPageComments.action?productId=' + para + '&score=0&sortType=3&page=1&pageSize=10&callback=fetchJSON_comment98vv45667'
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
        request.add_header('Host', 'sclub.jd.com')
        request.add_header('Accept', '*/*')
        request.add_header('Accept-Encoding', 'identity')
        request.add_header('Connection', 'close')
        response = urllib2.urlopen(request, timeout=20)
        data = str(response.read().decode('gb18030').encode('utf8'))

        a = str(data).split('(', 1)[1]
        if len(a) > 1:
            a = a[0: len(a)-2]

        null = "null"
        true = "true"
        false = "false"

        jsonData = eval(a)

        # 总页数
        maxPage = jsonData["maxPage"]

        return maxPage

    except Exception, ex:
        print str(ex)
        # 保存异常信息
        try:
            conndb = MySQLdb.connect("localhost", "root", "12345678", "jingdong", charset="utf8")
            cursor = conndb.cursor()
            result_data = (para, str(ex), time.strftime(ISOTIMEFORMAT, time.localtime()))
            cursor.execute("INSERT INTO jingdong.phoneexception(para, exceptInfo, exceptTime)"
                           " VALUES (%s, %s, %s)", result_data)
            conndb.commit()
        except Exception, ex:
            print str(ex)

        return -1

# 获取当前手机的所有评论信息
def getComments(para, maxPage):
    try:
        conndb = MySQLdb.connect("localhost", "root", "12345678", "jingdong", charset="utf8")
        cursor = conndb.cursor()

        # 从第一页获取到最后一页
        for j in range(0, maxPage):
            url = 'http://sclub.jd.com/comment/productPageComments.action?productId=' + para + '&score=0&sortType=3&page=' + str(j+1) + '&pageSize=10&callback=fetchJSON_comment98vv45667'
            request = urllib2.Request(url)
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
            request.add_header('Host', 'sclub.jd.com')
            request.add_header('Accept', '*/*')
            request.add_header('Accept-Encoding', 'identity')
            request.add_header('Connection', 'close')
            response = urllib2.urlopen(request, timeout=20)
            data = str(response.read().decode('gb18030').encode('utf8'))

            a = str(data).split('(', 1)[1]
            if len(a) > 1:
                a = a[0: len(a) - 2]

            null = "null"
            true = "true"
            false = "false"

            jsonData = eval(a)
            for k in range(0, len(jsonData["comments"])):
                content = jsonData["comments"][k]["content"].decode("utf-8")
                creationTime = jsonData["comments"][k]["creationTime"]
                days = jsonData["comments"][k]["days"]
                nickname = jsonData["comments"][k]["nickname"].decode("utf-8")
                productColor = jsonData["comments"][k]["productColor"].decode("utf-8")
                productSize = jsonData["comments"][k]["productSize"].decode("utf-8")
                referenceName = jsonData["comments"][k]["referenceName"].decode("utf-8")
                score = jsonData["comments"][k]["score"]
                userLevelId = jsonData["comments"][k]["userLevelId"]
                userLevelName = jsonData["comments"][k]["userLevelName"].decode("utf-8")

                result_data = (para, referenceName, str(j+1), creationTime, nickname, days, productColor, productSize, score,
                               content, userLevelId, userLevelName)

                cursor.execute("INSERT INTO jingdong.phonecomments(para, referenceName, pageNum, creationTime, nickName, "
                               "afterDays, productionColor, productionSize, score, content, userLevelId, userLevelName)"
                               " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", result_data)
                conndb.commit()

            print ("page" + str(j+1) + "/" + str(maxPage) + " ---- Done!" + time.strftime(ISOTIMEFORMAT, time.localtime()))

    except Exception, ex:
        print str(ex)
        # 保存异常信息
        try:
            conndb = MySQLdb.connect("localhost", "root", "12345678", "jingdong", charset="utf8")
            cursor = conndb.cursor()
            result_data = (para, str(ex), time.strftime(ISOTIMEFORMAT, time.localtime()))
            cursor.execute("INSERT INTO jingdong.phoneexception(para, exceptInfo, exceptTime)"
                           " VALUES (%s, %s, %s)", result_data)
            conndb.commit()
        except Exception, ex:
            print str(ex)


# 保存最大页码
def saveMaxPage(para, maxPage):
    try:
        conndb = MySQLdb.connect("localhost", "root", "12345678", "jingdong", charset="utf8")
        cursor = conndb.cursor()

        result_value = (para, maxPage)
        cursor.execute("INSERT INTO jingdong.commentsmaxpage(para, maxPage)"
                       " VALUES (%s, %s)", result_value)
        conndb.commit()
    except Exception, ex:
        print str(ex)

# --------------- Main Function ------------------#
paraList = GetFileList(filePath, [])

# for i in range(0, len(paraList)):
for i in range(301, 500):
    maxPage = getMaxPage(paraList[i])
    # saveMaxPage(paraList[i], maxPage)
    # print (str(i+1) + "/" + str(len(paraList)) + " ----Done! " + time.strftime(ISOTIMEFORMAT, time.localtime()))

    getComments(paraList[i], maxPage)
    print ("phone id." + str(i+1) +", para: "+ paraList[i] + "---- Done! " + time.strftime(ISOTIMEFORMAT, time.localtime()))

