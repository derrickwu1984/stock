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
        stock_file = open(dirName + '\stock_' + str(name) + '.csv', 'a', newline='')
        csv_write = csv.writer(stock_file, dialect='excel')
        csv_write.writerow(['股票代码', '股票名称','交易日期', '开盘价 ', '收盘价', '涨跌', '涨幅', '最低价', '最高价', '成交量', '成交额', '换手率'])
        for i in range(len(group)):
            #print('stock_his_data'+str(fileNum),'中第'+str(i)+'条记录', name+'记录总数:'+str(len(group)))
            csv_write.writerow([group.iloc[i][-2],group.iloc[i][-1],group.iloc[i][0],group.iloc[i][1],group.iloc[i][2],group.iloc[i][3],group.iloc[i][4],group.iloc[i][5],group.iloc[i][6],group.iloc[i][7],group.iloc[i][8],group.iloc[i][9]])
        single_stocke_end_time = time.time()
        cost_time=round(single_stocke_end_time - single_stocke_start_time)
        print('stock_his_data' + str(fileNum), name + '记录总数:' + str(len(group)),'耗时'+str(cost_time)+'秒')
        stock_file.close()