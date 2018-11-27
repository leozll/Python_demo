# -*- coding: utf-8 -*-
import os
import datetime

str_time = datetime.datetime.now().strftime('%Y-%m-%d')
work_dir = 'D:\\Project\\Aliyun\\weibo\\process\\weibo_csv'
target_file = 'D:\\Project\\Aliyun\\weibo{0}.csv'.format(str_time)

docList = []
for parent, dirnames, filenames in os.walk(work_dir,  followlinks=True):
    for filename in filenames:
        file_path = os.path.join(parent, filename)
        docList.append(file_path)

print (len(docList))

fname = open(target_file, "w")  # 创建一个以当前时间命名的log文件
a=1
for i in docList:
    print (a)
    x = open(i, 'r',encoding='utf-8')  # 打开列表中的文件,读取文件内容
    #fname.write(x.read())
    with open(target_file, 'a',encoding='utf-8') as f:
        f.write(x.read()[1:-1]+'\n')
    x.close()  # 关闭列表文件
    a=a+1

#fname.close()
