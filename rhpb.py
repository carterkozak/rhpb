#!/usr/bin/env python2
import os
import sys
import urllib2
from urllib import urlencode

def print_usage():
    '''
    Always print usage to stderr, we never want it piped into an output file
    '''
    sys.stderr.write("Usage:\nrhpb reads stdin untill EOF and prints the pastebin link\n" +
            "  EX: $ cat foo.txt | rhpb\n" +
            "  http://pastebin.test.redhat.com/{id}\n" +
            "rhpb will can dump a posted pastebin to stdout given the id or url\n" +
            "  EX: $ rhpb http://pastebin.test.redhat.com/{id}\n" +
            "  Hello, World!\n")

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

def post():
    encoded = buildData(sys.stdin.read())

    request = urllib2.Request("http://pastebin.test.redhat.com/pastebin.php",
            data=encoded, headers={'Content-type': 'application/x-www-form-urlencoded'})
    r = urllib2.urlopen(request)
    print r.geturl()

def fetch():
    try:
        arg = str(int(sys.argv[1].split('/')[-1]))
        f = urllib2.urlopen('http://pastebin.test.redhat.com/pastebin.php?dl=%s' % arg)
        print f.read().replace('\r', '') # Because we don't use dos...
        f.close()
    except:
        # Could probably do some better exception handling for
        # network exceptions
        print_usage()

arglen = len(sys.argv)
if arglen == 1:
    post()
elif arglen == 2:
    fetch()
else:
    print_usage()
