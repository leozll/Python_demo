#coding:utf-8
import xlrd
import matplotlib.pyplot as plt
import xlwt

import urllib2
import re
from bs4 import BeautifulSoup
import gzip, StringIO
import socket

import sys   
import json
import time 
import pymssql
import os
sys.setrecursionlimit(1000000)



	
	
#插入到目标表
def insertMobileMomentSpider(data):
	conn=pymssql.connect(host=".",user="",password="",charset="utf8")
	cur=conn.cursor()
	cur.execute(
		"""insert INTO wechat.dbo.MobileMomentAccount
		(
		snsId,authorId,MomentTime,
		Longitude,Latitude,LName,LAddress,LCity,PictureCount,IsMMVideo,Url,UrlDomain,Account,hasContent
		)
		 VALUES 
		(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""" , data)
	conn.commit()
	conn.close()
	
#打开url
def openSoup(url):
	timeout = 20    
	socket.setdefaulttimeout(timeout)
	req = urllib2.Request(url)
	open = urllib2.urlopen(req)
	page = open.read()
	if urllib2.urlopen(req).info().get('Content-Encoding') == 'gzip':
		html=gzip.GzipFile(fileobj=StringIO.StringIO(page), mode="r")
		soup = BeautifulSoup(html.read(), "html.parser",from_encoding="gb18030")
	else:
		soup = BeautifulSoup(page, "html.parser",from_encoding="gb18030")
	open.close()
	return soup

#解析rawXML
def spider(result):
	#找出mediaList字段
	mediaList=result[3]
	#找出rawXML字段
	rawXML=result[4]
	#找出Content字段
	Content=result[5]
	
	#找出rawXML字段中各个信息的位置
	longitudeindex     = rawXML.find("longitude")
	latitudeindex      = rawXML.find("latitude")
	poiScaleindex      = rawXML.find("poiScale")
	poiNameindex       = rawXML.find("poiName")
	poiClassifyIdindex = rawXML.find("poiClassifyId")
	poiAddressindex    = rawXML.find("poiAddress")
	cityindex          = rawXML.find("city")
	endindex           = rawXML.find("</location>")
	
	#取出rawXML字段中的各个信息
	Longitude          = rawXML[longitudeindex+11:latitudeindex].replace('\\','').replace('"','').strip().replace('&#x20;',' ')
	Latitude           = rawXML[latitudeindex+10:poiScaleindex].replace('\\','').replace('"','').strip().replace('&#x20;',' ')
	LName              = rawXML[poiNameindex+9:poiClassifyIdindex].replace('\\','').replace('"','').strip().replace('&#x20;',' ')
	LAddress           = rawXML[poiAddressindex+12:cityindex].replace('\\','').replace('"','').strip().replace('&#x20;',' ')
	LCity              = rawXML[cityindex+6:endindex].replace('\\','').replace('"','').replace('>','').strip().replace('&#x20;',' ')
	PictureCount       = mediaList.count("http://mmsns.qpic.cn/mmsns") if rawXML.count("http://mmsns.qpic.cn/mmsns")>0 else '0'
	IsMMVideo          = '1' if rawXML.count("<title><![CDATA[微信小视频]]></title>")>0 else '0'
	hasContent         = '1' if len(Content)>2 else '0'

	#爬虫找出转发链接的内容
	start=rawXML.find("<contentUrl><![CDATA[")
	try:
		if IsMMVideo=='0' and start>-1:
			end=rawXML[start+21:].find("]]></contentUrl>")
			Url=rawXML[start+21:start+21+end]
			#print rownum,"------",Url
			Url = Url if Url[0:4]=="http" else "http://"+Url
			Url = "http:"+Url if Url[0:2]=="//" else Url
			soup=openSoup(Url)
			Account = soup.find('a',id='post-user').string if soup.find('a',id='post-user') else u""
			UrlDomain=Url.split('/')[2]
		else:
			Url=''
			UrlDomain=''
			Account=''
	except Exception,e:  
		Url=''
		UrlDomain=''
		Account=''
	data=result[:3]+(Longitude,Latitude,LName,LAddress,LCity,PictureCount,IsMMVideo,Url,UrlDomain,Account,hasContent)
	insertMobileMomentSpider(data)
	#print data


if __name__ == '__main__':
	try:
		#提取数据源
		conn=pymssql.connect(host=".",user="",password="",charset="utf8")
		cur=conn.cursor()
		cur.execute(
			"""
			select distinct
			 snsId,authorId,MomentTime,mediaList,rawXML,Content
			from wechat.dbo.MobileMomentSpider a
			where exporttime<'2016-10-10 04:45:35.010' and UrlDomain='mp.weixin.qq.com'
			and not exists (select 1 from wechat.dbo.MobileMomentAccount b where a.snsid=b.snsid)
			""")
		resList = cur.fetchall()  
		conn.commit()
		conn.close()
		#循环爬取源数据，取出
		loop=1
		for r in resList:
			try:
				print loop
				spider(r)
				loop=loop+1
			except Exception,e:  
				print Exception,":",e
	except Exception,e:  
		print Exception,":",e
