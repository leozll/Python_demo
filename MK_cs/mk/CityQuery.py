#coding:utf-8

from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q

import sys
reload(sys)

sys.setdefaultencoding('utf-8')
#连接neo4j数据库
gdb = GraphDatabase("http://localhost:7474/db/data/",username="neo4j", password="admin")

#q3= """
#match (a:CITY) where a.City CONTAINS '{city}'  return count(*)
#"""
a=sys.argv[1]
q3= unicode("match (a:CITY) where a.City CONTAINS '"+a+"'  return count(*)")

cityDiffusion = gdb.query(q3)
print cityDiffusion[0][0]

