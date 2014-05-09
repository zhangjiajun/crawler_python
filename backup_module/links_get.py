#!/usr/bin/python
# -*- coding: utf-8 -*-


#  author:jiajun zhang <jzhang@suse.com>
#  time:2013-12-
#  target:just for python practise
#  language:python

import HTMLParser,urllib2,urlparse
import re,sys,os,string
import datetime,time

def domain_get(url_open):
	
	pattern = re.compile(r'https*://\w+?\.([\w\.]*)/*')
	domain_1 = pattern.match(url_open)
#	host=urlparse.urlparse(example)
#	domain = host.hostname
	domain = domain_1.group(1)
	return domain


def link_get(url_open):
	Page = html_open(url_open)
	pattern = re.compile("href=\"(.+?)\"")
	link_1 = pattern.findall(Page)
	for link in link_1:
		if "http" in link and domain in link:
			if link not in links:
				links.append(link+'\n')
	

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

if __name__=='__main__':
#	url_open = raw_input("Please input the url : \n")
	url_open=['http://www.sina.com.cn','http://news.qq.com','http://blog.csdn.net/tianzhu123/article/details/8187470','http://gd.sina.com.cn/news/s/2014-03-25/073689102.html','http://news.qq.com/a/20140325/013858.htm','http://news.sina.com.cn','http://blog.csdn.net/forgetbook/article/details/9080463','http://sports.sina.com.cn/']
	global domain,links
	links = []
	example=url_open[0]
	domain = domain_get(example)
	print "url input:",example,'\n',"url domain:",domain
	
	Page = html_open(example)
	fp=open("./B/test.txt",'wb+')
	fp.writelines(Page)
	time.sleep(1)
	fp.close()

	link_get(example)
	f_1 = datetime.datetime.now()
	f_2 = str(datetime.datetime.now())+".txt"
	fp_1=open("./B/%s" % f_2,'wb+')
	fp_1.truncate()
	fp_1.writelines(links)
	time.sleep(1)
	fp_1.close()
