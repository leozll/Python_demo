#  -*-  coding:  UTF-8  -*-
import oss2

def oss_read(context,region,bucketname,objectname):
    endpoint = 'oss-{0}.aliyuncs.com'.format(region)
    creds = context.credentials
    auth = oss2.StsAuth(creds.accessKeyId, creds.accessKeySecret, creds.securityToken)
    bucket = oss2.Bucket(auth, endpoint, bucketname)
    if bucket.object_exists(objectname):
        content = bucket.get_object(objectname)
        data = content.read()
        return (data.decode('utf-8'))
    else :
        return ('ObjectNotExists')