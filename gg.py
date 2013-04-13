#!/usr/bin/env python


import base64, hashlib, urllib, subprocess, sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-D", "--debug", action="store_true", dest="d_debug", help="debug mode")
parser.add_option("-s", "--save", dest="d_save", help="url to save")
parser.add_option("-f", "--find", dest="d_find", help="url to find")
parser.add_option("-d", "--download", dest="d_download", help="url to lxd")
parser.add_option("-a", "--add", dest="d_add", help="url to lx add")


(options, args) = parser.parse_args()

API_ENDPOINT = 'http://pahud.net/gg/'

def save(x, p=False):
	try:
		h = urllib.urlopen( API_ENDPOINT+'save/'+ base64.b64encode(x) ).read()
		if p: print h.strip()
		return h.strip()
	except Exception, e:
		print('failed to save, ', e)
		return None

def find(x, p=False):
	try:
		h = urllib.urlopen( API_ENDPOINT+'find/'+ x ).read()
		if p: print base64.b64decode(h)
		return base64.b64decode(h)
	except:
		print('failed to find')
		return None

def lxadd(x):
	p = subprocess.Popen('lx add "%s"' % (x), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(stdout, stderr) = p.communicate()
	return (stdout, stderr)

def lxd(x):
	p = subprocess.Popen('screen -d -m lx download --tool=aria2 --continue "%s"' % (x), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	return p


def add(x):
	if x.startswith('magnet:') or x.startswith('bt://') or x.startswith('ed2k://'):
		save(x, p=True)
		lxadd(x)
	else:
		found = find(x)
		if found:
			lxadd(found)

def main():
	if options.d_save:
		save(options.d_save, p=True)
	elif options.d_find:
		find(options.d_find, p=True)
	elif options.d_add:
		add(options.d_add)
	elif options.d_download:
		x = options.d_download
		found = find(x)
		if found:
			lxd(found)
		elif x.isdigit() and len(x)==12:
			lxd(x)
		else:
			print('[ERROR] resource not found')
	else:
		parser.print_help()
		sys.exit(1)


if __name__ == '__main__':
	sys.exit(main())


