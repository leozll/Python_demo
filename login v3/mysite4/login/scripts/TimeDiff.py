#coding:utf-8

from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q

import sys
reload(sys)

sys.setdefaultencoding('utf-8')
def timeDiff(queryDict):
	#连接neo4j数据库
	gdb = GraphDatabase("http://localhost:7474/db/data/",username="neo4j", password="admin")

	if queryDict['consultant'] == '':
		a=''
		a1=''
	else:
		a=" a.IsCon = '"+queryDict['consultant']+"' "
		a1=" and "

	if queryDict['order'] == '':
		b=''
		b1=''
	else:
		b=" a.IsOrder = '"+queryDict['order']+"' "
		b1=" and "

	if queryDict['city'] == '':
		c=''
	else:
		c=" a.City = '"+queryDict['city']+"' "

	if queryDict['consultant'] == '' and queryDict['order'] == '' and queryDict['city'] == '' :
		d='  WHERE EXISTS(a.Time) and a.ShareId<>"NULL"'
	else:
		d=(' WHERE EXISTS(a.Time) and a.ShareId<>"NULL" and '+a+a1+b+b1+c).rstrip().rstrip('and')
		
	#各个日期的数量
	q4= "match (a:TIME) "+d+" return left(a.Time,10),count(*) order by left(a.Time,10)"
	#执行cypher语句
	timeDiffusion = gdb.query(q4)
	timeDiff={}
	result1=[]
	result2=[]
	for a in timeDiffusion:
		result1.append(a[0])
		result2.append(a[1])
	timeDiff['time']=result1
	timeDiff['timeCount']=result2
	return timeDiff


