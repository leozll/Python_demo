#coding:utf-8

import xlrd
import collections
import time
ISOTIMEFORMAT='%Y-%m-%d %X'

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