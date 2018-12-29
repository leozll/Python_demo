import logging
import hashlib
import requests
import time
import datetime
import oss2
from lxml import etree
import urllib.request


def handler(event, context):
    data_limit = 20

    oss_csv_path = "process/weibo/weibo_csv/"
    oss_result_path = "result/weibo/html/"
    oss_imgs_path = "result/weibo/img/"
    logger = logging.getLogger()
    config_key = 'configuration/shenjian_weibo_status.json'
    region = "cn-hangzhou-internal"
    bucketname = "leo-hangzhou"
    endpoint = 'oss-{0}.aliyuncs.com'.format(region)
    creds = context.credentials
    auth = oss2.StsAuth(creds.accessKeyId, creds.accessKeySecret, creds.securityToken)
    bucket = oss2.Bucket(auth, endpoint, bucketname)

    user_key = 'NmExZDQ1Mm-6a1d452aa8'
    user_secret = 'OGQ5ZDFkZGU5OTVi-8d9d1dde995b94b'
    t = int(time.time())
    source_id = '2155369'
    sign_value = user_key + str(t) + user_secret
    sign = hashlib.md5(sign_value.encode()).hexdigest()

    weibo_config = bucket.get_object(config_key).read().decode('utf-8')
    weibo_config = eval(weibo_config)
    print(weibo_config)

    # if last run finished
    if weibo_config['current_status'] == 'finish':
        weibo_config_new = dict()
        weibo_config_new['current_cursor'] = 0
        weibo_config_new['current_status'] = 'running'
        weibo_config_new['unixtime_start'] = weibo_config['unixtime_end']
        weibo_config_new['unixtime_end'] = int(time.time())
        weibo_config_new['localtime_start'] = weibo_config['unixtime_start']
        weibo_config_new['localtime_end'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        weibo_config = weibo_config_new

    cursor = weibo_config['current_cursor']
    time_start = weibo_config['unixtime_start']
    time_end = weibo_config['unixtime_end']
    logger.info('------------------------- start ' + str(cursor) + ' ' + str(time_start) + str(time_end))
    # query_value = 'source(__id:{gt:%d},limit:20){data{},page_info{end_cursor,has_next_page}}' % (cursor)
    query_value = 'source(__id:{gt:%d},__time:{gte:%s,lt:%s},limit:%d,sort:"asc"){data{},page_info{end_cursor,has_next_page}}' % (
    int(cursor), str(time_start), str(time_end), data_limit)
    url = 'https://graphql.shenjian.io/?user_key=' + user_key + '&timestamp=' + str(
        t) + '&sign=' + sign + '&source_id=' + source_id + '&query=' + query_value
    r = requests.get(url)
    json = r.json()
    status = json['code']
    if status != 0:
        print(json['error_info'])
        exit - 1
    for d in json['result']['data']:
        logger.info('------------------------- get ' + d['url'])
        oss_html = d['url'].replace('http://m.weibo.cn/', oss_result_path) + '.html'
        csv_file = oss_csv_path + str(d['url']).replace('http://m.weibo.cn/', '')

        if bucket.object_exists(csv_file):
            logger.info('------------------------- ' + csv_file + ' is existing in the process folder!')
            continue

        content_list = []
        # if is_repost, get the original text, else original+repost
        pic_list = []
        if d['is_repost'] == 'true':
            origin_post_content = ' ' + etree.HTML(d['origin']['origin_post_content']).xpath('string(.)')
            imglist = d['origin']['origin_post_img']
            for img in imglist:
                if img[-3:] != 'gif':
                    pic = urllib.request.urlopen(img).read()
                    pic_path = img.replace('https:/', oss_imgs_path + str(d['userid']))
                    bucket.put_object(pic_path, pic)
                    pic_list.append(pic_path)
            h = repost_html((d['nickname'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(d['post_time']))),
                             d['source'], d['post_content'], d['origin']['origin_nickname'],
                             d['origin']['origin_post_content']
                             , ''.join(
                '<li><img src="' + '/' + s.replace('https:/', oss_imgs_path + str(d['userid'])) + '" alt=""></li>' for s
                in pic_list)
                             , time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(d['origin']['origin_post_time']))),
                             d['origin']['origin_source'], str(d['origin']['origin_attitudes_count']),
                             str(d['origin']['origin_comments_count']), str(d['origin']['origin_reposts_count']),
                             str(d['attitudes_count']), str(d['comments_count']), str(d['reposts_count'])))
        else:
            origin_post_content = ''
            imglist = d['pics']
            for img in imglist:
                if img[-3:] != 'gif':
                    pic = urllib.request.urlopen(img).read()
                    pic_path = img.replace('https:/', oss_imgs_path + str(d['userid']))
                    bucket.put_object(pic_path, pic)
                    pic_list.append('/' + pic_path)
            h = origin_html((d['nickname'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(d['post_time']))),
                             d['source'], d['post_content'], ''.join(
                '<li><img src="' + '/' + s.replace('https:/', oss_imgs_path + str(d['userid'])) + '" alt=""></li>' for s
                in pic_list), str(d['attitudes_count']), str(d['comments_count']), str(d['reposts_count'])))

        content_list.append(d['__id'])  # ID
        content_list.append(d['url'])  # url
        content_list.append(d['nickname'])  # title
        content_list.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(d['post_time']))))  # publish_time
        content_list.append('/' + oss_html)  # content_html_url
        # content_list.append(d['pics'])  #lst_img_url
        content_list.append(';'.join(pic_list))  # lst_img_url
        content_list.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))))  # insert_time
        content_list.append('微博')  # sub_source
        content_list.append(d['userid'])  # use_id
        content_list.append(d['nickname'])  # nickname
        content_list.append(d['follow_count'])  # follow_cnt
        content_list.append(d['followers_count'])  # followers_cnt
        content_list.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(d['post_time']))))  # post_time
        content_list.append(d['source'])  # post_source
        content_list.append(d['reposts_count'])  # reposts_cnt
        content_list.append(d['comments_count'])  # comments_cnt
        content_list.append(d['attitudes_count'])  # like_cnt
        content_list.append('Y' if d['isLongText'] == 'true' else 'N')  # islongtext
        content_list.append('Y' if d['is_repost'] == 'true' else 'N')  # is_repost
        content_list.append(d['post_content_txt'] + origin_post_content)  # content

        print(d['__id'])

        bucket.put_object(csv_file, '\u0000'.join(str(s) for s in content_list).replace('\n', '').replace('\r', ''))
        logger.info('------------------------- put to oss finished: ' + csv_file)
        bucket.put_object(oss_html, h)
        logger.info('------------------------- put to oss finished: ' + oss_html)
    weibo_config['current_cursor'] = json['result']['page_info']['end_cursor']
    if not json['result']['page_info']['has_next_page']:
        weibo_config['current_status'] = 'finish'
    logger.info('------------------------- finish ' + str(weibo_config))
    bucket.put_object(config_key, '{0}'.format(str(weibo_config)))


