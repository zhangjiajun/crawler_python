#!/usr/bin/python
#coding:utf-8-

#  author:jiajun zhang <jzhang@suse.com>
#  time:2014-04-06
#  target:crawler for website information
#  language:python

import HTMLParser,urllib2,urlparse
import BeautifulSoup
import re,sys,os,string
import datetime,Queue,threading

#---use thread to get information----
class Thread_url(threading.Thread):
	def __init__(self,queue):
		threading.Thread.__init__(self)
		self.queue=queue
	def run(self):
		while True:
			url_open=self.queue.get()
			Page=html_open(url_open)
			get_title_keyword(Page)
			#sent a singal when task done
			self.queue.task_done()

#-------founction make httpheaders and open html ---------
def html_open(url_input):

	headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11(KHTML,like Gecko) Chrome/23.0.1271.64 Safari/537.11',
				}

	req = urllib2.Request(url_input,headers=headers)
	con = urllib2.urlopen(req)
	Page = con.read()
	
	return Page

#------founction get title and keyword ----------
def get_title_keyword(Page):
	
	soup= BeautifulSoup.BeautifulSoup(Page,fromEncoding="gb18030")
	title= unicode(soup.title)
	print title[7:-8],type(title[8])

#	keyword=soup.findAll('meta',attrs={"name":"keywords"})
#	print keyword,type(keyword)

if __name__=='__main__':
	url_open=['http://www.sina.com.cn','http://news.qq.com','http://blog.csdn.net/tianzhu123/article/details/8187470','http://gd.sina.com.cn/news/s/2014-03-25/073689102.html','http://news.qq.com/a/20140325/013858.htm','http://news.sina.com.cn','http://blog.csdn.net/forgetbook/article/details/9080463','http://sports.sina.com.cn/']
	time_1= datetime.datetime.now()
	print "time start: ",time_1
	print "crawler staring ..."
	queue=Queue.Queue()
	for i in url_open:
		queue.put(i)
	t =Thread_url(queue)
	t.setDaemon(True)
	t.start()
	queue.join()
	time_2= datetime.datetime.now()
	print "time end:",time_2
	print "time use: %s " %(time_2-time_1)
