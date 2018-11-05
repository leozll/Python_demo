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
import networkx as nx #使用库的声明  
import matplotlib.pyplot as plt

#连接neo4j数据库
gdb = GraphDatabase("http://localhost:7474/db/data/",username="neo4j", password="admin")
plt.subplot(2, 1, 1)
G=nx.Graph()
#查询ShareId
param=sys.argv[1]
q1 = "MATCH P=(a:SHARE)-[n:APP*]->(b:SHARE) WHERE a.ShareId='NULL' and b.ShareId='"+param+"' RETURN nodes(P)"
#执行cypher语句
nodes = gdb.query(q1)
for a in nodes:
  for b in range(len(a[0])-1):
    G.add_edges_from([(a[0][b]['data']['ShareId'][0:8],a[0][b+1]['data']['ShareId'][0:8] )])

q2 = "MATCH P=(a:SHARE)-[n:APP*]->(b:SHARE) WHERE a.ShareId='"+param+"' RETURN nodes(P)"
#执行cypher语句
nodes = gdb.query(q2)
for a in nodes:
  for b in range(len(a[0])-1):
    G.add_edges_from([(a[0][b]['data']['ShareId'][0:8],a[0][b+1]['data']['ShareId'][0:8] )])
nx.draw(G,nx.spring_layout(G),node_size = 500,arrows=True)



plt.subplot(2, 1, 2)
G=nx.Graph()
nx.draw(G,nx.spring_layout(G),node_size = 500,arrows=True)

q3 = unicode("MATCH (a:SHARE) WHERE a.ShareId='"+param+"' RETURN a")
aAtt = gdb.query(q3)
att=''
for a in aAtt:
  for b in a:
    for key in b['data'].keys():
      att = att+key+': '+b['data'][key]+'\n'
plt.text(0.5,0.3,att,color='blue',ha='center', fontproperties='SimHei')


plt.show()