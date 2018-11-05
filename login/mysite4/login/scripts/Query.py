#coding:utf-8

from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q

import sys
reload(sys)

sys.setdefaultencoding('utf-8')
#连接neo4j数据库


def orderQuery(queryDict):
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
        d='  WHERE a.ShareId<>"NULL"'
        f='  WHERE c.ShareId="NULL" '
    else:
        d=(' WHERE a.ShareId<>"NULL" and '+a+a1+b+b1+c).rstrip().rstrip('and')
        f=(' WHERE c.ShareId="NULL" and '+a+a1+b+b1+c).rstrip().rstrip('and')
    
    q1 = unicode("match (a:CON:ORDER:CITY:AGE:TIME) "+d+" return count(*)")
    diffCount = "转发数量:"+str(gdb.query(q1)[0][0])

    spanDiffusion=''
    if str(queryDict['span']) != 'None':
        e=str(queryDict['span'])
        q2 = unicode("match (a:SHARE),(a)-[n:APP]->(b) "+d+" return a.ShareId,count(n) order by count(n) desc limit "+e+"")
        spanResult = gdb.query(q2)
        spanDiffusion = u"转发最广的"+e+"个ShareId为:\r\n"
        for a in spanResult:
            spanDiffusion = spanDiffusion +u"ShareId:"+a[0]+"  "+u"转发次数:"+str(a[1])+" \r\n"

    depthDiffusion=''
    if str(queryDict['depth']) != 'None':
        e=str(queryDict['depth'])
        q3 = unicode("match (c:SHARE),(c)-[n:APP*]->(a:SHARE) "+f+" return a.ShareId,size(n) order by size(n) desc limit "+e+"")
        depthResult = gdb.query(q3)
        depthDiffusion = u"转发最深的"+e+"个ShareId为:\r\n"
        for a in depthResult:
            depthDiffusion = depthDiffusion +u"ShareId:"+a[0]+"  "+u"转发深度:"+str(a[1])+" \r\n"


    queryResult={}
    queryResult['diffCount']=diffCount
    queryResult['spanDiffusion']=spanDiffusion
    queryResult['depthDiffusion']=depthDiffusion
    
    return queryResult

