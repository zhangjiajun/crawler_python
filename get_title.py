#!/usr/bin/python
#coding:utf-8-

#  author:jiajun zhang <jzhang@suse.com>
#  time:2013-12-
#  target:just for python practise
#  language:python

import HTMLParser,urllib
import re,sys,os,string
import BeautifulSoup

if __name__=='__main__':
	url_open = raw_input("Please input the url : \n")
#	url_open = 'http://'+ url_input
#	url_open="http://www.qq.com.cn"
	Page = urllib.urlopen(url_open).read()
	soup= BeautifulSoup.BeautifulSoup(Page,fromEncoding="gb18030")
#	soup= BeautifulSoup.BeautifulSoup(Page)
	title =soup.title
	print title.contents
	fp=open("test.txt",'wb+')
	title= unicode(title)
	print title
	keyword=[]
	keyword=soup.findAll('meta')
	print keyword
