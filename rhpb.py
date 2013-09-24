#!/usr/bin/env python2
import os
import sys
import urllib2
from urllib import urlencode

def buildData(to_post):
    data = {}
    login = os.getlogin()
    if login != 'root':  # Erm, lets be anonymous
        data['poster'] = login
    data['code2'] = to_post
    data['expiry'] = 'd' # 1 day
    data['format'] = 'text'  # Could probably modify this
    data['parent_pid'] = ''
    data['paste'] = 'Send'
    data['remember'] = '0'
    return urlencode(data)

encoded = buildData(sys.stdin.read())

request = urllib2.Request("http://pastebin.test.redhat.com/pastebin.php", data=encoded, headers={'Content-type': 'application/x-www-form-urlencoded'})
r = urllib2.urlopen(request)
print r.geturl()
