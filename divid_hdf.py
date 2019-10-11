import pandas as pd
import re,h5py
from lxml import etree
import requests,re,csv,os,json,math
import pandas as pd
from datetime import datetime

stock_codes=pd.read_hdf('stock1.hdf5')

#divid hdf data into block
def divid_block():
    data_len = len(stock_codes)
    list_index = []
    for stock in range(data_len):
        if stock % 200 == 0:
            list_index.append(stock)
    list_index.append(data_len)
    return list_index

def write_blockData():
    list_index=divid_block()
    for i in range(len(list_index)):
        if i == (len(list_index) - 1):
            continue
        else:
            print(i, stock_codes.iloc[list_index[i]:list_index[i + 1]])
            store = pd.HDFStore('stock_divid' + str(i) + '.hdf5', 'a')
            store.append("stock", stock_codes.iloc[list_index[i]:list_index[i + 1]], append=True, format="table")
            store.close()

def test_result():
    for i in range(19):
        stock_divid_codes = pd.read_hdf('stock_divid' + str(i) + '.hdf5')
        print(i, stock_divid_codes.shape)