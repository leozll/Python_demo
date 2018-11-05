# -*- coding:utf8 -*-

from selenium import webdriver
import socket
import time
from datetime import datetime
import urllib2
from lxml import etree
import json
import chardet
from StringIO import StringIO
import gzip
import re
import xlwt


def downloadurl(driver):
	# 找出一共有多少页
	pageNumber = int(driver.find_elements_by_class_name('total')[0].text.split()[1])
	urls = []
	#循环所有页面
	for p in range(1,pageNumber):
		# 显示当前页面
		print datetime.now(), u'开始查找第', p, u'页......'
		producturls=driver.find_elements_by_id('mainsrp-itemlist')[0].find_elements_by_class_name('J_ClickStat')
		print len(producturls)
		for n,p in enumerate(producturls):
			urls.append(p.get_attribute("href")) if p.text.find(u"防晒霜")>-1 else 'x'
		## 点击下一页
		print driver.find_elements_by_class_name('J_Input')[0].get_attribute("value")
		#nexturl = driver.find_elements_by_class_name('J_Ajax')[-1].get_attribute("href")
		#print nexturl#
		#driver.get("https:"+nexturl)
		page = driver.find_elements_by_class_name('J_Ajax')[-1].click()
		time.sleep(10)
		#print driver.find_elements_by_class_name('J_Input')[0].get_attribute("value")
		#productuls = driver.find_elements_by_id('mainsrp-itemlist')[0].find_elements_by_class_name('J_ClickStat')
		#print len(productuls)
		#for n, p in enumerate(productuls):#
		#	urls.append(p.get_attribute("href"))
	f = open("mkurls.txt", 'w')
	for i in set(urls):
		f.write(i+'\n')
	f.close()



