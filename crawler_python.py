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
#------ founction get domain-----
def domain_get(url_open):
	
	pattern = re.compile(r'https*://\w+?\.([\w\.]*)/*')
	domain = pattern.match(url_open)
	return domain.group(1)

#-------founction make httpheaders and open html ---------
def html_open(url_input):

	headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11(KHTML,like Gecko) Chrome/23.0.1271.64 Safari/537.11',
				}

	req = urllib2.Request(url_input,headers=headers)
	con = urllib2.urlopen(req)
	Page = con.read()
	
	return Page

#--------define a class parser the source code of html --------
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
#------founction get title and keyword ----------
def get_title_keyword(Page):
	
	soup= BeautifulSoup.BeautifulSoup(Page,fromEncoding="gb18030")
	title= unicode(soup.title)
	print title
	print title[7:-8],type(title[8])

	keyword=soup.findAll('meta',attrs={"name":"keywords"})
	print keyword,type(keyword)

#	fp = open("title.txt",'wb+')
#	fp.writelines(str(title[7:-8]))
#	fp.writelines(str(keyword))

if __name__=='__main__':
#	url_open = raw_input("Please input the url : \n")
	url_open=['http://www.sina.com.cn','http://news.qq.com','http://blog.csdn.net/tianzhu123/article/details/8187470','http://gd.sina.com.cn/news/s/2014-03-25/073689102.html','http://news.qq.com/a/20140325/013858.htm','http://news.sina.com.cn','http://blog.csdn.net/forgetbook/article/details/9080463','http://sports.sina.com.cn/']
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
	#here input my.links to url_last
	#print type(my.links),my.links[21:29]
	for i in range(21,23,1):
		print datetime.datetime.now()
		#just dig from the current website
		link_open=my.links[21]
		host=urlparse.urlparse(link_open)
		domain = host.hostname

		Page_1=html_open(link_open)
		my_1=MyParser()
		my_1.feed(Page_1)
		get_title_keyword(Page_1)
		fp_1.writelines(my_1.links)
		
	fp_1.close()


