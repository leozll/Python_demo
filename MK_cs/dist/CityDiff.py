#coding:utf-8

from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q
import networkx as nx #使用库的声明  
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np


#连接neo4j数据库
gdb = GraphDatabase("http://localhost:7474/db/data/",username="neo4j", password="admin")

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

#plt.savefig("test.png", dpi=1000)
plt.show()



