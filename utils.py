import os,time,requests,re,logging,json
import shutil
from datetime import datetime, date, timedelta

def count_time(startTime,endTime):
    costTime=round(endTime-startTime)
    if costTime > float(60):
        costTime = str(costTime / 60)
        ret_cost='耗时:' + costTime + '分'
        return ret_cost
    else:
        ret_cost = '耗时:' + str(costTime) + '秒'
        return ret_cost

def copy_dir(dirList,desName):
    root = os.getcwd()
    for i in range(len(dirList)):
        startTime = time.time()
        src_path = os.path.join(root, dirList[i])
        des_path = os.path.join('bak',desName, dirList[i])
        shutil.copytree(src_path, des_path)
        if os.path.isdir(des_path):
            print(des_path + ' copy success')
        else:
            print ('copy fail')
        endTime = time.time()
        print (count_time(startTime,endTime))

def controller():
    dir_list=['sh','sz','cy']
    yesterday = (date.today() + timedelta(days=-1)).strftime("%Y%m%d")
    copy_dir(dir_list,yesterday)

def get_infoFromUrl(url):
    r = requests.get(url)
    list_res=[]
    list_res.append(r.status_code)
    list_res.append(r.text)
    return list_res
def check_holiday(check_date):
    url='http://api.goseek.cn/Tools/holiday?date='+check_date
    check_date=url.split('=')[1]
    r=get_infoFromUrl(url)
    res_status=r[0]
    if res_status==200:
        res_data = json.loads(r[1])
        data_status=res_data['data']
        if data_status==0:
            logging.info ('今天日期为:%s 是工作日' %check_date)
            return True
        else:
            logging.info ('今天日期为:%s 是非工作日' %check_date)
            return  False
            os._exit(0)
    else:
        logging.warning('url地址为 %s status = %s' %(url,res_status))
        return False
# controller()
