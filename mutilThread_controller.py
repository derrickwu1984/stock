import multiprocessing,time,threading,logging
from multiprocessing import Process, JoinableQueue
import signle_stockData,multi_getHisData,update_by_day

event = threading.Event()
threads_producer = []
threads_consumer= []
q = JoinableQueue()
def consumer(q, name):
    while True:
        event.wait()
        fileNum = q.get()
        #搜集数据加载到hdf中
        #multi_getHisData.thread_function(name,fileNum)
        #将hdf中数据装载到csv中
        # signle_stockData.writeDataToCsv(name,fileNum)
        #每日更新csv
        try:
            update_by_day.read_hdf(name,fileNum)
        except:
            logging.warning("更新数据出错了！")
        q.task_done()  # count - 1


def producer(q,threadName,fileNum):
    event.wait()
    multi_getHisData.thread_function(threadName,fileNum)
    q.put(fileNum)
    q.join()  # 阻塞  直到一个队列中的所有数据 全部被处理完毕
if __name__ == '__main__' :
    startTime = time.time()
    for i in range(19):
        threads_producer.append(threading.Thread(target=producer, args=(q, 'thread_producer_' + str(i),i)))
        threads_consumer.append(threading.Thread(target=consumer, args=(q, 'thread_consumer_' + str(i))))
    for thread_producer in threads_producer:
        thread_producer.start()
    for thread_consumer in threads_consumer:
        thread_consumer.start()

    print('主线程通知开始...')
    event.set()
    endTime = time.time()
    costTime=round(endTime-startTime)
    if costTime > float(60):
        costTime = str(costTime / 60)
        print('耗时:' + costTime + '分')
    else:
        print('耗时:' + str(costTime) + '秒')