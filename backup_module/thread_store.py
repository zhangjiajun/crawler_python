#!/usr/bin/python
#coding:utf-8-

#  author:jiajun zhang <jzhang@suse.com>
#  time:2014-04-06
#  target:crawler for website information
#  language:python

import urllib2,socket
import re,sys,os,string
import Queue,threading
import MySQLdb,time,datetime

#------ founction init crawler-----
def crawler_init():
	global domain,deep_crawler,queue,queue_page,links,sleep_time,time_join,time_out,thread_num,thread_number
	links = []
	queue = Queue.Queue()
	queue_page = Queue.Queue()
	deep_crawler = 2
	sleep_time = 0.1
	time_out = 20
	time_join = 6
	thread_num = 8
	thread_number = 8
	
#------ founction get domain-----
def domain_get(url_open):
	
	pattern = re.compile(r'https*://\w+?\.([\w\.]*)/*')
	domain_1 = pattern.match(url_open)
	domain =  domain_1.group(1)
	return domain

#------ founction get link-----
def link_get(url_open):
	Page = html_open(url_open)
	pattern = re.compile("href=\"(.+?)\"")
	link_1 = pattern.findall(Page)
	for link in link_1:
		if "http" in link and domain in link and "auto" not in link and "java" not in link:
			links.append(link+'\n')
	
#-------founction make httpheaders and open html ---------
def html_open(url_input):

	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11(KHTML,like Gecko) Chrome/23.0.1271.64 Safari/537.11',
				}

#	urllib2.socket.setdefaulttimeout(time_out)
	time.sleep(sleep_time)
	req = urllib2.Request(url_input,headers=headers)
	con = urllib2.urlopen(req)
	time.sleep(0.5)
	status_html = con.getcode()
	if status_html != 200:
		error_link = url_input+"error"
		return error_link 
	else:
		Page = con.read()
		return Page
	con.close()

#---use thread to get page----

def page_store(url_open):
	store_page = html_open(url_open)
#	print store_page
	time.sleep(sleep_time)
	store_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
	store_name = str(store_time) + ".txt"
	fp_store = open("./B/%s" % store_name,'wb+')
	fp_store.writelines(store_page)
	time.sleep(sleep_time)
	fp_store.close()

class Thread_page(threading.Thread):
	def __init__(self,t_name):
		threading.Thread.__init__(self,name=t_name)
	def run(self):
		global count_page
		while queue_page.qsize():
			url_open=queue_page.get()
			try:
				count_page +=1
				page_store(url_open)
				print "page_store(url_open)"
			finally:
				queue_page.task_done()

def thread_gogo(num):
	for i in range(0,num):
		t_name="thread_%3s" %i
		t =Thread_page(t_name)
		t.start()
	for i in range(0,num):
		t_name="thread_%3s" %i
		t.join(time_join)

#-----------main founction ------------------------
if __name__=='__main__':
#	url_open = raw_input("Please input the url : \n")
	url_open=['http://www.sina.com.cn','http://news.qq.com','http://blog.csdn.net/tianzhu123/article/details/8187470','http://gd.sina.com.cn/news/s/2014-03-25/073689102.html','http://news.qq.com/a/20140325/013858.htm','http://news.sina.com.cn','http://blog.csdn.net/forgetbook/article/details/9080463','http://sports.sina.com.cn/']

	count = 0
	count_page = 0
	example = url_open[0]
	crawler_init()

	time_start = datetime.datetime.now()
	print time_start
	domain = domain_get(example)
	print "url input: ",example,'\n',"url domain: ",domain

	Page = html_open(example)
#	fp = open("test.txt",'wb+')
	store_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
	store_name = str(store_time) + ".txt"
	fp = open("./%s" % store_name,'wb+')
#	fp = open("store_name",'wb+')
	fp.writelines(Page)
	time.sleep(1)
	fp.close()
#-------store url source Page---------	
	for i in url_open:
		queue_page.put(i)
	print	queue_page.qsize()
	thread_gogo(thread_number)

	print "loop_page is ",count_page
	time_end = datetime.datetime.now()
	print time_end
	print "time use: %s " %(time_end-time_start)
