import threading,time
import pandas as pd,os
import requests,re,csv,os,json,math
import pandas as pd
from multiprocessing import Process, JoinableQueue
from datetime import datetime, date, timedelta
import multiprocessing

def thread_function(process_name,stock_divid_id):
    get_stockHisData(process_name,stock_divid_id)

def get_infoFromSohu(url):
    r=requests.get(url)
    return r.text

def make_dir(dir_name):
    isExists=os.path.exists(dir_name)
    if not isExists:
       os.makedirs(dir_name)
    # else:
    #    print ('文件夹已创建')

def get_stockCode(stock_divid_id):
    stock_divid_codes = pd.read_hdf('stock_divid/stock_divid' + str(stock_divid_id) + '.hdf5')
    # fill_urls(stock_divid_codes)
    urls = []
    #stock_list[0]: code stock_list[1]: name
    stock_list = stock_divid_codes
    yesterday = (date.today() + timedelta(days=-1)).strftime("%Y%m%d")
    today = date.today().strftime("%Y%m%d")
    endDate=time.strftime("%Y%m%d", time.localtime())
    for stock_code in range(len(stock_list)):
        urls.append("http://q.stock.sohu.com/hisHq?code=cn_" + stock_list[0].iloc[
            stock_code] + "&start="+str(yesterday)+"&end="+str(today)+"&stat=1&order=D&period=d&callback=historySearchHandler&rt=json"+"||"+stock_list[1].iloc[stock_code])
    return  urls
def get_stockHisData(process_name,stock_divid_id):
    startTime  = time.time()
    dt = datetime.now()
    print(process_name,'file'+str(stock_divid_id),'开始时间: ', dt.strftime('%I:%M:%S %p'))
    urls = get_stockCode(stock_divid_id)
    for url in range(len(urls)):
            store = pd.HDFStore('stockHisData/stock_his_data'+str(stock_divid_id)+'.hdf5', 'a')
            stock_code = urls[url].split("_")[1].split("&")[0]
            stock_name = urls[url].split("||")[1]
            url_addr=urls[url].split("||")[0]
            # get response history stock data
            response = get_infoFromSohu(url_addr)
            # json load
            res_data = json.loads(response)
            #if the info status return 0 ,means info is usefull,else continue the loop
            if res_data[0]['status'] == 0:
                # defind use data length
                data_len = len(res_data[0]['hq'])
                print(process_name,'文件'+str(stock_divid_id),url,stock_code, data_len)
                # loop the data
                for i in range(data_len):
                    # append the stock code in the end of every list
                    res_data[0]['hq'][i].append(stock_code)
                    res_data[0]['hq'][i].append(stock_name)
                df = pd.DataFrame(res_data[0]['hq'])
                store.append("stock_his_data", df, min_itemsize=12,append=True,format="table")
            else:
                continue
            store.close()
    dt = datetime.now()
    endTime = time.time()
    print(process_name+' stock_divid_'+str(stock_divid_id)+' 结束时间: ', dt.strftime('%I:%M:%S %p')," 耗时：",endTime - startTime)

def consumer(q, name):
    while True:
        fileNum = q.get()
        thread_function(name,fileNum)
        q.task_done()  # count - 1


def producer(q):
    for i in range(1):
        q.put(i)
    q.join()  # 阻塞  直到一个队列中的所有数据 全部被处理完毕

if __name__ == '__main__' :
    startTime = time.time()
    process_name = multiprocessing.current_process().name
    q = JoinableQueue()
    p1 = Process(target=producer, args=(q,))
    c1 = Process(target=consumer, args=(q, process_name+"_1"))
    c2 = Process(target=consumer, args=(q, process_name+"_2"))
    c3 = Process(target=consumer, args=(q, process_name+"_3"))
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
 # numList = []
 # for i in range(2):
 #  p = multiprocessing.Process(target=thread_function, args=(i,))
 #  numList.append(p)
 #  p.start()
 #  p.join()
 #  print ("Process end.")