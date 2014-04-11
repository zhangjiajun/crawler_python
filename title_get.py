#!/usr/bin/python
#coding:utf-8-

#  author:jiajun zhang <jzhang@suse.com>
#  time:2013-12-
#  target:just for python practise
#  language:python

import HTMLParser,urllib2
import re,sys,os,string
import BeautifulSoup
import codecs
import datetime

def get_title_keyword(Page):
#	获取网页编码方式
#	chardit = chardet.detect(Page)
#	s =chardit['encoding']
#	print s
				
#	兼容输出
#	soup= BeautifulSoup.BeautifulSoup(Page)
#	print 'soup output:',soup.originalEncoding
	soup= BeautifulSoup.BeautifulSoup(Page,fromEncoding="gb18030")

	title_1 =soup.title
	code_1 = title_1.contents
	print type(code_1),code_1
#	realcode = code_1[2].decode("GB2312").encode('utf-8')

	title= unicode(soup.title)
	print title
	print title[7:-8],type(title[8])

	keyword=[]
#some page name=Keywords so can't figure out
	keyword=soup.findAll('meta',attrs={"name":"keywords"})
	print keyword
	print type(keyword)


#	写入标题
	reload(sys)
	sys.setdefaultencoding("utf-8")
	fp = open("title.txt",'wb+')
	fp.writelines(str(title[7:-8]).encode("utf-8"))
	fp.writelines(str(keyword).encode("utf-8"))

if __name__=='__main__':
	fp = open("title.txt",'wb+')
	fp.writelines("Bellow is what we get from the internet:")
	url_open=['http://blog.csdn.net/tianzhu123/article/details/8187470','http://gd.sina.com.cn/news/s/2014-03-25/073689102.html','http://news.qq.com/a/20140325/013858.htm','http://news.sina.com.cn/w/2014-03-25/112129787127.shtml']
	for i in url_open[3:]:
		print i
		time = datetime.datetime.now()
		print time,type(time)
		Page = urllib2.urlopen(i).read()
		get_title_keyword(Page)
