#!/usr/bin/python
#coding:utf-8-

#  author:jiajun zhang <jzhang@suse.com>
#  time:2013-12-
#  target:just for python practise
#  language:python

import HTMLParser,urllib
import re,sys,os,string

result_first = []

class MyParser(HTMLParser.HTMLParser):
	def __init__(self):
		HTMLParser.HTMLParser.__init__(self)
		self.links = []

	def handle_starttag(self,tag,attrs):

		if tag == 'a':
			#judge <a>  
			for name,value in attrs:
				if name =='href':  
					self.links.append(value+"\n")
#					print value

if __name__=='__main__':
#	url_input = raw_input("Please input the url : \n")
#	url_open = 'http://'+ url_input
	url_open="http://www.qq.com.cn"
	Page = urllib.urlopen(url_open).read()
	my = MyParser()
	my.feed(Page)
	fp=open("test.txt",'wb+')
	fp.writelines(my.links)

