#  -*-  coding:  UTF-8  -*-
import oss2

def oss_putfile(context,region,bucketname,objectname,localfile):
    endpoint = 'oss-{0}.aliyuncs.com'.format(region)
    creds = context.credentials
    auth = oss2.StsAuth(creds.accessKeyId, creds.accessKeySecret, creds.securityToken)
    bucket = oss2.Bucket(auth, endpoint, bucketname)
    bucket.put_object_from_file(objectname, localfile)

def oss_putobject(context,region,bucketname,objectname,data):
    endpoint = 'oss-{0}.aliyuncs.com'.format(region)
    creds = context.credentials
    auth = oss2.StsAuth(creds.accessKeyId, creds.accessKeySecret, creds.securityToken)
    bucket = oss2.Bucket(auth, endpoint, bucketname)
    bucket.put_object(objectname,data)
