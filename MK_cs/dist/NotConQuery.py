#coding:utf-8

from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q

import sys
reload(sys)

sys.setdefaultencoding('utf-8')
#连接neo4j数据库
gdb = GraphDatabase("http://localhost:7474/db/data/",username="neo4j", password="admin")

q3= unicode("match (a:ORDER) where a.IsCon='0' return count(*)")

conDiffusion = gdb.query(q3)
print conDiffusion[0][0]

