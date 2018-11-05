#encoding=utf-8
#pip install lxml

import os
import json
import time
import threading
from lxml import etree
from datetime import datetime
import spider_fuc as sf

config_file="./config.json"

if __name__ == '__main__':
	print datetime.now(),"JD spider is starting......"
	#读取jason配置文件
	with open(config_file) as json_file:
		jasonData = json.load(json_file)
	homepage = jasonData['jdconfig']['homepage']
	listdir = jasonData['jdconfig']['listdir']
	productdir = jasonData['jdconfig']['productdir']
	print "======================================================="
	print datetime.now(),"step 1: opening the list pages......"
	producturl = []
	for f in os.listdir(listdir):
		#打开list pages文件
		page = open(listdir+f)
		#解析page页面
		html = etree.HTML(page.read())
		#取出商品页面
		producturls = html.xpath("//div[@id='plist']/ul/li//div[@class='p-img']/a/@href")
		producturl.extend(producturls)
		page.close()

	print producturl
	# 清空目标文件夹
	sf.emptydir(productdir)
	# 保存商品html
	for i in xrange(1,pagenum+1):
		pagehtml = listdir+str(i)+".html"
		sf.downloadhtml("http://list.jd.com/list.html?cat=9987,653,655&page=" + str(i) + "&trans=1&JL=6_0_0#J_main",pagehtml)
	print datetime.now(), "list pages are downloaded......"
"""
	# 清空目标文件夹
	sf.emptydir(listdir)
	# 保存商品页面html
	for i in xrange(1,pagenum+1):
		pagehtml = listdir+str(i)+".html"
		sf.downloadhtml("http://list.jd.com/list.html?cat=9987,653,655&page=" + str(i) + "&trans=1&JL=6_0_0#J_main",pagehtml)
	print datetime.now(), "list pages are downloaded......"
	# 获取商品总页数
	pagenum = int(html.xpath("//span[@class='p-skip']/em/b")[0].text)
	print datetime.now(), "totally",pagenum,"list pages......"
	# 清空目标文件夹
	rt.emptydir(listdir)
	# 保存商品页面html
	for i in xrange(1,pagenum+1):
		pagehtml = listdir+str(i)+".html"
		rt.downloadhtml("http://list.jd.com/list.html?cat=9987,653,655&page=" + str(i) + "&trans=1&JL=6_0_0#J_main",pagehtml)
	print datetime.now(), "list pages are downloaded......"

	"""