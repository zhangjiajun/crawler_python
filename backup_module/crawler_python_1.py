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
import codecs
#------ founction get domain-----
def domain_get(url_open):
	
	pattern = re.compile(r'https*://\w+?\.([\w\.]*)/*')
	domain = pattern.match(url_open)
	return domain.group(1)

#-------founction make httpheaders and open html ---------
def html_open(url_input):

	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11(KHTML,like Gecko) Chrome/23.0.1271.64 Safari/537.11',
				}

	print url_input
	req = urllib2.Request(url_input,headers=headers)
	con = urllib2.urlopen(req)
	Page = con.read()
	
	return Page

#------founction get title and keyword ----------
def title_get(url_input):
	
	Page_1 = html_open(url_input)
	soup = BeautifulSoup.BeautifulSoup(Page,fromEncoding="gb18030")
	title = unicode(soup.title)
#	print title,type(title[8])
	print title[7:-8]

	keyword = soup.findAll('meta',attrs={"name":"keywords"})
	print keyword,type(keyword)

	reload(sys)
	sys.setdefaultencoding("utf-8")
	title_url = str(title[7:-8]).encode("utf-8")
	keyword_url = str(keyword).encode("utf-8")

	return (title_url,keyword_url)

def html_deal(url_input):
	title_1,keyword_1=title_get(url_input)
	string_1 = url_input+title_1+keyword_1+'\n'
	fp_1.writelines(string_1)
#	fp_1.writelines(url_input)
#	fp_1.writelines(title_1)
#	fp_1.writelines(keyword_1)

#--------define a class parser the source code of html --------
class MyParser(HTMLParser.HTMLParser):
	def __init__(self):
		HTMLParser.HTMLParser.__init__(self)
		self.links = []

	def handle_starttag(self,tag,attrs):

		if tag == 'a':
			#judge <a>  
			for name,value in attrs:
				if name == 'href' and "http" in value and domain in value:  
					self.links.append(value+"\n")

if __name__=='__main__':
#	url_open = raw_input("Please input the url : \n")
	url_open=['http://www.sina.com.cn','http://news.qq.com','http://blog.csdn.net/tianzhu123/article/details/8187470','http://gd.sina.com.cn/news/s/2014-03-25/073689102.html','http://news.qq.com/a/20140325/013858.htm','http://news.sina.com.cn','http://blog.csdn.net/forgetbook/article/details/9080463','http://sports.sina.com.cn/']

	time_start = datetime.datetime.now()
	print time_start
	global domain
	example = url_open[0]
#	get domain
	domain = domain_get(example)
#	host=urlparse.urlparse(example)
#	domain = host.hostname
	print "url input: ",example,'\n',"url domain: ",domain

	Page = html_open(example)
	my = MyParser()
	my.feed(Page)
	fp = open("test.txt",'wb+')
	fp.writelines(my.links)

	fp_1=open("title.txt",'wb+')
	fp_1.truncate()
	#here input my.links to url_open queue
	for i in range(102,105,1):
		link_open=my.links[i]
		html_deal(link_open)

	fp_1.close()
	time_end = datetime.datetime.now()
	print time_end
	print "time use: %s " %(time_end-time_start)
