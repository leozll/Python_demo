#!/usr/bin/env python
# -*- coding:utf8 -*-
import xlrd
import sys

site=sys.argv[1]
sitepre=sys.argv[2]
# site='marykaychinaintouch'
# sitepre='chinacorp'

wb = xlrd.open_workbook('./metadata/mapping.xlsx')
#open the first sheet
sh=wb.sheet_by_index(0)

#read the prop columns
pv=[]
for r in range(sh.nrows):
    if sh.row(r)[0].value==site and (sh.row(r)[1].value[0:4]=='prop'):
        pv.append('\tprop_'+''.join(sh.row(r)[2].value.split())+' VARCHAR(255) ENCODE zstd,\n')
pv.sort()
propcolumns=''.join(pv)[:-1]

#read the evar columns
pv=[]
for r in range(sh.nrows):
    if sh.row(r)[0].value==site and (sh.row(r)[1].value[0:4]=='evar'):
        pv.append('\tevar_'+''.join(sh.row(r)[2].value.split())+' VARCHAR(255) ENCODE zstd,\n')
pv.sort()
evarcolumns=''.join(pv)[:-1]

#read the business columns
pv=[]
for r in range(sh.nrows):
    if sh.row(r)[0].value==site and (sh.row(r)[1].value[0:4]=='prop'):
        pv.append('\t'+''.join(sh.row(r)[2].value.split())+' VARCHAR(255) ENCODE zstd,\n')
pv.sort()
businesscolumns=''.join(pv)[:-1]



#read the metadata for config_columns
with open('metadata/4.redshift.sql', mode='r', encoding='utf-8') as s:
    result_context=s.read().replace('propcolumns',propcolumns).replace('evarcolumns',evarcolumns).replace('businesscolumns',businesscolumns).replace('sitepre',sitepre)
s.close()


#write the metadata for config_columns
t = open('result/'+site+'/4.redshift.sql', 'w')
t.write(result_context+"\n")
t.close()


