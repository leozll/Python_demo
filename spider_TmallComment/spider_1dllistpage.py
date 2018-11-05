#encoding=utf-8
#pip install lxml

import json
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
	print "======================================================="
	print datetime.now(),"step 1: downloading the list pages......"
	# 获取html
	html = etree.HTML(sf.readurl(homepage))
	# 获取商品总页数
	pagenum = int(html.xpath("//span[@class='p-skip']/em/b")[0].text)
	print datetime.now(), "totally",pagenum,"list pages......"
	# 清空目标文件夹
	sf.emptydir(listdir)
	# 保存list页面html
	for i in xrange(1,pagenum+1):
		pagehtml = listdir+str(i)+".html"
		sf.downloadhtml("http://list.jd.com/list.html?cat=9987,653,655&page=" + str(i) + "&trans=1&JL=6_0_0#J_main",pagehtml)
	print datetime.now(), "list pages are downloaded......"