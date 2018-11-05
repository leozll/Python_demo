#coding:utf-8

from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q
import networkx as nx #使用库的声明  
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np


#连接neo4j数据库
gdb = GraphDatabase("http://localhost:7474/db/data/",username="neo4j", password="admin")

# #转发最多的5个ShareId
# q1 = """match (a:SHARE),(a)-[n:APP]->(b) where a.ShareId<>'NULL' return a.ShareId,count(n) order by count(n) desc limit 5"""
# #执行cypher语句
# maxDiffusion = gdb.query(q1)
# print u"转发最多的5个ShareId为:"
# for a in maxDiffusion:
  # print u"ShareId:",a[0],u"  转发次数:",a[1]

# #转发最深的5条路径
# q2 = """
# match (a:SHARE),p=(a)-[n:APP*]->(b:SHARE) 
# WHERE a.ShareId='NULL' and not (b)-->()
# return nodes(p)  order by size(n) desc limit 5
# """
# #执行cypher语句
# longestDiffusion = gdb.query(q2)
# print u"转发最深的5条路径为:"
# path=''
# for a in longestDiffusion:
  # for b in a[0]:
    # #print b['data']['ShareId']
    # path=path+b['data']['ShareId']+' -> '
  # print path.replace('NULL','APP').strip(' -> ')
  # path=''

  
ax = plt.axes()
#各个年龄的数量
q3= """
match (a:AGE) where EXISTS(a.Age) return a.Age,count(*) order by toInt(a.Age)
"""
#执行cypher语句
ageDiffusion = gdb.query(q3)
ageX=[]
ageY=[]
for a in ageDiffusion:
  ageX.append(a[0])
  ageY.append(a[1])

#对各个年龄的数量进行绘图
#plt.subplot(2, 2, 1)
plt.plot(ageX, ageY, c = 'red')
plt.title('Age Diffusion')
plt.ylabel('Number of Diffusion')
plt.xlabel('Ages')
plt.savefig("Ages.png", dpi=1000)
plt.close()

#各个城市的数量
q4= """
match (a:CITY) where EXISTS(a.City) return a.City,count(*) order by count(*)
"""
#执行cypher语句
cityDiffusion = gdb.query(q4)
cityX=[]
cityY=[]
for a in cityDiffusion:
  cityX.append(a[0])
  cityY.append(a[1])
#对各个城市的数量进行绘图
position = np.arange(len(cityX))
#plt.subplot(2, 2, 2)
ax = plt.axes()
ax.set_xticks(position +0.5)
font = FontProperties(fname = r'c:\windows\fonts\simsun.ttc', size = 8)
ax.set_xticklabels(cityX, fontproperties = font, ha='center', rotation=90)
plt.bar(position, cityY)
plt.title('Province Diffusion')
plt.ylabel('Number of Diffusion')
plt.xlabel('Provinces')
plt.savefig("Provinces.png", dpi=1000)
plt.close()
  
#下单数量
q5= """
match (a:ORDER) where EXISTS(a.IsOrder) return (case a.IsOrder when "1" then "已下单" when "0" then "未下单" else  "未知" end),count(*) order by count(*)
"""
#执行cypher语句
orderDiffusion = gdb.query(q5)
orderX=[]
orderY=[]
for a in orderDiffusion:
  orderX.append(a[0])
  orderY.append(a[1])
#对各个城市的数量进行绘图
position = np.arange(len(orderX))
ax = plt.axes()
plt.subplot(2, 1, 1)
ax.set_xticks(position +2)
font = FontProperties(fname = r'c:\windows\fonts\simsun.ttc', size = 8)
ax.set_xticklabels(orderX, fontproperties = font, ha='center', rotation=90)
plt.bar(position, orderY)
plt.title('Order Count')
plt.ylabel('Number of Order')
plt.xlabel(u'下单情况')
plt.savefig("Order.png", dpi=1000)


#顾问数量
q6= """
match (a:ORDER) where EXISTS(a.IsCon) return (case a.IsCon when "1" then "顾问" when "0" then "非顾问" else  "未知" end),count(*) order by count(*)
"""
#执行cypher语句
conDiffusion = gdb.query(q6)
conX=[]
conY=[]
for a in conDiffusion:
  conX.append(a[0])
  conY.append(a[1])
#对各个城市的数量进行绘图
position = np.arange(len(conX))
plt.subplot(2, 1, 2)
#ax = plt.axes()
ax.set_xticks(position )
font = FontProperties(fname = r'c:\windows\fonts\simsun.ttc', size = 8)
ax.set_xticklabels(conX, fontproperties = font, ha='center', rotation=90)
plt.bar(position, conY)
plt.title('Consultant Count')
plt.ylabel('Number of Consultant')
plt.xlabel(u'顾问情况')
plt.savefig("Con'.png", dpi=1000)





#plt.savefig("test.png", dpi=1000)
#plt.show()



