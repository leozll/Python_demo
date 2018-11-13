#  -*-  coding:  UTF-8  -*-
import oss2

def oss_getfile(context,region,bucketname,objectname,localfile):
    endpoint = 'oss-{0}.aliyuncs.com'.format(region)
    creds = context.credentials
    auth = oss2.StsAuth(creds.accessKeyId, creds.accessKeySecret, creds.securityToken)
    return oss2.Bucket(auth, endpoint, bucketname)


