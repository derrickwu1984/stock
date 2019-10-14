import pandas as pd
import csv,time


def writeDataToCsv():
    df = pd.read_hdf('stock_his_data1.hdf5')
    df.columns = ['交易日期', '开盘价 ', '收盘价', '涨跌', '涨幅', '最低价', '最高价', '成交量', '成交额', '换手率', '股票代码']
    grouped = df.groupby('股票代码')
    for name, group in grouped:
        single_stocke_start_time = time.time()
        print(name)
        stock_file = open('stock_' + str(name) + '.csv', 'a', newline='')
        csv_write = csv.writer(stock_file, dialect='excel')
        csv_write.writerow(['交易日期', '开盘价 ', '收盘价', '涨跌', '涨幅', '最低价', '最高价', '成交量', '成交额', '换手率', '股票代码'])
        for i in range(len(group)):
            # print (group.iloc[i])
            csv_write.writerow(group.iloc[i])
        single_stocke_end_time = time.time()
        stock_file.close()
        print(single_stocke_end_time - single_stocke_start_time)