def origin_html(parms):
    h = '''
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Document</title>
	<link rel="stylesheet" href="/result/weibo/header/css/index.css">
	<link rel="stylesheet" type="text/css" href="/result/weibo/header/font/iconfont.css">
</head>
<body>
	<div class="main">
		<div class="main-contant">
			<div class="main-contant-list">
				<div class="main-contaning">
					<div class="WB_detail">
						<div class="WB_contain WB_containers">
							<div class="WB_info">
								<a href="javascript:;" class="nickName">%s</a>
							</div>
							<div class="WB_inform">
								<a href="javascript:;" class="time">%s</a>来自
								<a href="javascript:;" class="fromto">%s</a>
							</div>
							<div class="number">%s</div>
                            <div class="img-list">
								<div class="img-list-detail">
                                    <ul>
                                        %s
                                    </ul>
                                </div>
                            </div>
						</div>
						<div class="WB_like WB_contain">
							<div class="WB_handle">
								<ul>
									<li>
										<a href="javascript:void(0);">
											<span>
												<span>
													<img src="/result/weibo/header/css/like.png" alt="收藏">
													<!-- <em>转发</em> -->
													<em>%s</em>
												</span>
											</span>
										</a>
									</li>
									<li>
										<a href="javascript:void(0);">
											<span>
												<span>
													<img src="/result/weibo/header/css/comment.png" alt="评论">
													<!-- <em>评论</em> -->
													<em>%s</em>
												</span>
											</span>
										</a>
									</li>
									<li>
										<a href="javascript:void(0);">
											<span>
												<span>
													<img src="/result/weibo/header/css/share.png" alt="转发">
													<em>%s</em>
												</span>
											</span>
										</a>
									</li>
								</ul>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</body>
</html>
    ''' % parms
    return h


