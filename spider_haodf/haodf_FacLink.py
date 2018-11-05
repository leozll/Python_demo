#!/usr/bin/env python
# -*- coding:utf8 -*-
#import sys
#reload(sys)
#sys.setdefaultencoding( "utf-8" )
import urllib2
import re
from bs4 import BeautifulSoup
import gzip, StringIO
import json
import HTMLParser
import socket  
import time  
from datetime import date, datetime, timedelta
import xlrd

#打开url
def openSoup(url,host):
	header = {'Host': host,
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
	'Accept-Encoding': 'gzip, deflate'}
	timeout = 20    
	socket.setdefaulttimeout(timeout)
	sleep_download_time = 10  
	#time.sleep(sleep_download_time) 
	req = urllib2.Request(url, headers = header)
	open = urllib2.urlopen(req)
	page = open.read()
	if urllib2.urlopen(req).info().get('Content-Encoding') == 'gzip':
		html=gzip.GzipFile(fileobj=StringIO.StringIO(page), mode="r")
		soup = BeautifulSoup(html.read(), "html.parser",from_encoding="gb18030")
	else:
		soup = BeautifulSoup(page, "html.parser",from_encoding="gb18030")
		#soup = BeautifulSoup(page, "html.parser",from_encoding="gb18030")
	open.close()
	#except UnicodeDecodeError as e:  
	#	print(u'-----(error)UnicodeDecodeError url:',url)  
	#except urllib2.URLError as e:  
	#	print("-----(error)urlError url:",url)  
	#except socket.timeout as e:  
	#	print(u"-----(error)socket timout:",url) 
	#except Exception,e:  
	#	print url,Exception,":",e
	#	return -1
	return soup


#查询所有地区链接
def allDqs(url,dqs):
	host = 'www.haodf.com'
	soup = openSoup(url,host)
	#print str(soup.encode('gb18030'))
	#soup = openSoup(url,host).encode('gb18030')
	#soup = BeautifulSoup(soup,"html.parser")
	Alldq = soup.find_all('ul',attrs={'class':'find_dq'})
	for dq in Alldq[0]:
		if len(dq)>1:
			for d in dq.find_all('a'):
				dqs.append(d.get('href'))
				 
#查询所有医院链接
def allHospitals(url,hospitals):
	host = url[7:]
	soup = openSoup(url,host)
	Allhos = soup.find_all('table', attrs={'class':'jblb'})
	for hos in Allhos:
		if len(hos)>1:
			for dq in hos.find_all('a',href=re.compile('hospital')):
				hospitals.append(dq.get('href'))
				
#查询所有科室链接
def allFacultys(url,facultys):
	host = 'www.haodf.com'
	soup = openSoup(url,host)
	hospital = soup.find('a',href=re.compile(url)).string
	Allfac = soup.find_all('a',href=re.compile('http://www.haodf.com/faculty'))
	for fac in Allfac:
		#facultys.append(fac['href'])
		print hospital,fac['href'],fac.next_element,fac.next_element.next_element.next_element.next_element

if __name__ == '__main__':
	#查询所有地区链接
	dqs=[]
	allDqs('http://www.haodf.com',dqs)
	dqs=list(set(dqs))
	print "start",datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	#查询所有医院链接
	hospitals=[]
	for dq in dqs:
		if dq != "http://tianjin.haodf.com":
			allHospitals(dq,hospitals)
	hospitals=list(set(hospitals))
	print "dq",datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	#查询所有科室链接
	#hospitals=['http://www.haodf.com/hospital/DE4rO-XCoLUmxIYztx00uSYNw1.htm']
	#hospitals=['http://www.haodf.com/hospital/DE4rO-XCoLUXhINJ1t4xLBGs4w.htm']
	facultys=[]
	for hos in hospitals:
		try:
			allFacultys(hos,facultys)
		except Exception,e:  
			print datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"ERROR:",hos,"。MSG:",Exception,":",e,'\n'
			time.sleep(30) 
			continue
	facultys=list(set(facultys))
	print "fac",datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	
	

	



	
	