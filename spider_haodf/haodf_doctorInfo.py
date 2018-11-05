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
import pymssql
import xlrd
import time  
from datetime import date, datetime, timedelta
import threading

def insertDoctor(data):
	conn=pymssql.connect(host=".",user="",password="",charset="utf8")
	cur=conn.cursor()
	cur.execute(
		"""insert INTO haodf.dbo.Doctor(addr,hospital,department,docname,professionalTitle,academicTitle,beGoodAt,practiceExperience,thanksLetter,present,headIconUrl,clinicalExperience,patientsTreatedNumbers,patientsFollowUpNumbers,diagnosisServiceStar,patientsVote,curativeEffect,attitude,patientsQuestions,replied,serviceCharge,mins,visitsSuccess,doctorurl,facultyurl)
		VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""" , data)
	conn.commit()
	conn.close()
	
def facultyLog(url,runid):
	data=(runid,url)
	conn=pymssql.connect(host=".",user="",password="",charset="utf8")
	cur=conn.cursor()
	cur.execute("insert INTO haodf.dbo.facultyLog(RunId,Url) VALUES (%s,%s);" , data)
	conn.commit()
	conn.close()
	
def facultyCheck(facultys):
	conn=pymssql.connect(host=".",user="",password="",charset="utf8")
	cur=conn.cursor()
	cur.execute("select distinct Url from haodf.dbo.facultyLog")
	resList = cur.fetchall()  
	conn.commit()
	conn.close()
	for r in resList:
		facultys.remove(r[0])
	
#def runId():
#	id=""
#	conn=pymssql.connect(host=".",user="",password="",charset="utf8")
#	cur=conn.cursor()
#	cur.execute("select max(RunId) from haodf.dbo.facultyLog")
#	resList = cur.fetchall()  
#	conn.commit()
#	conn.close()
#	for r in resList:
#		id=r[0] if r[0] else 0
#	return id
	

	
def ExceptionLog(exception,e,fac,docL,runid):
	data=(runid,str(exception),str(e),str(docL),str(fac))
	conn=pymssql.connect(host=".",user="",password="",charset="utf8")
	cur=conn.cursor()
	cur.execute("insert INTO haodf.dbo.ExceptionLog(RunId,Exception,Message,DoctorUrl,FacultyUrl) VALUES (%s,%s,%s,%s,%s);", data)
	conn.commit()
	conn.close()
	time.sleep(30) 
	

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


#查询所有医生链接
def allDoctorsLink(soup,doctorLinks):
	AlldocL = soup.find_all('a',class_="name")
	for docL in AlldocL:
		doctorLinks.append(docL['href'])


