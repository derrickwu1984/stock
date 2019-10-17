import threading,time,logging
import pandas as pd,os
import requests,re,csv,os,json,math
import pandas as pd
from multiprocessing import Process, JoinableQueue
from datetime import datetime, date, timedelta
import multiprocessing

def thread_function(process_name,startDate,endDate,stock_divid_id):
    #get_stockHisData(process_name,startDate,endDate,stock_divid_id)
    update_dataEveryDate(process_name,startDate,endDate,stock_divid_id)

def get_infoFromSohu(url):
    r = requests.get(url)
    list_res=[]
    list_res.append(r.status_code)
    list_res.append(r.text)
    return list_res

def make_dir(dir_name):
    isExists=os.path.exists(dir_name)
    if not isExists:
       os.makedirs(dir_name)
    # else:
    #    print ('文件夹已创建')

def get_stockCode(startDate,endDate,stock_divid_id):
    stock_divid_codes = pd.read_hdf('stock_divid/stock_divid' + str(stock_divid_id) + '.hdf5')
    urls = []
    #stock_list[0]: code stock_list[1]: name
    stock_list = stock_divid_codes
    for stock_code in range(len(stock_list)):
        urls.append("http://q.stock.sohu.com/hisHq?code=cn_" + stock_list[0].iloc[
            stock_code] + "&start="+str(startDate)+"&end="+str(endDate)+"&stat=1&order=A&period=d&callback=historySearchHandler&rt=json"+"||"+stock_list[1].iloc[stock_code])
    return  urls

def judge_block(stock_code):
    if re.findall('^6\d+',stock_code):
        dirName='sh'
    elif re.findall('^3\d+',stock_code):
        dirName='cy'
    else:
        dirName='sz'
    return dirName

def count_time(costTime):
    if costTime > float(60):
        costTime = str(costTime / 60)
        ret_cost='耗时:' + costTime + '分'
        return ret_cost
    else:
        ret_cost = '耗时:' + str(costTime) + '秒'
        return ret_cost
#some stock return data only by descend
def query_byDescend(startDate,endDate,stock_code,stock_name):
    url="http://q.stock.sohu.com/hisHq?code=cn_" + str(stock_code)+ "&start="+str(startDate)+"&end="+str(endDate)+"&stat=1&order=D&period=d&callback=historySearchHandler&rt=json"
    res=get_infoFromSohu(url)
    dirName = judge_block(stock_code)
    if res[0]==200:
        res_data = json.loads(res[1])
        stock_file = open(dirName + '\stock_' + str(stock_code) + '.csv', 'a', newline='')
        csv_write = csv.writer(stock_file, dialect='excel')
        csv_write.writerow(['股票代码', '股票名称', '交易日期', '开盘价 ', '收盘价', '涨跌', '涨幅', '最低价', '最高价', '成交量', '成交额', '换手率'])
        if res_data:
            print (stock_code,url)
            if res_data[0]['status'] == 0:
                res_data[0]['hq'].sort()
                data_len = len(res_data[0]['hq'])
                for i in range(data_len):
                    res_data[0]['hq'][i].append(stock_code)
                    res_data[0]['hq'][i].append(stock_name)
                    csv_write.writerow([res_data[0]['hq'][i][-2], res_data[0]['hq'][i][-1], res_data[0]['hq'][i][0],
                                        res_data[0]['hq'][i][1], res_data[0]['hq'][i][2], res_data[0]['hq'][i][3],
                                        res_data[0]['hq'][i][4], res_data[0]['hq'][i][5], res_data[0]['hq'][i][6],
                                        res_data[0]['hq'][i][7], res_data[0]['hq'][i][8], res_data[0]['hq'][i][9]])
            else:
                logging.warning('股票%s %s倒序数据返回status不等于0' %(stock_code,stock_name))
        else:
            logging.warning('股票%s %s倒序数据返回为空' % (stock_code, stock_name))
        stock_file.close()
    else:
        logging.warning('股票%s %s倒序数据返回http status不等于200' % (stock_code, stock_name))

# stock_list={"603810":"丰山集团","300749":"顶固集创","300748":"金力永磁","002938":"鹏鼎控股","002936":"郑州银行","601577":"长沙银行","603583":"捷昌驱动","603790":"雅运股份"}
# for k in stock_list:
#     startTime = time.time()
#     query_byDescend('19900101', '20191014', k, stock_list[k])
#     endTime = time.time()
#     # print (k,stock_list[k])
#     costTime=round(endTime-startTime)
#     print (count_time(costTime))

