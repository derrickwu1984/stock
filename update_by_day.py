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
def read_hdf(fileNum):
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
        print(' 耗时:' + str(math.ceil(single_stocke_end_time - single_stocke_start_time)) + '秒')
if __name__ == '__main__' :
    read_hdf(0)