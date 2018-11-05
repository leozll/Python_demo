#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import urllib2
import re
from bs4 import BeautifulSoup
import gzip, StringIO
import json
import HTMLParser
import pymssql
import xlrd
import time  
from datetime import date, datetime, timedelta
import threading

#打开url
def openSoup(url,host):
	header = {'Host': host,
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
	'Accept-Encoding': 'gzip, deflate'}
	req = urllib2.Request(url, headers = header)
	page = urllib2.urlopen(req).read()

	if urllib2.urlopen(req).info().get('Content-Encoding') == 'gzip':
		html=gzip.GzipFile(fileobj=StringIO.StringIO(page), mode="r")
		soup = BeautifulSoup(html.read(), "html.parser",from_encoding="gb18030")
	else:
		soup = BeautifulSoup(page, "html.parser",from_encoding="gb18030")
		#soup = BeautifulSoup(page, "html.parser",from_encoding="gb18030")
	return soup
	
	
	
if __name__ == '__main__':
	f = open("a.txt", "w")

	host = 'hm.baidu.com'
	urls=('http://www.123haitao.com/group/page-1','http://www.123haitao.com/group/page-2','http://www.123haitao.com/group/page-3')
	for url in urls:
		soup = openSoup(url,host)
		all = soup.find_all('div',class_='mainList')
		for a in all:
			text=a.find('span',class_='listName').find_all('a')[1].contents[0]
			text=" ".join(text.split())
			href=a.find('span',class_='listName').find_all('a')[1]['href']
			soup = openSoup(href,host)
			detailTime = str(soup.find('span',class_='DetailTime')).find(u'小时')
			if detailTime>-1:
				f.write(text+'\n'+href)
				f.write('\n')
				f.write('\n')
	f.close()
	
	
	