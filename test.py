import pandas as pd
import requests,re,csv,os,json
import pandas as pd
from datetime import datetime, date, timedelta

yesterday = (date.today() + timedelta(days=-2)).strftime("%Y%m%d")
today = date.today().strftime("%Y%m%d")

def get_stockCode():
    stock_codes=pd.read_hdf('stock.hdf5')
    stock_list=[]
    urls=[]
    stock_his_data=[]
#     stock_list=stock_codes[0]
    stock_list = ['603811']
    for stock_code in range(len(stock_list)):
        # print (stock_list[stock_code])
        urls.append("http://q.stock.sohu.com/hisHq?code=cn_" + stock_list[
            stock_code] + "&start="+str('19900101')+"&end="+str(yesterday)+"&stat=1&order=A&period=d&callback=historySearchHandler&rt=json")
    return urls

def get_infoFromSohu(url):
    r=requests.get(url)
    list_res=[]
    list_res.append(r.status_code)
    list_res.append(r.text)
    return list_res

def get_stockHisData():
    dt = datetime.now()
    print('开始时间: ', dt.strftime('%I:%M:%S %p'))
    urls = get_stockCode()

    for url in range(len(urls)):
        # get response history stock data
        response = get_infoFromSohu(urls[url])
        # json load
        print (response[0])
        if response[0]==200:
            res_data = json.loads(response[1])
            #if the info status return 0 ,means info is usefull,else continue the loop
            if res_data:
                if res_data[0]['status'] == 0:
                    data_len = len(res_data[0]['hq'])
                    for i in range(data_len):
                        print(res_data[0]['hq'])
                else:
                    continue
            else:
                continue
        else:
            continue
        # store.close()
    dt = datetime.now()
    print('结束时间: ', dt.strftime('%I:%M:%S %p'))

if __name__ == '__main__' :
    get_stockHisData()