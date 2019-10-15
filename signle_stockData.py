import pandas as pd
import csv,time,re,os,math
import multiprocessing
from multiprocessing import Process, JoinableQueue

def make_dir(dir_name):
    isExists=os.path.exists(dir_name)
    if not isExists:
       os.makedirs(dir_name)
    else:
       pass
def judge_block(stock_name):
    if re.findall('^6\d+',stock_name):
        dirName='sh'
    elif re.findall('^3\d+',stock_name):
        dirName='cy'
    else:
        dirName='sz'
    return dirName
def writeDataToCsv(name,fileNum):
    df = pd.read_hdf('stockHisData/stock_his_data'+str(fileNum)+'.hdf5')
    df.columns = ['交易日期', '开盘价 ', '收盘价', '涨跌', '涨幅', '最低价', '最高价', '成交量', '成交额', '换手率', '股票代码', '股票名称']
    grouped = df.groupby('股票代码')
    for name, group in grouped:
        single_stocke_start_time = time.time()
        dirName = judge_block(name)
        make_dir(dirName)
        print (fileNum,name,len(group))
        stock_file = open(dirName + '\stock_' + str(name) + '.csv', 'a', newline='')
        csv_write = csv.writer(stock_file, dialect='excel')
        csv_write.writerow(['股票代码', '股票名称','交易日期', '开盘价 ', '收盘价', '涨跌', '涨幅', '最低价', '最高价', '成交量', '成交额', '换手率'])
        for i in range(len(group)):
            csv_write.writerow([group.iloc[i][-2],group.iloc[i][-1],group.iloc[i][0],group.iloc[i][1],group.iloc[i][2],group.iloc[i][3],group.iloc[i][4],group.iloc[i][5],group.iloc[i][6],group.iloc[i][7],group.iloc[i][8],group.iloc[i][9]])
        single_stocke_end_time = time.time()
        cost_time=round(single_stocke_end_time - single_stocke_start_time)
        stock_file.close()

def consumer(q, name):
    while True:
        start=time.time()
        fileNum = q.get()
        writeDataToCsv(name,fileNum)
        end=time.time()
        cost=round(end-start)
        if cost>float(60):
            cost = str(cost/60)
            print('stock_his_data' + fileNum + '.hdf5 耗时:' +cost+'分')
        else:
            print('stock_his_data' + fileNum + '.hdf5 耗时:' + str(cost) + '秒')

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