import multiprocessing,time
from multiprocessing import Process, JoinableQueue
import signle_stockData,multi_getHisData,update_by_day

def func1():
    time.sleep(5)
    print ("I am func1...........")
def func2():
    time.sleep(5)
    print ("I am func2...........")
def consumer(q, name):
    while True:
        fileNum = q.get()
        #multi_getHisData.thread_function(name,fileNum)
        #将hdf中数据装载到csv中
        signle_stockData.writeDataToCsv(name,fileNum)
        #每日更新csv
        #update_by_day.read_hdf(name,fileNum)
        q.task_done()  # count - 1


def producer(q):
    for i in range(19):
        q.put(i)
    q.join()  # 阻塞  直到一个队列中的所有数据 全部被处理完毕
if __name__ == '__main__' :
    startTime = time.time()
    # process_name = multiprocessing.current_process().name
    q = JoinableQueue()
    p1 = Process(target=producer, args=(q,))
    c1 = Process(target=consumer, args=(q, "Process_1"))
    c2 = Process(target=consumer, args=(q, "Process__2"))
    c3 = Process(target=consumer, args=(q, "Process__3"))
    p1.start()
    c1.daemon = True  # 设置为守护进程 主进程中的代码执行完毕之后,子进程自动结束
    c2.daemon = True
    c3.daemon = True
    c1.start()
    c2.start()
    c3.start()
    p1.join()
    endTime = time.time()
    print ("time :", endTime - startTime)