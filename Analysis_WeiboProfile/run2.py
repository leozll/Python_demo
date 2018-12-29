# -*- coding: utf-8 -*-
import logging
import datetime
import time
import sys
import os
import csv

sys.path.append(os.curdir + '/func/packages/')
from func.func_requestweiboprofile import *
from func.func_ossread import *
from func.func_ossappend import *
from func.func_ossput import *
from func.func_ossget import *
from func.func_sendmail import *

def handler(event, context):
    logger = logging.getLogger()
    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Start WeiboUid')
    print('--------------------------------------------------------------------------------------')
    tmpdir = '/tmp/weibo/'
    os.system("rm -rf /tmp/*")
    os.mkdir(tmpdir)
    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' tmpdir is ready')
    tmp_profile_list = tmpdir + 'weibo_profile_list.csv'

    # load parameters
    region = "cn-shanghai-internal"
    bucketname = "leo-demo"
    oss_brand_list = "configuration/weibo_brand_list"
    oss_profile_list = "configuration/weibo_profile_list.csv"
    oss_status = "configuration/weibo_status"
    analysis_count = 100

    # check last status
    status = oss_read(context, region, bucketname, oss_status)
    # if no status file, start from row 1
    if status == "ObjectNotExists":
        logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' This is first run...')
        analysis_start = 1
    else:
        # get the last status
        analysis_start = int(status.strip("\r\n"))

    #get last profile file
    oss_getfile(context, region, bucketname, oss_profile_list, tmp_profile_list)

    # request webi profile
    brand_list = oss_read(context, region, bucketname, oss_brand_list)
    # if no brand file, exit -1
    if brand_list == "ObjectNotExists":
        logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Brand file is missing!!!...')
        return -1
    else:
        # continue  from the last status
        analysis_list = brand_list.split("\r\n")[analysis_start - 1:analysis_start + analysis_count]
        if len(analysis_list)==0:
            logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' No keyword is to be analysed...')
            return 1
        else:
            logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' starting '+str(analysis_start)+'-'+str(analysis_start + analysis_count-1)+'...')
        for brnd_kw in analysis_list:
            # if the response is not abnormal
            profile_info = []
            profile_info.append(brnd_kw)
            try:
                time.sleep(1)
                profile_j = weibo_profile(brnd_kw)
                if profile_j["retcode"] != "000000":
                    print (profile_j)
                    profile_info.append(brnd_kw)
                    logger.info(
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '"' + brnd_kw + '"不存在!!!...：' + str(
                            profile_j['message']))
                else:
                    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' starting to analyse ' + brnd_kw + '...')
                    # extract the first search result
                    profile = profile_j['data'][0]

                    profile_info.append(profile['id'])
                    profile_info.append(profile['url'])
                    profile_info.append(profile['idVerifiedInfo'].replace("\n", ""))
                    profile_info.append(profile['friendCount'])
                    profile_info.append(profile['followCount'])
                    profile_info.append(profile['postCount'])
                    profile_info.append(profile['biography'].replace("\n", ""))
                    profile_info.append(profile['avatarUrl'])
                    profile_info.append(profile['fansCount'])
                    profile_info.append(profile['location'])
                    profile_info.append(profile['screenName'])
                    profile_info.append(profile['idVerified'])
                    profile_info.append(profile['viewCount'])
                    profile_info.append(profile['educations'])
                    profile_info.append(profile['birthday'])
                    profile_info.append(profile['likeCount'])
                    profile_info.append(profile['userName'])
                    profile_info.append(profile['idType'])
                    profile_info.append(profile['registerDate'])
                    profile_info.append(profile['gender'])
                    profile_info.append(profile['updateDate'])
                    profile_info.append(profile['works'])

                    # dict has no sequence
                    # for v in profile.values():
                    #    profile_info.append(v)

                with open(tmp_profile_list, 'a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(profile_info)

            except Exception  as e:
                profile_info.append(str(e))
                logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '"' + brnd_kw + '"解析失败????...：' + str(e))



        # oss_put(context, region, bucketname, oss_profile_list, tmp_profile_list)
        oss_putfile(context, region, bucketname, oss_profile_list, tmp_profile_list)
        oss_putobject(context, region, bucketname, oss_status, str(analysis_start + analysis_count))
        logger.info(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' finish ' + str(analysis_start) + '-' + str(
                analysis_start + analysis_count - 1) + '...')

        if analysis_start + analysis_count - len(brand_list.split("\r\n")) < analysis_count and analysis_start + analysis_count >= len(brand_list.split("\r\n")):
            logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' last keywords are analysed...')
            sub = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' last keywords are analysed...'
            content = "All the keywords are analysed！！"
            user_list = ['leo.zhai@bizfocus.cn']
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Start to send finish mail!')
            send_mail(user_list, sub, conten)

if __name__ == "__main__":
    handler('1', '2')
