#!/usr/bin/python
#coding:utf-8-

#  author:jiajun zhang <jzhang@suse.com>
#  time:2014-04-06
#  target:crawler for website information
#  language:python

import HTMLParser,urllib2,urlparse
import BeautifulSoup,socket
import re,sys,os,string
import codecs
import Queue,threading
import MySQLdb,time,datetime

#------ founction init crawler-----
def crawler_init():
	global domain,queue,queue_mysql,links,sleep_time,time_out,thread_num
	links = []
	queue = Queue.Queue()
	queue_mysql = Queue.Queue()
	sleep_time = 0.1
	time_out = 20
	thread_num = 8
	
#------ founction init mysql-----
def mysql_init():
	global conn,cur,db_name,create_database,drop_table,create_table,insert_table
	conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='novell',port=3306,charset='utf8')
	cur=conn.cursor()

	db_name = "web_information"
	creat_database = "create database if not exists %s" % db_name
	drop_table = "drop table if exists test"
	creat_table = "create table test( url varchar(40), title varchar(40) )"
	insert_table = "insert ignore into test values ( %s,%s )"
	
	cur.execute(creat_database)
	conn.select_db(db_name)
	cur.execute(drop_table)
	cur.execute(creat_table)

#------ founction get domain-----
def domain_get(url_open):
	
	pattern = re.compile(r'https*://\w+?\.([\w\.]*)/*')
	domain_1 = pattern.match(url_open)
#	host=urlparse.urlparse(example)
#	domain = host.hostname
	domain =  domain_1.group(1)
	return domain

#------ founction get link-----
def link_get(url_open):
	Page = html_open(url_open)
	pattern = re.compile("href=\"(.+?)\"")
	link_1 = pattern.findall(Page)
	for link in link_1:
		if "http" in link and domain in link and "auto" not in link:
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
	status_html = con.getcode()
	if status_html != 200:
		error_link = url_input+"error"
		print error_link 
		return error_link 
	else:
		Page = con.read()
		return Page
	con.close()

#------founction get title ----------
def title_get(url_input):
	Page = html_open(url_input)	
	soup = BeautifulSoup.BeautifulSoup(Page,fromEncoding="gb18030")
	title = unicode(soup.title)

#	keyword = soup.findAll('meta',attrs={"name":"keywords"})
#	print keyword,type(keyword)

	reload(sys)
	sys.setdefaultencoding("utf-8")
	title_url = str(title[7:-8]).encode("utf-8")

	return title_url

#------founction deal with html ----------
def html_deal(url_input):
	title_1=title_get(url_input)
	queue_mysql.put((url_input,title_1))

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
		t_name="thread_%3s" %i
		t =Thread_url(t_name)
		t.start()
	for i in range(0,num):
		t_name="thread_%3s" %i
		t.join(6)

#-----------main founction ------------------------
if __name__=='__main__':
#	url_open = raw_input("Please input the url : \n")
	url_open=['http://www.sina.com.cn','http://news.qq.com','http://blog.csdn.net/tianzhu123/article/details/8187470','http://gd.sina.com.cn/news/s/2014-03-25/073689102.html','http://news.qq.com/a/20140325/013858.htm','http://news.sina.com.cn','http://blog.csdn.net/forgetbook/article/details/9080463','http://sports.sina.com.cn/']

	count = 0
	example = url_open[0]
	crawler_init()
	mysql_init()

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

	for i in links[4:60]:
		queue.put(i)
	thread_go(thread_num)

	while queue_mysql.qsize():
		i = queue_mysql.get()
		cur.execute(insert_table,i)
		conn.commit()
	cur.close()
	conn.close()
	
	print "loop is ",count
	time_end = datetime.datetime.now()
	print time_end
	print "time use: %s " %(time_end-time_start)