def allDoctors(doctorurl,facultyurl):

	addr=""
	hospital=""
	department=""
	docname=""
	professionalTitle=""
	academicTitle=""
	beGoodAt=""
	practiceExperience=""
	thanksLetter=""
	present=""
	headIconUrl=""
	patientsQuestions=""
	replied=""
	serviceCharge=""
	mins=""
	visitsSuccess=""
	clinicalExperience=""
	patientsTreatedNumbers=""
	patientsFollowUpNumbers=""
	diagnosisServiceStar=""
	patientsVote=""
	curativeEffect=""
	attitude=""
	
	host = 'www.haodf.com'
	soup = openSoup(doctorurl,host)
	Alldoc = soup.find_all('script')
	for data in Alldoc:
		if data.text.find('class=\\"luj\\"')>0:
			d=eval(data.text[24:-2])
			e=d['content'].replace("\\/","/").decode("unicode-escape")
			infos = BeautifulSoup(e,"html.parser").find('div',class_='luj').find_all('a')
			#省份
			addr=infos[2].string
			#医院
			hospital=infos[3].string
			#部门
			department=infos[4].string
		if data.text.find('doctor_about')>0:
			d=eval(data.text[24:-2])
			e=d['content'][d['content'].index('<\/style>')+9:].replace("\\/","/").decode("unicode-escape")
			soup = BeautifulSoup(e,"html.parser")
			#print e
			tds=soup.find_all('td')
			#医生名字
			docname=soup.find('h1').text[:-4].strip()
			#专业职称
			professionalTitle=tds[6].text.split(" ")[0]
			#学术职称
			academicTitle=(tds[6].text.split(" ")[-1] if tds[6].text.split(" ")[0]<>tds[6].text.split(" ")  else '')
			#擅长
			beGoodAt=(soup.find('div',id='full_DoctorSpecialize').text.strip() if soup.find('div',id='full_DoctorSpecialize') else '')
			#执业经历
			practiceExperience=(soup.find('div',id='full').text.strip()[:-5] if soup.find('div',id='full') else '')
			if practiceExperience=='':
				practiceExperience=soup.find_all('td',colspan='3')[1].next_element.strip()
			#感谢信
			thanksLetter=(soup.find('a',class_="button_halfgxx halfgxx_bgletter J_switchcomments").span.text.strip() if soup.find('a',class_="button_halfgxx halfgxx_bgletter J_switchcomments") else '')
			#礼物
			present=(soup.find('a',class_="button_halfgxx halfgxx_bgpresent J_switchcomments").span.text.strip() if soup.find('a',class_="button_halfgxx halfgxx_bgpresent J_switchcomments") else '')
			#头像
			headIconUrl=(soup.find('td',align="center").img['src'] if soup.find('td',align="center") and soup.find('td',align="center").img else '')
			#患者提问
			patientsQuestions=(soup.find_all('p')[1].find_all('span')[0].text if soup.find('p') else '')
			#回复
			replied=(soup.find_all('p')[1].find_all('span')[1].text if soup.find('p') else '')
			#服务费
			serviceCharge=(soup.find('span',class_='show_price').text[:-3] if soup.find('span',class_='show_price') else '')
			#时长
			mins=(soup.find('span',class_='show_duration').text[3:-3] if soup.find('span',class_='show_duration') else '')
			#预约就诊成功
			visitsSuccess=(soup.find('a',class_='orange').text if soup.find('a',class_='orange') else '')
		if data.text.find('bp_doctor_servicestar')>0:
			d=eval(data.text[24:-2])
			e=d['content'].replace("\\/","/").decode("unicode-escape")
			soup = BeautifulSoup(e,"html.parser")
			#临床经验
			clinicalExperience=(soup.find('table',class_='jbsm').text.replace(' ','').replace('\n','').strip() if soup.find('table',class_='jbsm') else '')
			#诊治过的患者数
			patientsTreatedNumbers=(soup.find('table',align="center").find('td').text.split(u"：")[-1].replace(u"例","") if soup.find('table',align="center") else '')
			#随访中的患者数
			patientsFollowUpNumbers=(soup.find('table',align="center").find_all('td')[1].text.split(u"：")[-1].replace(u"例","") if soup.find('table',align="center") else '')
			#诊后服务星
			diagnosisServiceStar=e.count('starRightliang')

		if data.text.find('"bp_doctor_getvote"')>0:
			d=eval(data.text[24:-2])
			e=d['content'].replace("\\/","/").decode("unicode-escape")
			soup = BeautifulSoup(e,"html.parser")
			#print e
			vote1=(BeautifulSoup(e,"html.parser").find('table',class_='jbsm').text.replace(' ','').replace('	','').replace('\n','').strip() if BeautifulSoup(e,"html.parser").find('table',class_='jbsm') else '')
			vote2=(soup.find('a',href=re.compile('http://www.haodf.com/doctor')).text[2:-2] if soup.find('a',href=re.compile('http://www.haodf.com/doctor')) else '')
			#患者投票
			patientsVote=vote1+' '+vote2
			infos=soup.find('div',class_="rtdiv")
			#疗效
			curativeEffect=(infos.find_all('td')[2].text[:-2].strip() if infos else '')
			#态度
			attitude=(infos.find_all('td')[5].text[:-2].strip() if infos else '')
	#print addr,hospital,department,docname,professionalTitle,academicTitle,beGoodAt,practiceExperience,thanksLetter,present,headIconUrl,clinicalExperience,patientsTreatedNumbers,patientsFollowUpNumbers,diagnosisServiceStar,patientsVote,curativeEffect,attitude,patientsQuestions,replied,serviceCharge,mins,visitsSuccess
	data=(addr,hospital,department,docname,professionalTitle,academicTitle,beGoodAt,practiceExperience,thanksLetter,present,headIconUrl,clinicalExperience,patientsTreatedNumbers,patientsFollowUpNumbers,diagnosisServiceStar,patientsVote,curativeEffect,attitude,patientsQuestions,replied,serviceCharge,mins,visitsSuccess,doctorurl,facultyurl)
	insertDoctor(data)

def run(runid,facultys):
	print datetime.now(),"start Thread:",runid,"=========================================="
	for fac in facultys:
		try:
			docL=""
			doctorLinks=[]
			soup = openSoup(fac,'www.haodf.com')
			#找出faculty链接下的所有Doctor链接
			allDoctorsLink(soup,doctorLinks)
			pages = soup.find_all('a',class_='p_num')
			#找出faculty链接下page2之后的所有Doctor链接
			for p in pages:
				soup = openSoup(p['href'],'www.haodf.com')
				allDoctorsLink(soup,doctorLinks)
			#去重
			doctorLinks=list(set(doctorLinks))
			#爬虫Doctor链接
			doctors=[]
			#doctorLinks=['http://www.haodf.com/doctor/DE4r0Fy0C9LugYKmk8K415FhFZqqOoERk.htm']
			for docL in doctorLinks:
				 allDoctors(docL,fac)
			facultyLog(fac,runid)
		except Exception,e:
			print fac
			ExceptionLog(Exception,e,fac,docL,runid)
	print datetime.now(),"finish Thread:",runid,"=========================================="



if __name__ == '__main__':
	print datetime.now(),"work start============================================================="

	data = xlrd.open_workbook(r'C:\Users\ZLL\Desktop\FacLink.xlsx')	#打开Excel文件读取数据
	table = data.sheets()[0]              #通过索引顺序获取
	nrows = table.nrows
	facultys=[]
	for r in range(0,nrows):
		facultys.append(table.row(r)[0].value)
	#删除已经成功爬虫过的faculty链接
	facultyCheck(facultys)

	rows=len(facultys)
	print "rows:",rows
	threads = []
	threadnum=20
	onethreadrows=rows/threadnum+1
	for r in xrange(0,rows,onethreadrows):
		#print r/onethreadrows+1,facultys[r:r+onethreadrows]
		runid=int(r/onethreadrows+1)
		threadFacultys=facultys[r:r+onethreadrows]
		t=threading.Thread(target=run,args=(runid,threadFacultys))
		threads.append(t)

	for t in threads:
		#t.setDaemon(True)
		t.start()
		time.sleep(1) 

	print datetime.now(),"Done!============================================================="

	

	
	