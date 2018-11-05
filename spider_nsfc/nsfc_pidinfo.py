#coding:utf-8
# -*- coding:utf8 -*-
#import sys
#reload(sys)
#sys.setdefaultencoding( "utf-8" )
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
def insertProjectInfo(data):
	conn=pymssql.connect(host=".",user="",password="",charset="utf8")
	cur=conn.cursor()
	cur.execute(
		"""insert INTO nsfc.dbo.ProjectInfo
		(
		ProjectId,PID,ProjectName,ProjectType,ProjectCode,ProjectLeader,ProjectTitle,Organization,ProjectDuration,ProjectFunds,
		ChAbs,ChTitle,EngAbs,EngTitle,AbsTitle,Url
		)
		 VALUES 
		(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""" , data)
	conn.commit()
	conn.close()
	
def ExceptionLog(exception,e,url):
	data=(str(''),str(exception),str(e),str(''),str(url[0]))
	conn=pymssql.connect(host=".",user="",password="",charset="utf8")
	cur=conn.cursor()
	cur.execute("insert INTO nsfc.dbo.ExceptionLog(RunId,Exception,Message,Page,Url) VALUES (%s,%s,%s,%s,%s);", data)
	conn.commit()
	conn.close()
	time.sleep(30) 
	
#打开url
def openSoup(url):
	timeout = 10    
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
def spider(result,id):
	pidurl=result[0]
	soup=openSoup(pidurl)
	#基本信息
	jben=soup.find('div',id='right')
	pid=jben.find_all('p')[0].contents[-1]
	projectName=jben.find_all('p')[1].contents[-1]
	projectType=jben.find_all('p')[2].contents[-1]
	projectCode=jben.find_all('p')[3].contents[-1]
	projectLeader=jben.find_all('p')[4].contents[-1].text
	projectTitle=jben.find_all('p')[5].contents[-1]
	organization=jben.find_all('p')[6].contents[-1].text
	projectDuration=jben.find_all('p')[7].contents[-1]
	projectFunds=jben.find_all('p')[8].contents[-1]
	
	#项目摘要
	zyao=soup.find('div',class_='zyao')
	chAbs=zyao.find_all('div')[1].text
	chTitle=zyao.find('p',class_='xmu').contents[-1] if len(zyao.find('p',class_='xmu'))==2 else ''	
	engAbs=zyao.find_all('div')[5].text
	engTitle=zyao.find_all('p',class_='xmu')[1].contents[-1] if len(zyao.find_all('p',class_='xmu')[1])==2 else ''	
	absTitle=zyao.find('div',class_='cguo').text
	
	data=(id,pid,projectName,projectType,projectCode,projectLeader,projectTitle,organization,projectDuration,projectFunds,chAbs,chTitle,engAbs,engTitle,absTitle,pidurl)
	#print data
	#insertProjectInfo(data)

	#项目成果
	cguo=soup.find_all('div',class_='cguo')[1].find_all('a')
	for c in cguo:
		print c['href'],c.text
		typeid=c['href'][c['href'].find('typeId=')+7:]
	
	##期刊
	#if typeid=='010':
	##会议
	#if typeid=='020':
	##著作
	#if typeid=='030':
	##奖励
	#if typeid=='090':

if __name__ == '__main__':
	try:
		#提取数据源
		conn=pymssql.connect(host=".",user="",password="",charset="utf8")
		cur=conn.cursor()
		cur.execute(
			"""
			select
			ProjectUrl
			from nsfc.dbo.nsfcLinkInfo
			""")
		resList = cur.fetchall()  
		conn.commit()
		conn.close()
		resList=(('http://npd.nsfc.gov.cn/projectDetail.action?pid=39970736',),('http://npd.nsfc.gov.cn/projectDetail.action?pid=30572167',))
		#39970736
		#30572167
		#循环爬取源数据，取出
		id=0
		for r in resList:
			id=id+1
			try:
				spider(r,id)
			except Exception,e:  
				print Exception,":",str(e)
				ExceptionLog(Exception,e,r)
	except Exception,e:  
		print Exception,":",e

