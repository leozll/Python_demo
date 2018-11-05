#encoding=utf-8
#pip install lxml

import os
import json
import time
import urllib2
import threading
from lxml import etree
from datetime import datetime
import spider_fuc as rt

config_file="./config.json"
mainurl = "http://list.jd.com/list.html?cat=9987,653,655&page=1&trans=1&JL=6_0_0#J_main"
mainhtml = "./downloads/mainhtml/main.html"
urldir = "./downloads/producturl/"
simple_cookie = '__jdc=122270672; __jda=122270672.1360558993.1482981002448.1484013745.1484028631.8; __jdv=122270672|jdzt_refer_null|t_108549027_1|jzt-zhitou|t5ngywhxaual4sls7c5q|1483497615808; __jdu=1360558993; ipLoc-djd=1-72-4137-0; areaId=1; listck=520709493c793a749249447ae85c3fe6'

# 手动设置cookie信息
class SimpleCookieHandler(urllib2.BaseHandler):
    def http_request(self, req):
        if not req.has_header('Cookie'):
            req.add_unredirected_header('Cookie', simple_cookie)
        else:
            cookie = req.get_header('Cookie')
            req.add_unredirected_header('Cookie', simple_cookie + '; ' + cookie)
        return req

def readhtml(url):
    # 读取url内容
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(), SimpleCookieHandler())
    req = urllib2.Request(url)
    return opener.open(req, timeout=20).read()

def downloadhtml(url,mainhtml):
    # 读取url内容
    htmlcontent = readhtml(url)
    #写入url内容到本地txt文件
    f = open(mainhtml, 'w')
    f.write(htmlcontent)
    f.close()

def getpagenum(mainhtml):
    #修正 html 代码
    html = etree.HTML(open(mainhtml, 'r').read())
    #htmlcontent = etree.tostring(html)
    #获取商品总页数
    pagenum = html.xpath("//span[@class='p-skip']/em/b")[0].text
    return pagenum

def getproducturl(urls):
    #获取自己的进程号
    threadid = threading.currentThread().ident
    #目标文件
    print datetime.now(), "Thread", threadid, ":downloading product urls......"
    filename = "./downloads/producturl/"+str(threading.currentThread().name)+"-"+str(threadid)+".txt"
    f = open(filename, 'a')
    urlnum=0
    productnum=0
    for url in urls:
        urlnum  = urlnum+1
        # 读取url内容
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(), SimpleCookieHandler())
        req = urllib2.Request(url)
        html = etree.HTML(opener.open(req, timeout=20).read())
        #html = etree.HTML(urllib2.urlopen(url).read())
        # 获取商品url
        producturls = html.xpath("//div[@id='plist']/ul/li//div[@class='p-img']/a/@href")
        for j in range(0, len(producturls)):
            productnum = productnum+1
            #写入文件
            f.write("http:"+producturls[j]+"\n")
    f.close()
    print datetime.now(), "Thread", threadid, ":downloaded",urlnum,"product pages,",productnum,"product urls......"
def test(urllist,a):
    print urllist

if __name__ == '__main__':
    print datetime.now(),"JD spider is starting......"
    #读取jason配置文件
    with open(config_file) as json_file:
        jasonData = json.load(json_file)
    #下载main页面
    print "======================================================="
    print datetime.now(),"step 1: downloading the main page......"
    downloadhtml(mainurl,mainhtml)
    #从main页面中解析商品页数
    print datetime.now(), "parsing main page......"
    pagenum = int(getpagenum(mainhtml))
    print datetime.now(), "totally",pagenum,"product pages......"
    #清空商品url文件夹
    print datetime.now(),"empty old product urls......"
    for f in os.listdir(urldir):
        os.remove(os.path.join(urldir, f))
    #读取线程个数
    threadnum=jasonData['threads']['count']
    print "======================================================="
    print datetime.now(), "step 2: distributing the product pages to",threadnum,"threads......"
    #创建product pages列表
    urllist=[]
    for i in xrange(1,pagenum+1):
        urllist.append("http://list.jd.com/list.html?cat=9987,653,655&page=" + str(i) + "&trans=1&JL=6_0_0#J_main")
    #启动线程
    rt.runthreads(threadnum, getproducturl, urllist)
    print "======================================================="
    print datetime.now(), "step 3: all product url is downloaded......"