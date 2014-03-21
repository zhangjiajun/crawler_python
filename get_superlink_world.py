#!/usr/bin/python
#coding:utf-8-

#  author:jiajun zhang <jzhang@suse.com>
#  time:2013-12-
#  target:just for python practise
#  language:python

import urllib,re

s1=[]
url='http://www.sina.com.cn'

Page = urllib.urlopen(url).read()
s1=re.findall("a\shref=\"(.*).*>(.*)</a>",Page)

print "合理咯："
