﻿#coding:utf-8
import xlrd
import matplotlib.pyplot as plt
import xlwt

import urllib2
import re
from bs4 import BeautifulSoup
import gzip, StringIO

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
		"""insert INTO wechat.dbo.MobileMomentSpidercs
		(
		ExportTime,mobile,snsId,timestamp,authorId,comments,content,authorName,isCurrentUser,likes,mediaList,rawXML,MomentTime,
		Longitude,Latitude,LName,LAddress,LCity,PictureCount,IsMMVideo,Url,UrlDomain,UrlContent
		)
		 VALUES 
		(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""" , data)
	conn.commit()
	conn.close()
	
def insertException(data):
	conn=pymssql.connect(host=".",user="",password="",charset="utf8")
	cur=conn.cursor()
	cur.execute(
		"""insert INTO wechat.dbo.Exceptioncs
		(snsId)
		 VALUES 
		(%s);""" , data)
	conn.commit()
	conn.close()
	
#打开url
def openSoup(url):
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
	mediaList=result[10]
	#找出rawXML字段
	rawXML=result[11]
	
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
			title = soup.find('title').string if soup.find('title') else u"无题"
			[script.extract() for script in soup.findAll('script')]
			[style.extract() for style in soup.findAll('style')]
			soup.prettify()
			reg1 = re.compile("<[^>]*>")
			content = reg1.sub('',soup.prettify())
			content="".join(content.split())
			UrlContent=content[0:200000]
			UrlDomain=Url.split('/')[2]
		else:
			Url=''
			UrlDomain=''
			UrlContent=''
	except Exception,e:  
		Url=''
		UrlDomain=''
		UrlContent=e
	data=result+(Longitude,Latitude,LName,LAddress,LCity,PictureCount,IsMMVideo,Url,UrlDomain,UrlContent)
	insertMobileMomentSpider(data)
	


	
		
if __name__ == '__main__':
	try:
		#提取数据源
		conn=pymssql.connect(host=".",user="",password="",charset="utf8")
		cur=conn.cursor()
		cur.execute(
			"""
			select
			ExportTime,mobile,snsId,timestamp,authorId,comments,content,authorName,isCurrentUser,likes,mediaList,rawXML,MomentTime
			FROM wechat.dbo.MobileMomentcs a WHERE exists
			(SELECT mobilephone FROM wechat.dbo.[Sheet1$] b WHERE careerlevelcode_r='60~75' AND a.mobile=b.mobilephone)
			AND NOT EXISTS 
			(
			SELECT mobile FROM wechat.dbo.MobileMomentSpidercs c WHERE a.mobile=c.mobile
			)
			""")	
		resList = cur.fetchall()  
		conn.commit()
		conn.close()
		#循环爬取源数据，取出
		c=1
		for r in resList:
			print c
			try:
				spider(r)
			except Exception,e:  
				print Exception,":",e
				insertException(r[2])
			c=c+1
	except Exception,e:  
		print Exception,":",e

