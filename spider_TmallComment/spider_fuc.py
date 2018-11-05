# coding=utf-8

# 根据参数文件里的配置，启动多线程
import os
import json
import time
from datetime import datetime
import threading
import urllib2

# 读取jason配置文件
config_file="./config.json"
with open(config_file) as json_file:
	jasonData = json.load(json_file)
jdcookie = jasonData['jdconfig']['jdcookie']

# 手动设置cookie信息
class SimpleCookieHandler(urllib2.BaseHandler):
	def http_request(self, req):
		if not req.has_header('Cookie'):
			req.add_unredirected_header('Cookie', jdcookie)
		else:
			cookie = req.get_header('Cookie')
			req.add_unredirected_header('Cookie', jdcookie + '; ' + cookie)
		return req


def readurl(url):
	# 读取url内容
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(), SimpleCookieHandler())
	req = urllib2.Request(url)
	return opener.open(req, timeout=20).read()


def downloadhtml(url, htmlpath):
	# 读取url内容
	htmlcontent = readurl(url)
	# 写入url内容到本地txt文件
	f = open(htmlpath, 'w')
	f.write(htmlcontent)
	f.close()


def emptydir(dir):
	for f in os.listdir(dir):
		os.remove(os.path.join(dir, f))


def runthreads(threadsnum, taskname, list, *args):
	threads = []
	# 每一个线程分配的url个数
	onethreaditems = len(list) / threadsnum + 1
	print datetime.now(), "each thread will handle", onethreaditems, "urls......"
	# 将url列表按照分组分配给每一个线程
	for a in xrange(0, len(list), onethreaditems):
		urls = list[a:a + onethreaditems]
		parms = (urls,) + args
		t = threading.Thread(target=taskname, args=parms)
		threads.append(t)
	for i, t in enumerate(threads):
		t.setDaemon(True)
		print datetime.now(), "Thread", i + 1, "is starting....."
		t.start()
		time.sleep(1)
	for t in threads:
		t.join()
	print datetime.now(), "all threads are over....."
