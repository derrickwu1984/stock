import pandas as pd
import csv,time,re,os,math
import multiprocessing
from multiprocessing import Process, JoinableQueue

def judge_block(stock_name):
    if re.findall('^6\d+',stock_name):
        dirName='sh'
    elif re.findall('^3\d+',stock_name):
        dirName='cy'
    else:
        dirName='sz'
    return dirName
def read_hdf(name,fileNum):
    df = pd.read_hdf('stockHisData/stock_his_data'+str(fileNum)+'.hdf5')
    df.columns = ['交易日期', '开盘价 ', '收盘价', '涨跌', '涨幅', '最低价', '最高价', '成交量', '成交额', '换手率', '股票代码', '股票名称']
    grouped = df.groupby('股票代码')
    for name, groups in grouped:
        single_stocke_start_time = time.time()
        group = groups.sort_values(by="交易日期", ascending=False).iloc[0]
        dirName=judge_block(name)
        stock_file = open(dirName + '\stock_' + str(name) + '.csv', 'a', newline='')
        csv_write = csv.writer(stock_file, dialect='excel')
        # print ([group[-2],group[-1],group[0],group[1],group[2],group[3],group[4],group[5],group[6],group[7],group[8],group[9]])
        csv_write.writerow([group[-2],group[-1],group[0],group[1],group[2],group[3],group[4],group[5],group[6],group[7],group[8],group[9]])
        stock_file.close()
        single_stocke_end_time = time.time()
        print(name+' 耗时:' + str(math.ceil(single_stocke_end_time - single_stocke_start_time)) + '秒')

def consumer(q, name):
    while True:
        fileNum = q.get()
        read_hdf(name,fileNum)
        q.task_done()  # count - 1


def producer(q):
    for i in range(19):
        q.put(i)
    q.join()  # 阻塞  直到一个队列中的所有数据 全部被处理完毕
if __name__ == '__main__':
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
    print("time :", endTime - startTime)