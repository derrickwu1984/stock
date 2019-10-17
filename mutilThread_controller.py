import multiprocessing,time,threading,logging
from multiprocessing import Process, JoinableQueue
import signle_stockData,multi_getHisData,update_by_day
from datetime import datetime, date, timedelta
import pandas as pd

import utils

event = threading.Event()
threads_producer = []
threads_consumer= []
q = JoinableQueue()
producer_q = JoinableQueue()
isEmpty=q.empty()
yesterday = (date.today() + timedelta(days=-2)).strftime("%Y%m%d")
today = (date.today() + timedelta(days=-1)).strftime("%Y%m%d")
def consumer(q,threadName,threadNum):
    while True:
        event.wait()
        fileNum = q.get()
        multi_getHisData.thread_function(threadName, yesterday, today, fileNum)
        print('队列大小%s 线程 %s 处理文件完成 %s' % (q.qsize(), threadNum, fileNum))
        q.task_done()  # count - 1
        if not isEmpty:
            logging.warning('所有线程执行完毕')

def producer(producer_q):
    for i in range(19):
        q.put(i)
    q.join()# 阻塞  直到一个队列中的所有数据 全部被处理完毕

#today = date.today().strftime("%Y%m%d")
if __name__ == '__main__' :
    #先备份昨天的记录
    utils.controller()

    startTime = time.time()
    # list=[]
    # step=19
    # for i in range(19):
    #     list.append(i)
    # divid_list=[list[j:j + step] for j in range(0, len(list), step)]
    threading.Thread(target=producer, args=(producer_q,)).start()
    for i in range(19):
        threads_consumer.append(threading.Thread(target=consumer, args=(q, 'thread_producer_' + str(i),i)))
    for thread_consumer in threads_consumer:
        thread_consumer.start()

    time.sleep(1)
    print('主线程通知开始...')
    event.set()
    endTime = time.time()
    costTime=round(endTime-startTime)
    print (multi_getHisData.count_time(costTime))