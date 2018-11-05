import os
import json
import time
import urllib2
import threading
from lxml import etree
from datetime import datetime
import spider_fuc as rt
simple_cookie = '__jdc=122270672; __jda=122270672.1360558993.1482981002448.1484013745.1484028631.8; __jdv=122270672|jdzt_refer_null|t_108549027_1|jzt-zhitou|t5ngywhxaual4sls7c5q|1483497615808; __jdu=1360558993; ipLoc-djd=1-72-4137-0; areaId=1; listck=520709493c793a749249447ae85c3fe6'
class SimpleCookieHandler(urllib2.BaseHandler):
    def http_request(self, req):
        if not req.has_header('Cookie'):
            req.add_unredirected_header('Cookie', simple_cookie)
        else:
            cookie = req.get_header('Cookie')
            req.add_unredirected_header('Cookie', simple_cookie + '; ' + cookie)
        return req

def http_request2():
    if not urllib2.BaseHandler.has_header('Cookie'):
        urllib2.BaseHandler.add_unredirected_header('Cookie', simple_cookie)
    else:
        cookie = urllib2.BaseHandler.get_header('Cookie')
        urllib2.BaseHandler.add_unredirected_header('Cookie', simple_cookie + '; ' + cookie)
    return urllib2.BaseHandler

print http_request2()

url="http://list.jd.com/list.html?cat=9987,653,655&page=50&trans=1&JL=6_0_0#J_main"


opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(), SimpleCookieHandler())
req = urllib2.Request(url)
htmlcontent = opener.open(req, timeout=20).read()

html = etree.HTML(htmlcontent)
producturls = html.xpath("//div[@id='plist']/ul/li//div[@class='p-img']/a/@href")
for pl in producturls:
    print pl

