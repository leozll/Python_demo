#!/usr/bin/env python
# -*- coding:utf8 -*-
import xlrd
import sys

site=sys.argv[1]
# site='marykaychinaintouch'

#open the mapping
wb = xlrd.open_workbook('./metadata/mapping.xlsx')
#open the first sheet
sh=wb.sheet_by_index(0)

#no close？？


pv=[]
pv_seq={}
#read the prop columns
for r in range(sh.nrows):
    if sh.row(r)[0].value==site and (sh.row(r)[1].value[0:4]=='prop'):
        pv.append(''.join(sh.row(r)[2].value.split()))

result_context=[]
#generate the data for config_event_mapping
for r in range(sh.nrows):
    if sh.row(r)[0].value==site and sh.row(r)[1].value[0:4]!='prop' :
        sitecolumn="'"+site+"'"
        OrginalColumn="'"+sh.row(r)[1].value+"'"
        BusinessName="'"+''.join(sh.row(r)[2].value.split())+"'"
        StartTime="CAST(N'2010-01-01 00:00:00.000' AS DateTime)"
        EndTime="CAST(N'2010-01-01 00:00:00.000' AS DateTime)"
        sql="INSERT [dbo].[config_event_mapping] ([Site], [OrginalColumn], [BusinessName], [StartTime], [EndTime]) VALUES (" + sitecolumn + "," + OrginalColumn+ "," + BusinessName+ ", CAST(N'2010-01-01 00:00:00.000' AS DateTime), CAST(N'2999-01-01 00:00:00.000' AS DateTime));"
        result_context.append(sql)

#write the metadata for config_columns
t = open('result/'+site+'/3.dbo.config_event_mapping.sql', 'w')
for r in result_context:
    t.write(r+"\n")
#t.write(str(result_context)[1:-1])
t.close()