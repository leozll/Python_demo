#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import csv
import xlwt
import time 

with open('C:\Users\ZLL\Desktop\exported_sns.json') as json_file:
	jasonData = json.load(json_file)
	
filename = xlwt.Workbook()
sheet = filename.add_sheet('moment',cell_overwrite_ok=True)

lines=len(jasonData)
rows=len(jasonData[0].keys())

#写入第一行title
for r in range(rows):
	sheet.write(0,r,jasonData[0].keys()[r])
sheet.write(0,rows,"Time")

#写入朋友圈内容
name = json.dumps(jasonData[0].values()[5]).replace('"','')
file=""
for l in range(lines):
	linedata = jasonData[l]
	file = json.dumps(linedata.values()[2]).replace('"','')
	for r in range(rows):
		sheet.write(l+1,r,json.dumps(linedata.values()[r],ensure_ascii=False))
	timeStamp=float(json.dumps(linedata.values()[1],ensure_ascii=False))
	timeArray = time.localtime(timeStamp)
	sheet.write(l+1,rows,time.strftime("%Y-%m-%d %H:%M:%S", timeArray))
	#print l,jasonData[0].keys()[0],str(linedata.values()[0])
	#print l,jasonData[0].keys()[1],str(linedata.values()[1])
	#print l,jasonData[0].keys()[2],str(linedata.values()[2])
	#print l,jasonData[0].keys()[3],str(linedata.values()[3])
	#print l,jasonData[0].keys()[4],json.dumps(linedata.values()[4],ensure_ascii=False)
	#print l,jasonData[0].keys()[5],str(linedata.values()[5])
	#print l,jasonData[0].keys()[6],str(linedata.values()[6])
	#print l,jasonData[0].keys()[7],str(linedata.values()[7])
	#print l,jasonData[0].keys()[8],str(linedata.values()[8])
	#print l,jasonData[0].keys()[9],str(linedata.values()[9])

#timeStamp = 1464538274
#timeArray = time.localtime(timeStamp)
#otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
print name.decode('unicode-escape')
filename.save(r'D:\Project\MartKay\Moment\\'+file+'.xls')


