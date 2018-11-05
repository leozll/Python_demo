#coding:utf-8

from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json

def shareId(queryDict):

	if queryDict['shareId'] != '':
		#连接neo4j数据库
		gdb = GraphDatabase("http://localhost:7474/db/data/",username="neo4j", password="admin")

		shareId = queryDict['shareId']
		#起点到shareId的轨迹
		q1 = "MATCH P=(a:SHARE)-[n:APP*]->(b:SHARE) WHERE a.ShareId='NULL' and b.ShareId='"+shareId+"' RETURN nodes(P),(a),(b)"
		#执行cypher语句
		shareIdDiffusion1 = gdb.query(q1)
		nodeList=[]
		relList=[]
		#起点
		id    = "node"+str(shareIdDiffusion1[0][1]['metadata']['id'])
		label = 'APP'
		color = '#CC333F'
		att = str(json.dumps("APP"))
		node=[id,label,color,att]
		nodeList.append(node)
		for a in shareIdDiffusion1:
			for b in range(len(a[0])):
				id1 = "node"+str(a[0][b]['metadata']['id'])
				if b<len(a[0])-1:
					id2 = "node"+str(a[0][b+1]['metadata']['id'])
					rel =[id1,id2]
					relList.append(rel)
					#shareId转发给的节点
					id = "node"+str(a[0][b+1]['metadata']['id'])
					label = a[0][b+1]['data']['ShareId'][0:8]
					color = '#6A4A3C'
					if a[0][b+1]['data']['ShareId']==queryDict['shareId']:
						color = '#CC333F'
					att1 = (
					"是否顾问:"+a[0][b+1]['data']['IsCon']+
					"\r\n是否下单:"+a[0][b+1]['data']['IsOrder']+
					"\r\n省份:"+a[0][b+1]['data']['City']+
					"\r\nShareId:"+a[0][b+1]['data']['ShareId']+
					"\r\n年龄:"+a[0][b+1]['data']['Age']+
					"\r\n转发时间:"+a[0][b+1]['data']['Time'])
					att = str(json.dumps(att1))
					node=[id,label,color,att]
					nodeList.append(node)
		
		#shareId到终点的轨迹
		q2 = "MATCH P=(a:SHARE)-[n:APP*]->(b:SHARE) WHERE not (b)-->() and a.ShareId='"+shareId+"' RETURN nodes(P),(a),(b)"
		#执行cypher语句
		shareIdDiffusion2 = gdb.query(q2)
		for a in shareIdDiffusion2:
			for b in range(len(a[0])):
				id1 = "node"+str(a[0][b]['metadata']['id'])
				if b<len(a[0])-1:
					id2 = "node"+str(a[0][b+1]['metadata']['id'])
					rel =[id1,id2]
					relList.append(rel)
					#shareId转发给的节点
					id = "node"+str(a[0][b+1]['metadata']['id'])
					label = a[0][b+1]['data']['ShareId'][0:8]
					color = '#6A4A3C'
					if a[0][b+1]['data']['ShareId']==queryDict['shareId']:
						color = '#CC333F'
					att1 = (
					"是否顾问:"+a[0][b+1]['data']['IsCon']+
					"\r\n是否下单:"+a[0][b+1]['data']['IsOrder']+
					"\r\n省份:"+a[0][b+1]['data']['City']+
					"\r\nShareId:"+a[0][b+1]['data']['ShareId']+
					"\r\n年龄:"+a[0][b+1]['data']['Age']+
					"\r\n转发时间:"+a[0][b+1]['data']['Time'])
					att = str(json.dumps(att1))
					node=[id,label,color,att]
					nodeList.append(node)
					
		shareIdResult={}
		shareIdResult['nodeList']=nodeList
		shareIdResult['relList']=relList
		return shareIdResult