def repost_html(parms):
    h = '''
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Document</title>
	<link rel="stylesheet" href="/result/weibo/header/css/index.css">
	<link rel="stylesheet" type="text/css" href="/result/weibo/header/font/iconfont.css">
</head>
<body>
	<div class="main">
		<div class="main-contant">
			<div class="main-contant-list">
				<div class="main-contaning">
					<div class="WB_detail">
						<div class="WB_contain WB_containers">
							<div class="WB_info">
								<a href="javascript:;" class="nickName">%s</a>
							</div>
							<div class="WB_inform">
								<a href="javascript:;" class="time">%s</a>来自
								<a href="javascript:;" class="fromto">%s</a>
							</div>
							<div class="number">%s</div>
						</div>
						<div class="judge-zhuanfa">
							<div style="background-color: #f2f2f5;">
								<div class="WB_contain">
									<!-- 列表 -->
									<div class="WB_detail">
										<div class="WB_info">
											<a href="javascript:;" class="nickName">@%s</a>
										</div>
										<div class="number">%s</div>
										<div class="img-list">
											<div class="img-list-detail">
												<ul>
													%s
												</ul>
											</div>
										</div>
									</div>
									<div class="WB_likes">
										<div class="WB_inform">
											<a href="javascript:;" class="time">%s</a>来自
											<a href="javascript:;" class="fromto">%s</a>
										</div>
										<div class="WB_handle">
											<ul>
												<li>
													<a href="javascript:void(0);">
														<span>
															<span>
																<img src="/result/weibo/header/css/like1.png" alt="收藏">
																<!-- <em>转发</em> -->
																<em>%s</em>
															</span>
														</span>
													</a>
												</li>
												<li>
													<a href="javascript:void(0);">
														<span>
															<span>
																<img src="/result/weibo/header/css/comment1.png" alt="评论">
																<!-- <em>评论</em> -->
																<em>%s</em>
															</span>
														</span>
													</a>
												</li>
												<li>
													<a href="javascript:void(0);">
														<span>
															<span>
																<img src="/result/weibo/header/css/share1.png" alt="转发">
																<em>%s</em>
															</span>
														</span>
													</a>
												</li>
											</ul>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div class="WB_like WB_contain">
							<div class="WB_handle">
								<ul>
									<li>
										<a href="javascript:void(0);">
											<span>
												<span>
													<img src="/result/weibo/header/css/like.png" alt="收藏">
													<!-- <em>转发</em> -->
													<em>%s</em>
												</span>
											</span>
										</a>
									</li>
									<li>
										<a href="javascript:void(0);">
											<span>
												<span>
													<img src="/result/weibo/header/css/comment.png" alt="评论">
													<!-- <em>评论</em> -->
													<em>%s</em>
												</span>
											</span>
										</a>
									</li>
									<li>
										<a href="javascript:void(0);">
											<span>
												<span>
													<img src="/result/weibo/header/css/share.png" alt="转发">
													<em>%s</em>
												</span>
											</span>
										</a>
									</li>
								</ul>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</body>
</html>
    ''' % parms
    return h

