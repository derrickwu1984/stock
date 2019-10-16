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
    stock_list = ['603811','诚意药业']
    for stock_code in range(len(stock_list)):
        # print (stock_list[stock_code])
        urls.append("http://q.stock.sohu.com/hisHq?code=cn_" + stock_list[
            stock_code] + "&start="+str('20191014')+"&end="+str('20191014')+"&stat=1&order=A&period=d&callback=historySearchHandler&rt=json"+"||"+stock_list[1])
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
        stock_code = urls[url].split("_")[1].split("&")[0]
        stock_name = urls[url].split("||")[1]
        url_addr = urls[url].split("||")[0]
        # get response history stock data
        response = get_infoFromSohu(url_addr)
        res_data = json.loads(response[1])
        # json load
        #if the info status return 0 ,means info is usefull,else continue the loop
        if response[0]==200:
            if res_data:
                if res_data[0]['status'] == 0:
                    data_len = len(res_data[0]['hq'])
                    for i in range(data_len):
                        res_data[0]['hq'][i].append(stock_code)
                        res_data[0]['hq'][i].append(stock_name)
                        print(res_data[0]['hq'][i][-2])
                    else:
                        continue
            else:
                continue
        else:
            continue
    dt = datetime.now()
    print('结束时间: ', dt.strftime('%I:%M:%S %p'))

if __name__ == '__main__' :
    get_stockHisData()