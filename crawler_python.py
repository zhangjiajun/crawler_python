#!/usr/bin/python
#coding:utf-8-

#  author:jiajun zhang <jzhang@suse.com>
#  time:2014-04-06
#  target:crawler for website information
#  language:python

import HTMLParser,urllib2,urlparse
import BeautifulSoup,socket
import re,sys,os,string
import datetime,time
import codecs,sqlite3 
import Queue,threading
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
		if "http" in link and domain in link:
			if link not in links:
				links.append(link+'\n')
	
#-------founction make httpheaders and open html ---------
def html_open(url_input):

	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11(KHTML,like Gecko) Chrome/23.0.1271.64 Safari/537.11',
				}

#	socket.setdefaulttimeout(time_out)
	time.sleep(sleep_time)
	req = urllib2.Request(url_input,headers=headers)
	con = urllib2.urlopen(req)
	Page = con.read()
	con.close()
	
	return Page

#------founction get title ----------
def title_get(url_input):
	Page = html_open(url_input)	
	soup = BeautifulSoup.BeautifulSoup(Page,fromEncoding="gb18030")
	title = unicode(soup.title)

	reload(sys)
	sys.setdefaultencoding("utf-8")
	title_url = str(title[7:-8]).encode("utf-8")

	return title_url

#------founction init ----------
def crawler_init():

	global domain,queue,links,sleep_time,time_out,thread_num
	links = []
	queue = Queue.Queue()
	sleep_time = 0.1
	time_out = 20
	thread_num = 18 

	global db,cursor,drop_table_sql,create_table_sql,insert_sql,select_sql
	db='test.db'
	conn=sqlite3.connect(db)
	cursor=conn.cursor()
	drop_table_sql="drop table if exists web_information"
	create_table_sql="""
	create table web_information(
		id integer primary key autoincrement unique not null,
		url text not null,
		title text not null
	);
	"""
	insert_sql="insert into web_information (url,title) values(?,?)"
	select_sql="SELECT * FROM web_information"

	cursor.execute(drop_table_sql)

#------founction deal with html ----------
def html_deal(url_input):
	title_1=title_get(url_input)
	cursor.execute(insert_sql,(url_input,title_1))
	conn.commit()

#---use thread to get information----
class Thread_url(threading.Thread):
	def __init__(self,t_name):
		threading.Thread.__init__(self,name=t_name)
	def run(self):
		global count
		while queue.qsize():
			url_open=queue.get()
			try:
				count +=1
				html_deal(url_open)
			finally:
				queue.task_done()

def thread_go(num):
	for i in range(0,num):
		t_name="thread_%s" %i
		t =Thread_url(t_name)
		t.start()
	for i in range(0,num):
		t_name="thread_%s" %i
		t.join()

#-----------main founction ------------------------
if __name__=='__main__':
#	url_open = raw_input("Please input the url : \n")
	url_open=['http://www.sina.com.cn','http://news.qq.com','http://blog.csdn.net/tianzhu123/article/details/8187470','http://gd.sina.com.cn/news/s/2014-03-25/073689102.html','http://news.qq.com/a/20140325/013858.htm','http://news.sina.com.cn','http://blog.csdn.net/forgetbook/article/details/9080463','http://sports.sina.com.cn/']
	example = url_open[0]
	crawler_init()
	count = 0

	time_start = datetime.datetime.now()
	print time_start
	domain = domain_get(example)
	print "url input: ",example,'\n',"url domain: ",domain

	Page = html_open(example)
	fp = open("test.txt",'wb+')
	fp.writelines(Page)
	time.sleep(1)
	fp.close()
	
	link_get(example)
	fp_1=open("url_result.txt",'wb+')
	fp_1.truncate()
	fp_1.writelines(links)
	time.sleep(1)
	fp_1.close()

	for i in links[1110:1180]:
		queue.put(i)
	thread_go(thread_num)
	time.sleep(20)
	conn.close()
	
	time_end = datetime.datetime.now()
	print time_end
	print "time use: %s " %(time_end-time_start)
