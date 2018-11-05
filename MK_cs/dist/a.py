#coding:utf-8

from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q
import networkx as nx #使用库的声明  
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#连接neo4j数据库
gdb = GraphDatabase("http://localhost:7474/db/data/",username="neo4j", password="admin")

#转发最多的5个ShareId
a=sys.argv[1]
if len(sys.argv)>2:
    b="and a.City CONTAINS '"+sys.argv[2]+"'"
if int(a)>5:
    a=5
q1 = unicode("match (a:SHARE),(a)-[n:APP]->(b) where exists(a.Age) "+b+" return a.ShareId,count(n) order by count(n) desc limit "+a+"")
#执行cypher语句
maxDiffusion = gdb.query(q1)
result = sys.argv[2]+u"转发最多的"+a+"个ShareId为:\n"
for a in maxDiffusion:
  result = result +u"ShareId:"+a[0]+"\n"+u"  转发次数:"+str(a[1])+"\n"
print result