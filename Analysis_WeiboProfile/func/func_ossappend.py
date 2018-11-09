#  -*-  coding:  UTF-8  -*-
import oss2

def oss_append(context,region,bucketname,objectname,data):
    endpoint = 'oss-{0}.aliyuncs.com'.format(region)
    creds = context.credentials
    auth = oss2.StsAuth(creds.accessKeyId, creds.accessKeySecret, creds.securityToken)
    bucket = oss2.Bucket(auth, endpoint, bucketname)
    if bucket.object_exists(objectname):
        bucket.append_object(objectname,1, data)
    else :
        bucket.append_object(objectname,0, data)