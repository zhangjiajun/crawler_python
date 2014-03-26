#!/usr/bin/python
# -*- coding: utf-8 -*-


#  author:jiajun zhang <jzhang@suse.com>
#  time:2013-12-
#  target:just for python practise
#  language:python

import urllib2
import re,os,sys
import HTMLParser
def a(url_input):

	headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11(KHTML,like Gecko) Chrome/23.0.1271.64 Safari/537.11',
#		'Accept':'text/html;q=0.9,*/*;q=0.8',
#		'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#		'Accept-Encoding':'gzip',
#		'Connection':'close',
#		'Referer':None
				}
#	req_timeout =5

	req = urllib2.Request(url_input,headers=headers)
	Page= urllib2.urlopen(req).read()
	return Page

class MyParser(HTMLParser.HTMLParser):
	def __init__(self):
		HTMLParser.HTMLParser.__init__(self)
		self.links = []

	def handle_starttag(self,tag,attrs):

		if tag == 'a':
			#judge <a>  
			for name,value in attrs:
				if name =='href' and "http" in value:  
					self.links.append(value+"\n")
#					print value


if __name__=='__main__':
	url_open="http://blog.csdn.net/nevasun/article/details/7331644"
	Page=a(url_open)
	fp=open("test.txt",'wb+')
	fp.writelines(Page)
	my = MyParser()
	my.feed(Page)
	fp=open("test.txt",'wb+')
	fp.writelines(my.links)
