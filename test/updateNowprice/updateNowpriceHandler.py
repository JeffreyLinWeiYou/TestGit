#-*- coding:utf-8 -*-
'''
Created on 2016年4月9日

@author: ben
'''
import csv
import MySQLdb
import time
import datetime
from getWebHandler.getPrices import *
from MySQLHandler.MySQLHandler import MySQLHandler
import logging
class UpdateNowpriceHandler(object):
    '''
    classdocs
    '''


    def __init__(self,twseDict,gtsmDict):
        '''
        Constructor
        '''
        self.dbHandler=MySQLHandler()
        self.twseDict=twseDict
        self.gtsmDict=gtsmDict
    def main(self):
        date=datetime.datetime.now().date()
        MysqlDatas=self.dbHandler.getAllCanUpdatePrice(date)
        print MysqlDatas
        for MysqlData in MysqlDatas:
            print MysqlData
            code=MysqlData['predict_targetcode']
            if (self.twseDict.get(str(code))!=None):
                twseHandler=TwseHandler()
                MysqlData['now_price']=twseHandler.getNowPrice(MysqlData['predict_time'],code)                                                        
            if (self.gtsmDict.get(str(code))!=None):
                gtsmHandler=GtsmHandler()
                MysqlData['now_price']=gtsmHandler.getNowPrice(MysqlData['predict_time'],code)
            
            if MysqlData['now_price']!= 0 and MysqlData['now_price']!= None:
                self.dbHandler.updateOracletNowprice(MysqlData)
#             break
def csvToList(filePath):
    f=open(filePath,'r')
    codeList=[]
    nameList=[]
    resultDict={}
    for row in csv.reader(f):
        codeList.append(row[0])
        nameList.append(row[1])
        resultDict[row[0]]=row[1]
    f.close()
    return resultDict 
if __name__ == '__main__':
    twseDict=csvToList('../data/twseStockList.csv')
    gtsmDict=csvToList('../data/gtsmStockList.csv')
    update=UpdateNowpriceHandler(twseDict,gtsmDict)
    update.main()