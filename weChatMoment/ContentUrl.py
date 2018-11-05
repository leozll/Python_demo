#coding:utf-8
import xlrd
import matplotlib.pyplot as plt
import xlwt

import urllib2
import re
from bs4 import BeautifulSoup
import gzip, StringIO
import sys   
sys.setrecursionlimit(1000000)
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

#写入文件
def writeExcel(data):
	#nrows = table.nrows	#行数
	nrows = table.nrows
	ncols = table.ncols	#列数
	
	#filename = xlwt.Workbook()
	#sheet = filename.add_sheet('contenturl',cell_overwrite_ok=True)
	#sheet.write(0,17,'Url')
	#sheet.write(0,18,'UrlTitle')
	#sheet.write(0,19,'UrlContent')

	maxrow=10000
	if nrows<maxrow:
		maxrow=nrows
	for r in xrange(0,nrows,maxrow):
		
		filename = xlwt.Workbook()
		sheet = filename.add_sheet('contenturl',cell_overwrite_ok=True)
		sheet.write(0,12,'longitude')
		sheet.write(0,13,'latitude')
		sheet.write(0,14,'poiName')
		sheet.write(0,15,'poiAddress')
		sheet.write(0,16,'city')
		sheet.write(0,17,'Url')
		sheet.write(0,18,'UrlTitle')
		sheet.write(0,19,'UrlContent')
		endrow = r+maxrow if r+maxrow<nrows else nrows
		print r,endrow
		for rownum in range(r,endrow):
			
			for colnum in range(0,ncols):
				#print rownum,colnum,table.row(rownum)[0].value
				sheet.write(rownum,colnum,table.row(rownum)[colnum].value)
			try:
				###找出转发链接的内容
				##mm=table.row(rownum)[9].value.find("<title><![CDATA[微信小视频]]></title>")
				##start=table.row(rownum)[9].value.find("<contentUrl><![CDATA[")
				##if mm==-1 and start>-1:
				##	end=table.row(rownum)[9].value[start+21:].find("]]></contentUrl>")
				##	url=table.row(rownum)[9].value[start+21:start+21+end]
				##	#print rownum,"------",url
				##	url = url if url[0:4]=="http" else "http://"+url
				##	url = "http:"+url if url[0:2]=="//" else url
				##	print rownum#,"------",url
				##	soup=openSoup(url)
				##	title = soup.find('title').string if soup.find('title') else u"无题"
				##	[script.extract() for script in soup.findAll('script')]
				##	[style.extract() for style in soup.findAll('style')]
				##	soup.prettify()
				##	reg1 = re.compile("<[^>]*>")
				##	content = reg1.sub('',soup.prettify())
				##	content="".join(content.split())
				##	sheet.write(rownum,17,url)
				##	sheet.write(rownum,18,title)
				##	#sheet.write(rownum,19,content)
				##	maxlength=30000
				##	content=content[0:300000]
				##	for i in xrange(0,len(content),maxlength):
				##		#print i/maxlength,content[i:i+maxlength]
				##		sheet.write(rownum,19+i/maxlength,content[i:i+maxlength])
				##	#print "write done!"
				longitudeindex=table.row(rownum)[9].value.find("longitude")
				latitudeindex=table.row(rownum)[9].value.find("latitude")
				poiScaleindex=table.row(rownum)[9].value.find("poiScale")
				poiNameindex=table.row(rownum)[9].value.find("poiName")
				poiClassifyIdindex=table.row(rownum)[9].value.find("poiClassifyId")
				poiAddressindex=table.row(rownum)[9].value.find("poiAddress")
				cityindex=table.row(rownum)[9].value.find("city")
				endindex=table.row(rownum)[9].value.find("</location>")
				
				longitude=table.row(rownum)[9].value[longitudeindex+11:latitudeindex].replace('\\','').replace('"','').strip().replace('&#x20;',' ')
				latitudeindex=table.row(rownum)[9].value[latitudeindex+10:poiScaleindex].replace('\\','').replace('"','').strip().replace('&#x20;',' ')
				poiName=table.row(rownum)[9].value[poiNameindex+9:poiClassifyIdindex].replace('\\','').replace('"','').strip().replace('&#x20;',' ')
				poiAddress=table.row(rownum)[9].value[poiAddressindex+12:cityindex].replace('\\','').replace('"','').strip().replace('&#x20;',' ')
				city=table.row(rownum)[9].value[cityindex+6:endindex].replace('\\','').replace('"','').replace('>','').strip().replace('&#x20;',' ')
				#print rownum,longitude,latitudeindex,poiName,poiAddress,city
				
				sheet.write(rownum,12,longitude)
				sheet.write(rownum,13,latitudeindex)
				sheet.write(rownum,14,poiName)
				sheet.write(rownum,15,poiAddress)
				sheet.write(rownum,16,city)
			except Exception,e:  
				print r,str(Exception)+":"+str(e)
				sheet.write(rownum,17,str(Exception)+":"+str(e))
				continue
		index=str(r)+'-'+str(r+maxrow)
		filename.save(r'C:\Users\ZLL\Desktop\Moment'+index+'.xls')
		
if __name__ == '__main__':
	data = xlrd.open_workbook(r'C:\Users\ZLL\Desktop\Moment.xlsx')	#打开Excel文件读取数据
	table = data.sheets()[0]              #通过索引顺序获取
	try:
		writeExcel(table)
	except Exception,e:  
		print Exception,":",e

