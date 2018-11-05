#!/usr/bin/env python
# -*- coding:utf8 -*-
import json
import xlrd
import sys

site=sys.argv[1]
# site='marykaychinaintouch'

config_file="./metadata/2.dbo.config_evar_prop_mapping.json"
with open(config_file) as json_file:
    jasonData = json.load(json_file)
pvsource = list(jasonData['PV'])

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
pv.sort()

#sort the prop columns
for i in range(len(pv)):
    pv_seq[pv[i]]=i + 1

result_context=[]
#generate the data for config_evar_prop_mapping
for r in range(sh.nrows):
    if sh.row(r)[0].value==site and (sh.row(r)[1].value[0:4]=='prop' or sh.row(r)[1].value[0:4]=='eVar'):
        sitecolumn="'"+site+"'"
        OrginalColumn="'"+sh.row(r)[1].value+"'"
        BusinessName="'"+''.join(sh.row(r)[2].value.split())+"'"
        StartTime="CAST(N'2010-01-01 00:00:00.000' AS DateTime)"
        EndTime="CAST(N'2010-01-01 00:00:00.000' AS DateTime)"
        if sh.row(r)[1].value[0:4]=='prop':
            EventColumn=str(pv_seq[''.join(sh.row(r)[2].value.split())])
            PVColumn=str(pv_seq[''.join(sh.row(r)[2].value.split())])
            PVSource="'"+jasonData['PV'].get(''.join(sh.row(r)[2].value.split()), 'prop_'+''.join(sh.row(r)[2].value.split())).replace("'","''")+"'"
            PVTarget="'"+''.join(sh.row(r)[2].value.split())+"'"
        else:
            EventColumn="NULL"
            PVColumn="NULL"
            PVSource="NULL"
            PVTarget = "NULL"
        sql="INSERT INTO [dbo].[config_evar_prop_mapping] ([Site], [OrginalColumn], [BusinessName], [StartTime], [EndTime], [EventColumn], [PVColumn], [PVSource], [PVTarget]) VALUES (" + sitecolumn + "," + OrginalColumn+ "," + BusinessName+ ", CAST(N'2010-01-01 00:00:00.000' AS DateTime), CAST(N'2999-01-01 00:00:00.000' AS DateTime)," + EventColumn+ "," + PVColumn+ "," + PVSource+ "," + PVTarget + ");"
        result_context.append(sql)

#write the metadata for config_columns
t = open('result/'+site+'/2.dbo.config_evar_prop_mapping.sql', 'w')
for r in result_context:
    t.write(r+"\n")
#t.write(str(result_context)[1:-1])
t.close()