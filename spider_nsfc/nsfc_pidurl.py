#!/usr/bin/env python
# -*- coding:utf8 -*-
#import sys
#reload(sys)
#sys.setdefaultencoding( "utf-8" )

from selenium import webdriver
import time
import pymssql
from datetime import datetime
import socket

def nsfcLinkInfo(pidUrls):
	conn=pymssql.connect(host=".",user="",password="",charset="utf8")
	cur=conn.cursor()
	for url in pidUrls:
		cur.execute("insert INTO nsfc.dbo.nsfcLinkInfo(ProjectId,ProjectUrl,PeriodicalUrl,PeriodicalCount,ConferenceUrl,ConferenceCount,BookUrl,BookCount,RewardUrl,RewardCount,Page) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);" , url)
	conn.commit()
	conn.close()
	
def nsfcEmptyLinkLog(page):
	conn=pymssql.connect(host=".",user="",password="",charset="utf8")
	cur=conn.cursor()
	cur.execute("insert INTO nsfc.dbo.nsfcEmptyLinkLog(page) VALUES (%s);" , page)
	conn.commit()
	conn.close()

def ExceptionLog(exception,e,page):
	data=(str(''),str(exception),str(e),str(page),str(''))
	conn=pymssql.connect(host=".",user="",password="",charset="utf8")
	cur=conn.cursor()
	cur.execute("insert INTO nsfc.dbo.ExceptionLog(RunId,Exception,Message,Page,Url) VALUES (%s,%s,%s,%s,%s);", data)
	conn.commit()
	conn.close()
	time.sleep(30) 
	
if __name__ == '__main__':
	#打开指定页面
	url='http://npd.nsfc.gov.cn/projectSearch!search.action?project.applyCode=H'
	driver =webdriver.PhantomJS(executable_path="C:\Users\ZLL\Desktop\phantomjs.exe")
	driver.set_window_size(800, 600)
	#循环打开10次，防止网络问题导致网站打开失败
	#driver.get(url)
	for i in range(0,10):
		driver.get(url)
		if driver.title=='科学基金共享服务网':
			print driver.title
			break
		time.sleep(2)  
	#找出一共有多少页
	pageNumber=int(driver.find_elements_by_id('currentPageNav')[0].text.split('/')[1][:-1])
	#page=driver.find_elements_by_class_name('page')[0].find_element_by_link_text(u'最后一页').click()
	#循环所有页面
	for p in range(1,pageNumber):
		id=p*100000
		loopCount=0
		while loopCount<3:
			try:
				#显示当前页面
				print datetime.now(),u'开始查找第',p,u'页......'
				#定位到项目数据栏
				timeout = 10    
				socket.setdefaulttimeout(timeout)
				time_dl=driver.find_elements_by_class_name('time_dl')
				#如果当前页面打开失败,就写入到错误日志表中
				if len(time_dl)==0:
					nsfcEmptyLinkLog(p)
				#找出当前页面所有的项目链接
				pidLinks=[]
				for t in time_dl:
					id=id+1
					#pidLinks.append(t.find_element_by_tag_name('dt').find_element_by_tag_name('a').get_attribute("href"))
					ProjectUrl     =t.find_element_by_tag_name('dt').find_element_by_tag_name('a').get_attribute("href")
					PeriodicalUrl  =t.find_elements_by_tag_name('dd')[-1].find_elements_by_tag_name('a')[0].get_attribute("href")
					PeriodicalCount=t.find_elements_by_tag_name('dd')[-1].find_elements_by_tag_name('a')[0].text[5:-1]
					ConferenceUrl  =t.find_elements_by_tag_name('dd')[-1].find_elements_by_tag_name('a')[1].get_attribute("href")
					ConferenceCount=t.find_elements_by_tag_name('dd')[-1].find_elements_by_tag_name('a')[1].text[5:-1]
					BookUrl        =t.find_elements_by_tag_name('dd')[-1].find_elements_by_tag_name('a')[2].get_attribute("href")
					BookCount      =t.find_elements_by_tag_name('dd')[-1].find_elements_by_tag_name('a')[2].text[3:-1]
					RewardUrl      =t.find_elements_by_tag_name('dd')[-1].find_elements_by_tag_name('a')[3].get_attribute("href")
					RewardCount    =t.find_elements_by_tag_name('dd')[-1].find_elements_by_tag_name('a')[3].text[3:-1]
					pidLinks.append((id,ProjectUrl,PeriodicalUrl,PeriodicalCount,ConferenceUrl,ConferenceCount,BookUrl,BookCount,RewardUrl,RewardCount,p))
					#print ProjectUrl,PeriodicalCount,ConferenceCount,BookCount,RewardCount
				#写入url表
				nsfcLinkInfo(pidLinks)
				#点击下一页
				page=driver.find_elements_by_class_name('page')[0].find_element_by_link_text(u'下一页').click()
				#page=driver.find_elements_by_class_name('page')[0].find_element_by_link_text(u'上一页').click()
				#休眠1秒
				time.sleep(1)  
				loopCount=3
			except Exception,e:
				print '================================',datetime.now(),u'第',p,u'页出错了'
				print Exception,e
				ExceptionLog(Exception,e,p)
				loopCount=loopCount+1
				continue
			break
	#关闭当前窗口
	driver.quit()
	