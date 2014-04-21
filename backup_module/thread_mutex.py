#!/usr/bin/python
#coding:utf-8-

#  author:jiajun zhang <jzhang@suse.com>
#  time:2014-04-06
#  target:crawler for website information
#  language:python

import HTMLParser,urllib2,urlparse
import BeautifulSoup
import re,sys,os,string
import datetime,time

import Queue
import threading

#-------founction make httpheaders and open html ---------
def html_open(url_input):

	headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11(KHTML,like Gecko) Chrome/23.0.1271.64 Safari/537.11',
				}

	req = urllib2.Request(url_input,headers=headers)
	con = urllib2.urlopen(req)
	Page = con.read()
	
	return Page

#------founction get title and keyword ----------
def title_get(Page):
	
	soup= BeautifulSoup.BeautifulSoup(Page,fromEncoding="gb18030")
	title= unicode(soup.title)
	print title[7:-8]

#------founction deal with html ----------
def html_deal(url_input):

	Page_1=html_open(url_input)
	title_get(Page_1)
	print url_input

#---use thread to get information----
class Thread_url(threading.Thread):
	def __init__(self,t_name):
		threading.Thread.__init__(self,name=t_name)
	def run(self):
		global count
		while queue.qsize():
			url_open=queue.get()
			count +=1
			html_deal(url_open)
			queue.task_done()

def thread_go(num):
	for i in range(0,num):
		t_name="thread_%s" %i
		t =Thread_url(t_name)
		t.start()
	for i in range(0,num):
		t_name="thread_%s" %i
		t.join()
	

if __name__=='__main__':
	url_open=['http://www.sina.com.cn','http://news.qq.com','http://blog.csdn.net/tianzhu123/article/details/8187470','http://gd.sina.com.cn/news/s/2014-03-25/073689102.html','http://news.qq.com/a/20140325/013858.htm','http://news.sina.com.cn','http://blog.csdn.net/forgetbook/article/details/9080463','http://sports.sina.com.cn/']
	time_1= datetime.datetime.now()
	print "time start: ",time_1
	print "crawler staring ..."
	global queue
	count =0
	queue=Queue.Queue()
	for i in url_open:
		queue.put(i)
#	t= Thread_url(queue)
#	t.start()
	thread_go(8)
	time.sleep(2)
	print "count=",count
	time_2= datetime.datetime.now()
	print "time end: ",time_2
	print "time use: %s " %(time_2-time_1)
