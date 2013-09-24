all:
	#make sure we have urllib2
	/usr/bin/env python2 -c "import urllib2"
	cp rhpb.py rhpb
clean:
	rm -rf *.pyo *.pyc rhpb
install: all
	cp rhpb /usr/local/bin/
uninstall:
	rm -f /usr/local/bin/rhpb
