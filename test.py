import time
import random
import pandas as pd
from multiprocessing import Process, JoinableQueue
from multiprocessing import Pool
import multiprocessing

def get_stockCode(name,stock_divid_id):
    stock_divid_codes = pd.read_hdf('stock_divid/stock_divid' + str(stock_divid_id) + '.hdf5')
    urls = []
    #stock_list[0]: code stock_list[1]: name
    stock_list = stock_divid_codes
    endDate=time.strftime("%Y%m%d", time.localtime())
    for stock_code in range(len(stock_list)):
        urls.append("http://q.stock.sohu.com/hisHq?code=cn_" + stock_list[0].iloc[
            stock_code] + "&start=19900101&end="+str(endDate)+"&stat=1&order=D&period=d&callback=historySearchHandler&rt=json"+"||"+stock_list[1].iloc[stock_code])
    #return  urls
        print (name,stock_code)

def consumer(q, name):
    while True:
        food = q.get()
        get_stockCode(name,food)
        q.task_done()  # count - 1


def producer(q):
    for i in range(19):
        q.put(i)
    q.join()  # 阻塞  直到一个队列中的所有数据 全部被处理完毕


if __name__ == '__main__':
    startTime = time.time()
    process_name = multiprocessing.current_process().name
    q = JoinableQueue()
    p1 = Process(target=producer, args=(q,))
    c1 = Process(target=consumer, args=(q, process_name+"1"))
    c2 = Process(target=consumer, args=(q, process_name+"2"))
    c3 = Process(target=consumer, args=(q, process_name+"3"))
    p1.start()
    c1.daemon = True  # 设置为守护进程 主进程中的代码执行完毕之后,子进程自动结束
    c2.daemon = True
    c3.daemon = True
    c1.start()
    c2.start()
    c3.start()
    p1.join()
    endTime = time.time()
    print("time :", endTime - startTime)
    #tuple 处理进程并发，但是并发进程的结束时间要依赖于tuple中最后处理完数据的进程时间而定
    # list = []
    # step = 3
    # for i in range(9,19):
    #     list.append(i)
    # group_num = [list[j:j + step] for j in range(0, len(list), step)]
    # for k in range(len(group_num)):
    #     testFL = group_num[k]
    #     startTime=endTime = time.time()
        #testFL = [9]
        # pool = Pool(3)
        # pool.map(thread_function, testFL)
        # pool.close()
        # pool.join()