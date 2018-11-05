#coding:utf-8

import xlrd
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt


data = xlrd.open_workbook('D:\Project\Neo4J\ShareRecord.xlsx')	#打开Excel文件读取数据

table = data.sheets()[0]              #通过索引顺序获取
nrows = table.nrows	#行数

__s_date = datetime.datetime(1899, 12, 31, 0).toordinal()-1
def getShareDate(date):
    if isinstance(date, float):
        date = int(date)
    d = datetime.date.fromordinal(__s_date + date)
    return d.strftime("%Y-%m-%d-%H")

shareTime = []
for rownum in range(1,nrows):
	#shareTime.append(getShareDate(table.row(rownum)[11].value))
	shareTime.append(time.strftime("%Y-%m-%d-%H",xlrd.xldate_as_tuple(table.row(rownum)[11].value, 0)+(0,0,0)))


shareStart = datetime.datetime.strptime('2016-02-23-00','%Y-%m-%d-%H')
#day = [time.strptime(d, '%Y-%m-%d-%H') for d in shareTime]
hours = [(datetime.datetime.strptime(i,'%Y-%m-%d-%H')-shareStart).total_seconds()/3600/24 for i in shareTime]


values, base = np.histogram(hours, bins = 80)
#print base

cumulative = np.cumsum(values)
plt.subplot(1, 2, 1)
plt.plot(base[:-1], cumulative, c = 'red')
plt.title('Cumulative Diffusion')
plt.ylabel('Number of Diffusion')
plt.xlabel('Days')

plt.subplot(1, 2, 2 )
plt.plot(base[:-1], values, c = 'orange')
plt.title('Daily Diffusion')
plt.xlabel('Days')
plt.show()




