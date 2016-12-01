#-*- coding:utf-8 -*-
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib,urllib2
import time
import pandas as pd
import csv
from _sqlite3 import Row
import MySQLdb
import requests
from time import sleep
from bs4 import BeautifulSoup
import json
from getWebHandler.getPrices import *
from grs import Stock
import jieba
import logging
class Demo:
    def __init__(self, i):
        self.i = i
    def __str__(self):
        return  str(self.i)
    def hello(self):
        print "hello", self
        
def setOneContradiction(self,oracletDict):
    sql="SELECT * FROM `oraclet` WHERE  `predict_targetcode`='%s' AND `predict_time`<='%s' AND `predict_time`>='%s' AND `type`!= 2 AND `type`!= 4"%\
        (oracletDict['code'],(oracletDict['date']+datetime.timedelta(days = self.days)).strftime("%Y-%m-%d"),(oracletDict['date']-datetime.timedelta(days = self.days)).strftime("%Y-%m-%d"))
    print sql
    try:
        self.dict_cursor.execute(sql)
        MysqlData=self.dict_cursor.fetchall()
#        如果回傳回來的值大於一，那就把回傳的oraclet的hasContradiction全部變成1 
        print len(MysqlData)
        if len(MysqlData)>1:
            for temp in MysqlData:
                sql="UPDATE `oraclet` SET hasContradiction = true WHERE `predict_people` = '%s' AND `predict_time` = '%s' AND `predict_targetcode` = %s AND `event_content` = '%s'"\
                    %(temp['predict_people'].encode('utf8'),temp['predict_time'].strftime("%Y-%m-%d"),str(temp['predict_targetcode']),temp['event_content'].encode('utf8'))
                self.dict_cursor.execute(sql)
                self.db.commit()
    except MySQLdb.Error as e:
        print 'error in getOnePttSource:',e
def main():
    testdb=MySQLdb.connect('140.118.7.46','s8107072004','ben60514','test',charset='utf8')
    dict_cursor = testdb.cursor(MySQLdb.cursors.DictCursor)
    sql="SELECT * FROM `oraclet` WHERE `type` < 5 ORDER BY `predict_time` DESC"
    try:
        dict_cursor.execute(sql)
        MysqlData=dict_cursor.fetchall()
    except MySQLdb.Error as e: 
        logging.exception("parseGos")
#     print MysqlData   
    ptt_testdb=MySQLdb.connect('140.118.7.46','s8107072004','ben60514','ptt_test',charset='utf8')
    dict_cursor = ptt_testdb.cursor(MySQLdb.cursors.DictCursor)

    for data in MysqlData:
        print data
        try:
            sql="INSERT INTO `oraclet` (predict_people,predict_time,predict_targetcode,predict_targetname,\
            occur_time,event_content,type,now_price) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%\
            (data['predict_people'].encode('utf8'),data['predict_time'].strftime("%Y-%m-%d"),
             str(data['predict_targetcode']),data['predict_targetname'].encode('utf8'),
             data['occur_time'].strftime("%Y-%m-%d"),data['event_content'].encode('utf8'),
             str(data['type']),str(data['now_price']))
            print sql
            dict_cursor.execute(sql)
            ptt_testdb.commit()
    #         更新矛盾卜卦-------------------------------------------------------------
            if data['type']!= 2 or data['type']!= 4:
                sql="SELECT * FROM `oraclet` WHERE  `predict_targetcode`='%s' AND `predict_time`<='%s' AND `predict_time`>='%s' AND `type`!= 2 AND `type`!= 4"%\
                    (data['predict_targetcode'],(data['predict_time']+datetime.timedelta(days = 7)).strftime("%Y-%m-%d"),(data['predict_time']-datetime.timedelta(days = 7)).strftime("%Y-%m-%d"))
                print sql
                try:
                    dict_cursor.execute(sql)
                    MysqlData=dict_cursor.fetchall()
            #        如果回傳回來的值大於一，那就把回傳的oraclet的hasContradiction全部變成1 
                    print len(MysqlData)
                    if len(MysqlData)>1:
                        for temp in MysqlData:
                            sql="UPDATE `oraclet` SET hasContradiction = true WHERE `predict_people` = '%s' AND `predict_time` = '%s' AND `predict_targetcode` = %s AND `event_content` = '%s'"\
                                %(temp['predict_people'].encode('utf8'),temp['predict_time'].strftime("%Y-%m-%d"),str(temp['predict_targetcode']),temp['event_content'].encode('utf8'))
                            dict_cursor.execute(sql)
                            ptt_testdb.commit()
                except MySQLdb.Error as e:
                    print 'error in getOnePttSource:',e
    #             ------------------------------------------------------------------------
            
    #         break
        except MySQLdb.Error as e: 
            logging.exception("parseGos")
    testdb.close()
    ptt_testdb.close()        
#         for i in range(1,7,1):
#             print  (20*i)-1
if __name__ == '__main__':
    main()

