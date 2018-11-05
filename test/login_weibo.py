#!/usr/bin/python

import webbrowser
import weibo
#from weibo.auth import OAuthHandler
#from weibo.api import API
#
AppKey = 'z_llong@163.com'
AppSecret = 'zllong145511'

my_auth = OAuthHandler(AppKey , AppSecret)
webbrowser.open(my_auth.get_authorization_url())
verifier = raw_input('PIN: ').strip()
my_auth.get_access_token(verifier)

my_api = API(my_auth)
for comment in my_api.mentions():
    object = comment
    id = object.__getattribute__("id")
    text = object.__getattribute__("text")
    print str(id) + " : " + text

