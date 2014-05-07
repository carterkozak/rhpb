all:
	#make sure we have urllib2
	/usr/bin/env python2 -c "import urllib2"
	cp rhpb.py rhpb
clean:
	rm -rf *.pyo *.pyc rhpb
install: all
	sudo cp rhpb /usr/local/bin/
uninstall:
	sudo rm -f /usr/local/bin/rhpb
