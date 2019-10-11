import pandas as pd
import re,h5py
from lxml import etree
import requests,re,csv,os,json
import pandas as pd
from datetime import datetime

def get_infoFromSohu(url):
    r=requests.get(url)
    return r.text

#获取股票代码
def get_stockCode():
    stock_codes=pd.read_hdf('stock.hdf5')
    stock_list=[]
    urls=[]
    stock_his_data=[]
    stock_list=stock_codes[0]
    for stock_code in range(len(stock_list)):
        # print (stock_list[stock_code])
        urls.append("http://q.stock.sohu.com/hisHq?code=cn_" + stock_list[
            stock_code] + "&start=19900101&end=20191010&stat=1&order=D&period=d&callback=historySearchHandler&rt=json")
    return urls
def get_stockHisData():
    dt = datetime.now()
    print('开始时间: ', dt.strftime('%I:%M:%S %p'))
    urls = get_stockCode()

    for url in range(len(urls)):
        store = pd.HDFStore('stock_his_data3.hdf5', 'a')
        stock_code = urls[url].split("_")[1].split("&")[0]
        # get response history stock data
        response = get_infoFromSohu(urls[url])
        # json load
        res_data = json.loads(response)
        #if the info status return 0 ,means info is usefull,else continue the loop
        if res_data[0]['status'] == 0:
            # defind use data length
            data_len = len(res_data[0]['hq'])
            print(url,stock_code, data_len)
            # loop the data
            for i in range(data_len):
                # append the stock code in the end of every list
                res_data[0]['hq'][i].append(stock_code)
            df = pd.DataFrame(res_data[0]['hq'])
            store.append("stock_his_data", df, append=True, format="table")
        else:
            continue
        store.close()
    dt = datetime.now()
    print('结束时间: ', dt.strftime('%I:%M:%S %p'))

def show_data():
    stock_his_data = pd.read_hdf('stock_his_data2.hdf5')
    stock_his_data.columns = ['交易日期', '开盘价 ', '收盘价', '涨跌', '涨幅', '最低价', '最高价', '成交量', '成交额', '换手率', '股票代码']
    stock_his_data

if __name__ == '__main__':
     get_stockHisData()