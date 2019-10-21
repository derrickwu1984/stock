import threading,json,requests,logging
import time
from utils import check_holiday
from datetime import datetime, date, timedelta

def run():
    print('当前线程的名字是： ', threading.current_thread().name)
if __name__ == '__main__':
    # print ("main 被调起了")
    yesterday = (date.today() + timedelta(days=-1)).strftime("%Y%m%d")
    print (yesterday)
    today = date.today().strftime("%Y%m%d")
    if not check_holiday(today):
        print ('fail')
    else:
        print ('ok')