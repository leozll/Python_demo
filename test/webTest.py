#-*- coding:utf-8 -*-
import urllib.request
from lxml import etree
import time
import re
webpage=urllib.request.urlopen('https://www.qidian.com/free/all?orderId=&vip=hidden&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=1&page=1').read()
localTime=time.strftime("%y%m%d")
print(localTime)

html = webpage.decode('UTF-8')
e = etree.HTML(html)
infos = e.xpath("//div[@class='book-mid-info']/h4/a")

filename="D:\\"+localTime+".txt"
file=open(filename,'w')
for i in infos:
    print(i.text)
    file.write(i.text+'\n')


file.close()
