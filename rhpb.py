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

def page(text):
    if hasattr(os, 'system') and os.system('(less) 2>/dev/null') == 0:
        # -F closes when text cal all be displayed
        # -X will not clear the screen upon exit (like git log)
        pipe = os.popen("less -F", 'w')
        try:
            pipe.write(text)
            pipe.close()
        except IOError:
            # Broken pipe
            pass
    else:
        print text

def buildData(to_post):
    data = {}
    login = os.getlogin()
    data['poster'] = login if login != 'root' else 'user'
    data['code2'] = to_post
    data['expiry'] = 'd' # 1 day
    data['format'] = 'text'  # Could probably modify this
    data['parent_pid'] = ''
    data['paste'] = 'Send'
    data['remember'] = '0'
    return urlencode(data)

def post():
    try:
        encoded = buildData(sys.stdin.read())

        request = urllib2.Request("http://pastebin.test.redhat.com/pastebin.php",
                data=encoded, headers={'Content-type': 'application/x-www-form-urlencoded'})
        r = urllib2.urlopen(request)
        print r.geturl()
    except KeyboardInterrupt:
        sys.stderr.write("Caught SIGINT, exiting.\n")

def fetch():
    arg = None
    try:
        arg = str(int(sys.argv[1].split('/')[-1]))
        f = urllib2.urlopen('http://pastebin.test.redhat.com/pastebin.php?dl=%s' % arg)
        page(f.read().replace('\r', '')) # Because we don't use dos...
        f.close()
    except urllib2.HTTPError, he:
        if he.code == 404:
            sys.stderr.write("Invalid pastebin ID: '%s'\n" % arg)
        else:
            sys.stderr.write("Network issue: %s\n" % he)
    except:
        print_usage()

arglen = len(sys.argv)
if arglen == 1:
    post()
elif arglen == 2:
    fetch()
else:
    print_usage()
