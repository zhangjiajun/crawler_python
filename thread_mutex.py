#!/usr/bin/python
#coding:utf-8-

#  author:jiajun zhang <jzhang@suse.com>
#  time:2014-04-06
#  target:crawler for website information
#  language:python

import HTMLParser,urllib2,urlparse
import BeautifulSoup
import re,sys,os,string
import datetime

from Queue import Queue
from threading import Thread,Lock

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

#---use thread to get information----
class Thread_url:
	def __init__(self,threads):
		# lock thread
		self.lock=Lock()
		self.q_req=Queue()
		self.q_ans=Queue()
		for i in range(threads):
			t=Thread(target=self.thread_start)
			t.setDaemon(True)
			t.start()
		self.running=0
	def push(self,queue):
		self.q_req.put(queue)
	def pop(self):
		return self.q_ans.get()
	def thread_start(self):
		url_open=self.q_req.get()
		Page=html_open(url_open)
		get_title_keyword(Page)
		#sent a singal when task done
		self.q_req.task_done()


if __name__=='__main__':
	url_open=['http://www.sina.com.cn','http://news.qq.com','http://blog.csdn.net/tianzhu123/article/details/8187470','http://gd.sina.com.cn/news/s/2014-03-25/073689102.html','http://news.qq.com/a/20140325/013858.htm','http://news.sina.com.cn','http://blog.csdn.net/forgetbook/article/details/9080463','http://sports.sina.com.cn/']
	time_1= datetime.datetime.now()
	print "time start: ",time_1
	print "crawler staring ..."
	queue=Queue()
	for i in url_open:
		queue.put(i)
#		print queue.qsize()
	t =Thread_url(4)
	t.push(queue)
	time_2= datetime.datetime.now()
	print "time end: ",time_2
	print "time use: %s " %(time_2-time_1)
