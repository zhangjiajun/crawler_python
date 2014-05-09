#!/usr/bin/python
#coding:utf-8-

#  author:jiajun zhang <jzhang@suse.com>
#  time:2013-12-
#  target:just for python practise
#  language:python

import MySQLdb,time

if __name__=='__main__':
	url_open=['http://www.sina.com.cn','http://news.qq.com','http://blog.csdn.net/tianzhu123/article/details/8187470','http://gd.sina.com.cn/news/s/2014-03-25/073689102.html','http://news.qq.com/a/20140325/013858.htm','http://news.sina.com.cn','http://blog.csdn.net/forgetbook/article/details/9080463','http://sports.sina.com.cn/']

	global db,cursor,drop_sql,create_sql,insert_sql,select_sql
	conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='novell',port=3306,charset='utf8')
	cur=conn.cursor()

	cur.execute("create database if not exists web_information")
	conn.select_db('web_information')
	cur.execute("create table if not exists test(url varchar(40))")
#	cur.execute("insert into test values %s",`http`)
	cur.execute("insert ignore into test values(%s)",url_open[1])
	
	conn.commit()
	cur.close()
	conn.close()


