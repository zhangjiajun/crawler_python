#!/usr/bin/python
#coding:utf-8-

#  author:jiajun zhang <jzhang@suse.com>
#  time:2013-12-
#  target:just for python practise
#  language:python

from urllib import urlopen
import re


#f = file(r'1.html','r').read()
#f = urlopen('http://news.qq.com/a/20140325/022286.htm').read()
f = urlopen('http://view.news.qq.com/original/legacyintouch/d118.html').read()

pattern = re.compile(r"meta.name=.[Kk]eywords.*content=(.*?)>")
match = pattern.findall(f)
print "1",match
if isinstance(match[0],unicode):
	print match[0]
else:
	result=unicode(match[0],'gbk')
	print result
