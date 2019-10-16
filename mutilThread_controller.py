import multiprocessing,time,threading,logging
from multiprocessing import Process, JoinableQueue
import signle_stockData,multi_getHisData,update_by_day
import pandas as pd

event = threading.Event()
threads_producer = []
threads_consumer= []
q = JoinableQueue()
producer_q = JoinableQueue()
isEmpty=q.empty()
def consumer(q, name):
    while True:
        event.wait()
        fileNum = q.get()
        #将hdf中数据装载到csv中
        # signle_stockData.writeDataToCsv(name,fileNum)
        #每日更新csv
        update_by_day.read_hdf(name,fileNum)
        # df = pd.read_hdf('stockHisData/stock_his_data' + str(fileNum) + '.hdf5', mode='r')
        # df.columns = ['交易日期', '开盘价 ', '收盘价', '涨跌', '涨幅', '最低价', '最高价', '成交量', '成交额', '换手率', '股票代码', '股票名称']
        print ('消费文件%s 队列大小%s'% (fileNum,q.qsize()))
        q.task_done()  # count - 1


def producer(q,threadName,threadNum):
    event.wait()
    fileNum=producer_q.get()
    multi_getHisData.thread_function(threadName,fileNum)
    print ('队列大小%s 线程 %s 处理文件完成 %s' %(q.qsize() ,threadNum,fileNum))
    producer_q.task_done()
    q.put(fileNum)
    q.join()  # 阻塞  直到一个队列中的所有数据 全部被处理完毕

def producer_queue(producer_q):
    for i in range(19):
        producer_q.put(i)
    producer_q.join()

if __name__ == '__main__' :
    startTime = time.time()
    # list=[]
    # step=19
    # for i in range(19):
    #     list.append(i)
    # divid_list=[list[j:j + step] for j in range(0, len(list), step)]
    threading.Thread(target=producer_queue, args=(producer_q,)).start()
    for i in range(19):
        # for threadNum in range(len(divid_list[i])):
        threads_producer.append(threading.Thread(target=producer, args=(q, 'thread_producer_' + str(i),i)))

    for thread_producer in threads_producer:
        # thread_producer.setDaemon(True)
        thread_producer.start()
    # thread_consumer = threading.Thread(target=consumer, args=(q, 'thread_consumer_1'))
    # thread_consumer.start()

    time.sleep(1)
    print('主线程通知开始...')
    event.set()
    endTime = time.time()
    costTime=round(endTime-startTime)
    if costTime > float(60):
        costTime = str(costTime / 60)
        print('耗时:' + costTime + '分')
    else:
        print('耗时:' + str(costTime) + '秒')

    # if isEmpty:
    #     print ('队列已空')
    #     exit()