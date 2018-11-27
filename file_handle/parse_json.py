# -*- coding: utf-8 -*-

import datetime
import os
str_time = datetime.datetime.now().strftime('%Y-%m-%d')
work_dir = 'D:\\Project\\Aliyun\\parse\\weibo_json'
target_file = 'D:\\Project\\Aliyun\\parse\\weibo{0}.csv'.format(str_time)
docList = []
for parent, dirnames, filenames in os.walk(work_dir,  followlinks=True):
    for filename in filenames:
        file_path = os.path.join(parent, filename)
        docList.append(file_path)

print (len(docList))
a = 1
for i in docList:
    #print (i)
    print (str(a)+'/'+str(len(docList)))
    #read the file
    #print (bucket.get_object(json_key).read().decode('utf-8'))
    content_str = open(i, 'r',encoding='utf-8').read()
    content = eval(content_str)
    content_list = []
    content_list.append((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'))
    content_list.append(content['from']['id'])  # uid
    content_list.append(content['id'])  # 文章id
    content_list.append(content['url'])  # 文章链接
    content_list.append(content['mblog']['localPublishDateStr'])  # 发布时间／北京时间
    if 'edit_at' in content:
        content_list.append(content['edit_at'])  # 最后编辑时间
    else:
        content_list.append('')
    content_list.append(content['shareCount'])  # 转发数
    content_list.append(content['commentCount'])  # 评论数
    content_list.append(content['likeCount'])  # 点赞数
    content_list.append(content['content'].replace("\n", "").replace(",", "，"))  # 文章内容
    content_list.append(content['mblog']['source'])  # 来自
    if content['imageURLs'] is not None:
        content_list.append(';'.join(content['imageURLs']))  # 图片链接
    else:
        content_list.append('')
    if 'retweeted_status' in content['mblog']:
        content_list.append(content['mblog']['retweeted_status']['user']['id'])  # 转发作者uid
        content_list.append(content['mblog']['retweeted_status']['id'])  # 转发文章id
        content_list.append(content['mblog']['retweeted_status']['created_at'])  # 转发文章发布时间
        content_list.append(content['mblog']['retweeted_status']['text'].replace("\n", "").replace(",", "，"))  # 转发内容
        content_list.append(content['mblog']['retweeted_status']['reposts_count'])  # 转发文章转发数
        content_list.append(content['mblog']['retweeted_status']['comments_count'])  # 转发文章评论数
        content_list.append(content['mblog']['retweeted_status']['attitudes_count'])  # 转发文章点赞数
        if content['mblog']['retweeted_status']['pic_urls'] is not None:
            if content['mblog']['retweeted_status']['pic_urls'] != []:
                content_list.append(';'.join(
                    list(content['mblog']['retweeted_status']['pic_urls'][0].values())))  # 转发内容图片
            else:
                content_list.append('')
        else:
            content_list.append('')
        content_list.append(content['mblog']['retweeted_status']['source'])  # 转发文章来自
    else:
        content_list.append('')
        content_list.append('')
        content_list.append('')
        content_list.append('')
        content_list.append('')
        content_list.append('')



    #csv_file = i.replace('json','csv')
    #if not os.path.exists(os.path.dirname(csv_file)):
    #    os.makedirs(os.path.dirname(csv_file))
    with open(target_file, 'a+',encoding='utf-8') as f:
        f.write(",".join('%s' %id for id in content_list)+'\n')
    a = a+1


print ('Congratulations')