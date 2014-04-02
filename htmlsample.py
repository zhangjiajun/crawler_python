#!/usr/bin/python
# -*- coding: utf-8 -*-


#  author:jiajun zhang <jzhang@suse.com>
#  time:2013-12-
#  target:just for python practise
#  language:python

import HTMLParser,urllib2
import re,sys,os,string
import datetime

def domain_get(url_open):
	
	pattern = re.compile(r'https*://\w+?\.([\w\.]*)/*')
#	pattern = re.compile(r'https*://([\w\.]*)/*')
	domain = pattern.match(url_open)
	return domain.group(1)


def html_open(url_input):

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
				if name =='href' and "http" in value and domain in value:  
					self.links.append(value+"\n")
#					print value

if __name__=='__main__':
#	url_open = raw_input("Please input the url : \n")
	url_open=['http://www.sina.com.cn','http://news.qq.com','http://blog.csdn.net/tianzhu123/article/details/8187470','http://gd.sina.com.cn/news/s/2014-03-25/073689102.html','http://news.qq.com/a/20140325/013858.htm','http://news.sina.com.cn','http://blog.csdn.net/forgetbook/article/details/9080463']
	global domain
	example=url_open[0]
	domain = domain_get(example)
	print "url input:",example,'\n',"url domain:",domain
	Page = html_open(example)
	my = MyParser()
	my.feed(Page)
	fp=open("test.txt",'wb+')
	fp.writelines(my.links)
	fp_1=open("url_result.txt",'wb+')
	fp_1.truncate()
	fp_1.close()
#here input my.links to url_last

#	print type(my.links),my.links[100]
	for i in range(21,24,1):
		print datetime.datetime.now()
		Page_1=html_open(my.links[i])
		my_1=MyParser()
		my_1.feed(Page_1)
		fp_1=open("url_result.txt",'a')
		fp_1.writelines(my_1.links)
		