if __name__ == '__main__':
	# 打开指定页面
	#url = 'https://s.taobao.com/search?q=%E8%88%92%E6%80%A1%E9%98%B2%E6%99%92%E9%9C%9CSPF20+%E7%8E%AB%E7%90%B3%E5%87%AF&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20170116&ie=utf8'
	#url= 'https://s.taobao.com/search?q=%E8%88%92%E6%80%A1%E9%98%B2%E6%99%92&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20170119&ie=utf8'
	#driver = webdriver.PhantomJS()
	##driver.set_window_size(800, 600)
	## 打开网页
	#driver.get(url)
	#print driver.title#
	##downloadurl(driver)
	## 关闭当前窗口
	#driver.quit()
	#f=open("mkurls.txt", 'r')
	#for i in f.readlines()[0:2]:
	#	print i
	#	driver.get(i)
	#	#print driver.title
	#	waittime=0
	#	time.sleep(10)
	#	lengthprice = len(driver.find_elements_by_class_name('tb-rmb-num'))
	#	lengthcount = len(driver.find_elements_by_class_name('tb-sell-counter'))
	#	lengthshop = len(driver.find_elements_by_class_name('tb-shop-name'))
	#	lengthfav = len(driver.find_elements_by_class_name('J_FavCount'))
	#	print lengthcount
	#	while lengthprice+lengthcount+lengthshop+lengthfav<4 and waittime<4:
	#		time.sleep(1)
	#		waittime=waittime+1
	#	price = driver.find_elements_by_class_name('tb-rmb-num')[-1].text
	#	count = driver.find_elements_by_class_name('tb-sell-counter')[-1].text
	#	shop = driver.find_elements_by_class_name('tb-shop-name')[0].text
	#	fav = driver.find_elements_by_class_name('J_FavCount')[0].text
	#	print "len",len(driver.find_elements_by_class_name('tb-sell-counter'))
	#	for i in driver.find_elements_by_id('J_RateCounter'):
	#		print i.text,"x"
	#	print driver.find_elements_by_id('J_SellCounter')[0].text
	#	print shop,price,count,fav


	excelfile = xlwt.Workbook()
	sheet1 = excelfile.add_sheet(u'sheet1', cell_overwrite_ok=True)

	row0 = [u'宝贝标题', u'产品名称', u'店铺名称', u'商品id', u'淘宝价', u'销售个数', u'收藏个数', 'url', u'原价']
	# 生成第一行
	for i in range(0, len(row0)):
		sheet1.write(0, i, row0[i])


	f = open("mkurls2.txt", 'r')

	f2 = open("excp.txt", 'w')



	headers = {
		 'Accept': 'application/javascript, */*;q=0.8',
		 'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
		 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
		 'Accept-Encoding': 'gzip',
		 'Host': 'detailskip.taobao.com',
		'Connection': 'Keep-Alive',
		'Cookie': 'cookie2=38f270dad590ef171ac58ccaf55fe12b; v=0; _tb_token_=eedb7db656301; uc1=cookie14=UoW%2FWXmujglOrw%3D%3D; linezing_session=dnCEBtkAvmXks7iBEU3aFlV4_1484835803481qbld_2; t=0f95c5746a1375e484367ecf1946231a; cna=sZzrEOCZazwCAWVRguc+e4h0; l=Ary8yB2f4T84gPQoVYqgl-4gDFRvYmBk; isg=Anx8i4LcCI-GeDy29pLPYTL5VBoTGCCf8iInxFb8X2fxIRyreoXwL_LbV_Sk; thw=cn; mt=ci%3D-1_0',
		'Referer': 'https://item.taobao.com/item.htm?id=2250381185&ns=1&abbucket=0'
	}
	for n,i in enumerate(f.readlines()):
		time.sleep(1)
		print n,i

		try:
			html = etree.HTML(urllib2.urlopen(i).read())
			istaobao = len(html.xpath("//div[@id='J_Pine']"))

		except Exception, e:
			print Exception, e
			html = ''
			istaobao = 0

		if istaobao == 0 :
			sheet1.write(n + 1, 0, 'xianyu')
			sheet1.write(n + 1, 7, i)
			continue

		try:
			#html = etree.HTML(urllib2.urlopen(i).read())
			producttile = html.xpath("//h3[@class='tb-main-title']")[0].text.strip() if html.xpath("//h3[@class='tb-main-title']")[0]>0 else ''
			productinfo = html.xpath("//ul[@class='attributes-list']/li")[0].text[5:] if len(html.xpath("//ul[@class='attributes-list']/li"))>0 else ''
			productid = html.xpath("//div[@id='J_Pine']/@data-itemid")[0] if len(html.xpath("//div[@id='J_Pine']/@data-itemid"))>0 else ''
			sellerid = html.xpath("//div[@id='J_Pine']/@data-sellerid")[0] if len(html.xpath("//div[@id='J_Pine']/@data-itemid"))>0 else ''
			shopname = html.xpath("//div[@class='tb-shop-name']/dl/dd/strong/a")[0].text.strip() if len(html.xpath("//div[@class='tb-shop-name']/dl/dd/strong/a"))>0 else ''

			requesturl = 'https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId='+productid+'&sellerId='+sellerid+'&modules=dynStock,qrcode,viewer,price,contract,duty,xmpPromotion,delivery,activity,fqg,zjys,couponActivity,soldQuantity&callback=onSibRequestSuccess'
			a = html.xpath("//script")[0].text
			u = re.compile(r'//count.taobao.com/counter3?(.+?),SCCP_2_')
			favurl = 'https://count.taobao.com/counter3?callback=jsonp87&'+re.findall(u, a)[0]
			#html = urllib2.urlopen(urllib2.Request(requesturl,headers=headers)).read()
			request = urllib2.Request(requesturl,headers=headers)
			response = urllib2.urlopen(request, timeout=20)#.read().decode('unicode-escape').encode('utf-8')
				#.decode('gb18030').encode('utf-8')
			if response.info().get('Content-Encoding') == 'gzip':
				buf = StringIO(response.read())
				f = gzip.GzipFile(fileobj=buf)
				data = f.read()
			jasonData = json.loads(str(data)[22:-2])
			if len(jasonData[u'data'][u'promotion'][u'promoData'])>0:
				print 1
				print jasonData[u'data'][u'promotion'][u'promoData'][u'def'][0][u'loginPromotion']
				if jasonData[u'data'][u'promotion'][u'promoData'][u'def'][0][u'loginPromotion']!=1:
					price = jasonData[u'data'][u'promotion'][u'promoData'][u'def'][0][u'price']
				else:
					price = jasonData[u'data'][u'price']
			else:
				price = jasonData[u'data'][u'price']
			confirmGoodsCount = jasonData[u'data'][u'soldQuantity'][u'confirmGoodsCount']
			soldTotalCount = jasonData[u'data'][u'soldQuantity'][u'soldTotalCount']
			data = urllib2.urlopen(favurl, timeout=20).read()
			jasonData = json.loads(str(data)[8:-2])
			favcount = jasonData[u'ICCP_1_'+productid]

			sheet1.write(n + 1, 0, producttile)
			sheet1.write(n + 1, 1, productinfo)
			sheet1.write(n + 1, 2, shopname)
			sheet1.write(n + 1, 3, productid)
			sheet1.write(n + 1, 4, price)
			sheet1.write(n + 1, 5, confirmGoodsCount)
			sheet1.write(n + 1, 6, favcount)
			sheet1.write(n + 1, 7, i)
		except Exception, e:
			print i,Exception,e
			f2.write(i+str(Exception)+str(e) + '\n')
	f.close()
	f2.close()
	excelfile.save('mktb.xls')