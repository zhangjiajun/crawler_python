#!/usr/bin/python
#coding:utf-8-

#  author:jiajun zhang <jzhang@suse.com>
#  time:2013-12-
#  target:just for python practise
#  language:python

import urllib,urllib2
import re
import sys,os,string
#-----------------------------source page open-------------------------

args = sys.argv[1:]
def help():
	print "Usage: %s + Url" %sys.argv[0]

url_input = raw_input("Please input the Url  :\n ")
url_open = 'http://' +url_input
Hash_table = []

Page_open = urllib.urlopen(url_open).read()

