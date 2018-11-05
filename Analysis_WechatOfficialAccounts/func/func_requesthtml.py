#  -*-  coding:  UTF-8  -*-
import urllib.request

page = urllib.request.urlopen('http://www.njust.edu.cn')
htmlcode = page.read()  # .decode('gbk')#页面源码