def get_stockHisData(process_name,startDate,endDate,stock_divid_id):
    startTime  = time.time()
    dt = datetime.now()
    print(process_name,'file'+str(stock_divid_id),'开始时间: ', dt.strftime('%I:%M:%S %p'))
    urls = get_stockCode(startDate,endDate,stock_divid_id)
    dir_list=['sh','sz','cy']
    for dir in range(len(dir_list)):
        make_dir(dir)
    for url in range(len(urls)):
        stock_code = urls[url].split("_")[1].split("&")[0]
        stock_name = urls[url].split("||")[1]
        url_addr = urls[url].split("||")[0]
        startDate=url_addr.split('&')[1].split('=')[1]
        endDate = url_addr.split('&')[2].split('=')[1]
        dirName = judge_block(stock_code)
        # get response history stock data
        response = get_infoFromSohu(url_addr)
        if response[0] == 200:
            res_data = json.loads(response[1])
            stock_file = open(dirName + '\stock_' + str(stock_code) + '.csv', 'a', newline='')
            csv_write = csv.writer(stock_file, dialect='excel')
            csv_write.writerow(['股票代码', '股票名称', '交易日期', '开盘价 ', '收盘价', '涨跌', '涨幅', '最低价', '最高价', '成交量', '成交额', '换手率'])
            if res_data:
                if res_data[0]['status'] == 0:
                    data_len = len(res_data[0]['hq'])
                    for i in range(data_len):
                        res_data[0]['hq'][i].append(stock_code)
                        res_data[0]['hq'][i].append(stock_name)
                        csv_write.writerow([res_data[0]['hq'][i][-2], res_data[0]['hq'][i][-1], res_data[0]['hq'][i][0],
                          res_data[0]['hq'][i][1], res_data[0]['hq'][i][2], res_data[0]['hq'][i][3],
                          res_data[0]['hq'][i][4], res_data[0]['hq'][i][5], res_data[0]['hq'][i][6],
                          res_data[0]['hq'][i][7], res_data[0]['hq'][i][8], res_data[0]['hq'][i][9]])
                        # print([res_data[0]['hq'][i][-2], res_data[0]['hq'][i][-1], res_data[0]['hq'][i][0],
                        #   res_data[0]['hq'][i][1], res_data[0]['hq'][i][2], res_data[0]['hq'][i][3],
                        #   res_data[0]['hq'][i][4], res_data[0]['hq'][i][5], res_data[0]['hq'][i][6],
                        #   res_data[0]['hq'][i][7], res_data[0]['hq'][i][8], res_data[0]['hq'][i][9]])
                else:
                    print('%s status!=0 status=%s'%(stock_code,res_data[0]['status']))
                    continue
            else:
                print('%s 返回空 status=%s'%(stock_code,res_data))
                continue
            # stock_file.close()
        else:
            print('%s http status!=200 http status=%s'%(stock_code,response[0]))
            query_byDescend(startDate,endDate,stock_code,stock_name)
            continue
    dt = datetime.now()
    endTime = time.time()
    costTime=round(endTime-startTime)
    ret_cost=count_time(costTime)
    print(process_name+' stock_divid_'+str(stock_divid_id)+' 结束时间: ', dt.strftime('%I:%M:%S %p'),ret_cost)

def update_dataEveryDate(process_name,startDate,endDate,stock_divid_id):
    startTime  = time.time()
    dt = datetime.now()
    print(process_name,'file'+str(stock_divid_id),'开始时间: ', dt.strftime('%I:%M:%S %p'))
    urls = get_stockCode(startDate,endDate,stock_divid_id)
    dir_list=['sh','sz','cy']
    for dir in range(len(dir_list)):
        make_dir(dir)
    for url in range(len(urls)):
        stock_code = urls[url].split("_")[1].split("&")[0]
        stock_name = urls[url].split("||")[1]
        url_addr = urls[url].split("||")[0]
        startDate=url_addr.split('&')[1].split('=')[1]
        endDate = url_addr.split('&')[2].split('=')[1]
        dirName = judge_block(stock_code)
        # get response history stock data
        response = get_infoFromSohu(url_addr)
        if response[0] == 200:
            res_data = json.loads(response[1])
            stock_file = open(dirName + '\stock_' + str(stock_code) + '.csv', 'a', newline='')
            csv_write = csv.writer(stock_file, dialect='excel')
            if res_data:
                if res_data[0]['status'] == 0:
                    data_len = len(res_data[0]['hq'])
                    for i in range(data_len):
                        res_data[0]['hq'][i].append(stock_code)
                        res_data[0]['hq'][i].append(stock_name)
                        csv_write.writerow([res_data[0]['hq'][i][-2], res_data[0]['hq'][i][-1], res_data[0]['hq'][i][0],
                          res_data[0]['hq'][i][1], res_data[0]['hq'][i][2], res_data[0]['hq'][i][3],
                          res_data[0]['hq'][i][4], res_data[0]['hq'][i][5], res_data[0]['hq'][i][6],
                          res_data[0]['hq'][i][7], res_data[0]['hq'][i][8], res_data[0]['hq'][i][9]])
                        # print([res_data[0]['hq'][i][-2], res_data[0]['hq'][i][-1], res_data[0]['hq'][i][0],
                        #   res_data[0]['hq'][i][1], res_data[0]['hq'][i][2], res_data[0]['hq'][i][3],
                        #   res_data[0]['hq'][i][4], res_data[0]['hq'][i][5], res_data[0]['hq'][i][6],
                        #   res_data[0]['hq'][i][7], res_data[0]['hq'][i][8], res_data[0]['hq'][i][9]])
                else:
                    print('%s status!=0 status=%s'%(stock_code,res_data[0]['status']))
                    continue
            else:
                print('%s 返回空 status=%s'%(stock_code,res_data))
                continue
            # stock_file.close()
        else:
            print('%s http status!=200 http status=%s'%(stock_code,response[0]))
            query_byDescend(startDate,endDate,stock_code,stock_name)
            continue
    dt = datetime.now()
    endTime = time.time()
    costTime=round(endTime-startTime)
    ret_cost=count_time(costTime)
    print(process_name+' stock_divid_'+str(stock_divid_id)+' 结束时间: ', dt.strftime('%I:%M:%S %p'),ret_cost)
