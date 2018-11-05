#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys

site=sys.argv[1]
# site='marykaychinaintouch'

result_context=[]
#read the metadata for config_columns
with open('metadata/1.dbo.config_columns.sql', mode='r', encoding='utf-8') as s:
    lines=s.readlines()
    for line in lines:
        #print("INSERT [dbo].[config_colusource_contexzmns] ([Site], [ColumnName]) VALUES (N'marykaychinamobileintouchapp', N'"+line[:-1]+"');")
        result_context.append("INSERT [dbo].[config_columns] ([Site], [ColumnName]) VALUES (N'"+site+"', N'"+line[:-1]+"');")
s.close()

#write the metadata for config_columns
t = open('result/'+site+'/1.dbo.config_columns.sql', 'w')
for r in result_context:
    t.write(r+"\n")
#t.write(str(result_context)[1:-1])
t.close()


