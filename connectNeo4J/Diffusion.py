#coding:utf-8

import xlrd
import collections

import time
import datetime
import numpy as np
import matplotlib.pyplot as plt


data = xlrd.open_workbook('D:\Project\Neo4J\ShareRecord.xlsx')	#打开Excel文件读取数据
table = data.sheets()[0]              #通过索引顺序获取
#table = data.sheet_by_index(0)        #通过索引顺序获取
#table = data.sheet_by_name(u'Sheet1') #通过名称获取

nrows = table.nrows	#行数
ncols = table.ncols	#列数


parentCount= []
for rownum in range(1,nrows):
	if table.row(rownum)[5].value != 'NULL':
		parentCount.append(table.row(rownum)[5].value)
parentCounter = collections.Counter(parentCount)
#print parentCounter.most_common(3)			#筛选出传播前3的ID
print u"最广的传播源:",parentCounter.most_common(3)[0][0]
print u"最广的传播数量:",parentCounter.most_common(3)[0][1]

#print parentCounter

file_object = open('thefile1.txt', 'w')
for rownum in range(1,nrows):
	#print table.row(rownum)[5].value,parentCounter[table.row(rownum)[5].value]
	file_object.write(str(parentCounter[table.row(rownum)[5].value])+ '\n')

#取出shareID和ParentShareID
match= {}
for rownum in range(1,nrows):
	match[table.row(rownum)[0].value]=table.row(rownum)[5].value

##去除match中传播链的中间过程
# newMatch = match
# for k in newMatch.keys():
	# if k in newMatch.values():
		# del newMatch[k] 


#计算start和end之间的任一轨迹
def find_path(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not graph.has_key(start):
            return None
        node = graph[start]
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath: return newpath
        return NONE

#计算start和end之间的所有轨迹
def find_all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if not graph.has_key(start):
            return []
        paths = []
        node = graph[start]
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
        return paths
        
#计算出所有的传播链

mylistDict = {}
for shareId,parentShareId in match.items():
	if len(find_all_paths(match,shareId,'NULL'))==0:
		#mylist.append(find_all_paths(match,shareId,parentShareId))
		mylistDict[shareId]=find_all_paths(match,shareId,parentShareId)
	else:
		#mylist.append(find_all_paths(match,shareId,'NULL'))
		mylistDict[shareId]=find_all_paths(match,shareId,'NULL')


#去除mylistDict中传播链的中间过程
for k in match.keys():
	if k in match.values():
		del mylistDict[k] 
mylist = []
for v in mylistDict.values():
	mylist.append(v)



#选出最长的传播链
def chooseMost(mylist):
    temp=[]
    for i in range(0,len(mylist)-1):
        #print len(mylist[i][0])
        if len(mylist[i])>0:
			temp+=[len(mylist[i][0])]
        else:
			temp+=[1]
	#print temp.index(max(temp))
    return mylist[temp.index(max(temp))]

most = chooseMost(mylist)



#将传播链写入文件
#print len(mylist)
#print mylist[0][0][0]
file_object = open('thefile.txt', 'w')
for listitem in mylist:
	#print ','.join(listitem[0])
	file_object.write(','.join(listitem[0])+ '\n')

#转变最长的传播链
link = ''
for i in range(0,len(most[0]))[::-1]:
	if most[0][i] == 'NULL':
		link = 'App'
	elif i == 0:
		link = link + '->' + most[0][i]
	else: link = link + '->' + most[0][i] 

print u"最深的传播链:",link











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

