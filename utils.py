import os,time
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

# controller()
