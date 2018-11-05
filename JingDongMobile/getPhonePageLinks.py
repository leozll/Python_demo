# -*- coding: utf-8 -*-
# -*- author: Charlie -*-

import lxml.html
import MySQLdb
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 存放文件的位置
filePath = "D:\MobileInfo\JingDong\PhoneListPage"

# 获取目录下所有文件的文件名list
def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir.decode('gbk'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码
            # if s == "xxx":
            # continue
            newDir = os.path.join(dir, s)
            GetFileList(newDir, fileList)
    return fileList

# 根据文件名，解析相应html
def htmlETL(path):
    try:
        conndb = MySQLdb.connect("localhost", "root", "12345678", "jingdong", charset="utf8")
        cursor = conndb.cursor()

        f = open(path, 'r')
        htmlInfo = f.read()
        doc = lxml.html.document_fromstring(htmlInfo)

        linkList = doc.xpath("//div[@id='plist']/ul/li//div[@class='p-img']/a/@href")

        # 循环，将link存放到数据库汇总
        for j in range(0, len(linkList)):
            result_value = (linkList[j])
            cursor.execute("INSERT INTO jingdong.phonepagelink(pageLink) VALUES (%s)", result_value)
            conndb.commit()

        print path + "---- done"
    except Exception, ex:
        print path + str(ex) +'-----------Except'


#-------------- Main Function -------------#
list = GetFileList(filePath, [])
for i in range(0, len(list)):
    htmlETL(list[i])
