import threading,time
import pandas as pd
import requests,re,csv,os,json,math
import pandas as pd
from datetime import datetime

import getStockHisData

def fill_urls(stock_list):
    urls = []
    print(stock_list)
    for stock_code in range(len(stock_list)):
        urls.append("http://q.stock.sohu.com/hisHq?code=cn_" + stock_list[stock_code] + "&start=19900101&end=20191010&stat=1&order=D&period=d&callback=historySearchHandler&rt=json")

def thread_function(i):
    stock_divid_codes=pd.read_hdf('stock_divid/stock_divid'+str(i)+'.hdf5')
    # fill_urls(stock_divid_codes)
    urls = []
    stock_list=stock_divid_codes[0]
   # for stock_code in range(len(stock_list)):
        # pass
        #urls.append("http://q.stock.sohu.com/hisHq?code=cn_" + stock_list[stock_code] + "&start=19900101&end=20191010&stat=1&order=D&period=d&callback=historySearchHandler&rt=json")
        #print (stock_list[stock_code])
        #TimeMark = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #return urls
    print (stock_list)

exitFlag=0
class myThread(threading.Thread):
    def __init__(self,threadID,name,counter,fileNum):
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.name=name
        self.counter=counter
        self.fileNum=fileNum
    def run (self):
        print ("Starting"+self.name)
        print ("threading.currentThread()"+str(threading.activeCount()))
        threadLock.acquire()
        print_time(self.name,self.counter,self.fileNum,1)
        threadLock.release()
        print ("Exiting"+self.name)
def print_time(threadName,counter,fileNum,delay):
    while counter:
        if exitFlag:
            (threading.Thread).exit()
        time.sleep(delay)
        thread_function(fileNum)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1
threadLock = threading.Lock()
threads = []
# 创建新线程
thread1 = myThread(0,"Thread_0",1,0)
thread2 = myThread(1,"Thread_1",1,1)
# thread3 = myThread(2,"Thread_2",1,2)

# 开启新线程
thread1.start()
thread2.start()
# thread3.start()

# 添加线程到线程列表
threads.append(thread1)
threads.append(thread2)
# threads.append(thread3)

# 等待所有线程完成
for t in threads:
    t.join()
print ("Exiting Main Thread")