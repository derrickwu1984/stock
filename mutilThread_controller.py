import multiprocessing,time,threading,logging,os
from multiprocessing import Process, JoinableQueue
import signle_stockData,multi_getHisData,update_by_day
from datetime import datetime, date, timedelta
import pandas as pd
import utils
from utils import check_holiday

logging.getLogger().setLevel(logging.INFO)

event = threading.Event()
threads_producer = []
threads_consumer= []
q = JoinableQueue()
producer_q = JoinableQueue()
isEmpty=q.empty()
yesterday = (date.today() + timedelta(days=-1)).strftime("%Y%m%d")
today = date.today().strftime("%Y%m%d")
def consumer(q,threadName,threadNum):
    while True:
        event.wait()
        fileNum = q.get()
        multi_getHisData.thread_function(threadName, yesterday, today, fileNum)
        logging.info('队列大小%s 线程 %s 处理文件完成 %s' % (q.qsize(), threadNum, fileNum))
        q.task_done()  # count - 1
        logging.info ('当前活动线程数'+str(threading.active_count()))

def producer(producer_q):
    for i in range(19):
        q.put(i)
    q.join()# 阻塞  直到一个队列中的所有数据 全部被处理完毕

#today = date.today().strftime("%Y%m%d")
if __name__ == '__main__' :
    #1、判断是否为节假日，只有在工作日才跑数
    if not check_holiday(yesterday):
        logging.info('昨天日期为:%s 是工作日' % yesterday)
        os._exit(0)
    else:
        logging.info ('昨天日期为:%s 是工作日' %yesterday)
        #2、先备份昨天的记录
        utils.controller()
        startTime = time.time()
        thread_producer=threading.Thread(target=producer, args=(producer_q,))
        thread_producer.start()
        for i in range(19):
            threads_consumer.append(threading.Thread(target=consumer, args=(q, 'thread_producer_' + str(i),i)))
        for thread_consumer in threads_consumer:
            thread_consumer.start()
        logging.info ('主线程通知开始...')
        event.set()
        endTime = time.time()
        costTime=round(endTime-startTime)
        logging.info (multi_getHisData.count_time(costTime))