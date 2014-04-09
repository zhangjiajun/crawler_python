#!/usr/bin/python
#coding:utf-8-
import urllib2
from threading import Thread,Lock
from Queue import Queue
import datetime,time
import BeautifulSoup 

#-------founction make httpheaders and open html ---------
def html_open(url_input):

	headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11(KHTML,like Gecko) Chrome/23.0.1271.64 Safari/537.11',
				}

	req = urllib2.Request(url_input,headers=headers)
	con = urllib2.urlopen(req)
	Page = con.read()
	
#------founction get title and keyword ----------
def get_title_keyword(Page):
	
	soup= BeautifulSoup.BeautifulSoup(Page,fromEncoding="gb18030")
	title= unicode(soup.title)
	print title[7:-8],type(title[8])

#	keyword=soup.findAll('meta',attrs={"name":"keywords"})
#	print keyword,type(keyword)

class Fetcher:
    def __init__(self,threads):
        self.opener = urllib2.build_opener(urllib2.HTTPHandler)
        self.lock = Lock() #线程锁
        self.q_req = Queue() #任务队列
        self.q_ans = Queue() #完成队列
        self.threads = threads
        for i in range(threads):
            t = Thread(target=self.threadget)
            t.setDaemon(True)
            t.start()
        self.running = 0
 
    def __del__(self): #解构时需等待两个队列完成
        time.sleep(0.5)
        self.q_req.join()
        self.q_ans.join()
 
    def taskleft(self):
        return self.q_req.qsize()+self.q_ans.qsize()+self.running
 
    def push(self,req):
        self.q_req.put(req)
 
    def pop(self):
        return self.q_ans.get()
 
    def threadget(self):
        while True:
            req = self.q_req.get()
            with self.lock: #要保证该操作的原子性，进入critical area
                self.running += 1
            try:
                ans = html_open(req)
#                get_title_keyword(ans)
            except Exception, what:
                ans = ''
                print what
            self.q_ans.put((req,ans))
            with self.lock:
                self.running -= 1
            self.q_req.task_done()
            time.sleep(0.1) # don't spam
 
if __name__ == "__main__":
    url_open=['http://www.sina.com.cn','http://news.qq.com','http://blog.csdn.net/tianzhu123/article/details/8187470','http://gd.sina.com.cn/news/s/2014-03-25/073689102.html','http://news.qq.com/a/20140325/013858.htm','http://news.sina.com.cn','http://blog.csdn.net/forgetbook/article/details/9080463','http://sports.sina.com.cn/']
    links = [ 'http://www.verycd.com/topics/%d/'%i for i in range(5420,5430) ]
    time_1=datetime.datetime.now()
    print time_1
    f = Fetcher(threads=10)
    for url in url_open:
        f.push(url)
    while f.taskleft():
        url,content = f.pop()
        print url,get_title_keyword(content)
    time_2=datetime.datetime.now()
    print time_2
    print "time use: %s " %(time_2-time_1)
