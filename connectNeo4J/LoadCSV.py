#coding:utf-8

import xlrd
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q
import random
import string
import time
import math
import csv


#连接neo4j数据库
gdb = GraphDatabase("http://localhost:7474/db/data/",username="neo4j", password="admin")

#创建节点索引
q1 = """CREATE INDEX ON :SHARE(ShareId)"""
q2 = """CREATE INDEX ON :AGE(Age)"""
q3 = """CREATE INDEX ON :CITY(City)"""
q4 = """CREATE INDEX ON :TIME(Time)"""
q5 = """CREATE INDEX ON :ORDER(IsOrder)"""
q6 = """CREATE INDEX ON :CON(IsCon)"""
#加载节点文件
q7 = """
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///D:/neo4j/500wnode.csv" AS row
CREATE (ShareId:SHARE:AGE:CITY:TIME:ORDER:CON { ShareId:row.ShareId, Age:row.UsrAge, City:row.Usrcity, Time:row.DiffTime, IsOrder:row.IsOrder,IsCon:row.IsCon})
"""

q77 = """
CREATE (ShareId:SHARE:AGE:CITY:TIME:ORDER:CON { ShareId:'NULL'})
"""
#创建边索引
q8 = """CREATE INDEX ON :APP(App)"""
q9 = """CREATE INDEX ON :FAV(Fav)"""
#加载边文件
q10 = """
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///D:/neo4j/500wrel.csv" AS row
MATCH (ShareId:SHARE {ShareId: row.ShareId})
MATCH (ShareParentId:SHARE {ShareId: row.ShareParentId})
WHERE not (ShareId)-[:APP]->(ShareParentId)
MERGE (ShareParentId)-[pu:APP {App:row.App, Fav:row.Fav}]->(ShareId)
"""

#执行cypher语句
gdb.query(q1)
gdb.query(q2)
gdb.query(q3)
gdb.query(q4)
gdb.query(q5)
gdb.query(q6)
print "Start load nodes at ",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
gdb.query(q7)
gdb.query(q77)
print "load nodes finished at ",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
gdb.query(q8)
gdb.query(q9)
print "Start load rels at ",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
gdb.query(q10)
print "load rels finished at ",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

#CREATE (ShareId:SHARE:AGE:CITY:TIME:ORDER:CON { ShareId:'NULL', Age:NULL, City:'', Time:'', IsOrder:'',IsCon:''})



# USING PERIODIC COMMIT
# LOAD CSV WITH HEADERS FROM "file:///D:/neo4j/500wnode.csv" AS row
# MATCH (ShareId:SHARE {ShareId: 'NULL'})
# MATCH (ShareParentId:SHARE {ShareId: row.ShareId})
# WHERE not (:SHARE)-[:APP]->(ShareParentId)
# MERGE (ShareId)-[pu:APP {App:'QQ', Fav:'99'}]->(ShareParentId)
