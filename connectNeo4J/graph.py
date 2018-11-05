#coding:utf-8

import networkx as nx #使用库的声明  
import matplotlib.pyplot as plt
import numpy as np

import xlrd
import collections
import time
ISOTIMEFORMAT='%Y-%m-%d %X'
data = xlrd.open_workbook('D:\Project\Neo4J\ShareRecord.xlsx')	#打开Excel文件读取数据
table = data.sheets()[0]              #通过索引顺序获取
nrows = table.nrows	#行数
G=nx.Graph()
for rownum in range(1,100):
	#if table.row(rownum)[5].value != 'NULL':
	#	G.add_edges_from([(str(table.row(rownum)[0].value), str(table.row(rownum)[5].value))])
	G.add_edges_from([(str(table.row(rownum)[0].value), str(table.row(rownum)[5].value))])


# e=[('4','5'),('3','4'),('2','4'),('1','2'),('7','2')]
# e=[(4,5),(3,4),(2,4),(1,2),(7,2)]  
# G=nx.Graph()
# G=nx.Graph(e)
# degree=nx.degree_histogram(G)
# e=[(4,5),(3,4),(2,4),(1,2),(7,2)]  
# e=match
# G=nx.Graph(e)
#nx.draw(G)

nx.draw(G,nx.spring_layout(G),node_size = 40,width=0.5,with_labels=False)
#nx.draw(G,nx.spring_layout(G),with_labels=False,node_size = 30) 
plt.savefig("test.png", dpi=1000)
plt.show()
        