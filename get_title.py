#!/usr/bin/python
#coding:utf-8-

#  author:jiajun zhang <jzhang@suse.com>
#  time:2013-12-
#  target:just for python practise
#  language:python

import HTMLParser,urllib
import re,sys,os,string
import BeautifulSoup
import chardet

def get_title_keyword(Page):
#	获取网页编码方式
	chardit = chardet.detect(Page)
	s =chardit['encoding']
	print s
				
#	兼容输出
	soup= BeautifulSoup.BeautifulSoup(Page,fromEncoding="gb18030")
#	soup= BeautifulSoup.BeautifulSoup(Page)
#	print 'soup output:',soup.originalEncoding

	title =soup.title
	print title.contents
#	print title.contents.decode('xxxxx').encode('utf-8')


	title= unicode(soup.title)
#	title= unicode(soup.title.contents)
	print title


	keyword=[]
#some page name=Keywords so can't figure out
	keyword=soup.findAll('meta',attrs={"name":"keywords"})
#	keyword=soup.findAll('meta')
	print keyword


#	写入标题
	fp = open("title.txt",'a')
	fp.writelines(str(soup.title))
	fp.writelines(str(keyword))

if __name__=='__main__':
	fp = open("title.txt",'wb+')
	fp.writelines("Bellow is what we get from the internet:")
	url_open=['http://blog.csdn.net/tianzhu123/article/details/8187470','http://gd.sina.com.cn/news/s/2014-03-25/073689102.html','http://news.qq.com/a/20140325/013858.htm','http://news.sina.com.cn/w/2014-03-25/112129787127.shtml']
	for i in url_open[1:]:
		print i
		Page = urllib.urlopen(i).read()
		get_title_keyword(Page)
