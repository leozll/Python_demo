#coding:utf-8

from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q
import networkx as nx #使用库的声明  
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np


#连接neo4j数据库
gdb = GraphDatabase("http://localhost:7474/db/data/",username="neo4j", password="admin")

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

#plt.savefig("test.png", dpi=1000)
plt.show()



