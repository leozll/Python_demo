#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
import shutil



newsite=[]
newsite.append(['marykaychinaintouch','intouchweb'])
# newsite.append(['marykaychinaintouchwechat','intouchwechat'])
# newsite.append(['marykaychinamobileeshowcaseapp','eshowcase'])
# newsite.append(['marykaychina','chinacorp'])
for i in range(len(newsite)):
    site=newsite[i][0]
    sitepre = newsite[i][1]
    print(site,sitepre)
    if os.path.exists("result/" + site):
        shutil.rmtree("result/" + site)
    os.mkdir("result/" + site)

    os.system("python 1.config_column.py " + site)
    os.system("python 2.config_evar_prop_mapping.py " + site)
    os.system("python 3.config_event_mapping.py " + site)
    os.system("python 4.redshiftSchema.py " + site + " " + sitepre)

#site='marykaychinaintouch'
#sitepre='chinacorp'
# if os.path.exists("result/"+site):
#     shutil.rmtree("result/"+site)
# os.mkdir("result/"+site)
#
# os.system("python 1.config_column.py "+site)
# os.system("python 2.config_evar_prop_mapping.py "+site)
# os.system("python 3.config_event_mapping.py "+site)
# os.system("python 4.redshiftSchema.py "+site+" "+sitepre)

