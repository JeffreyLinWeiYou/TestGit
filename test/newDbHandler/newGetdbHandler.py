# -*- coding:utf-8 -*-
'''
Created on 2016年5月22日

@author: ben
'''
from bson import *
import MySQLdb
import time
import datetime
import json
class GetDbHandler(object):
    '''
    classdocs
    '''
    def date_handler(self,obj):
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj

    def __init__(self):
        '''
        Constructor
        '''
        self.ip="140.118.7.46"
        self.account="s8107072004"
        self.password="ben60514"
        self.schema="ptt_test"
        self.db=MySQLdb.connect(self.ip,self.account,self.password,self.schema,charset='utf8')
        self.dict_cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
    def __del__(self):
        self.db.close() 
    def getAllOraclet(self):
        sql="SELECT * FROM oraclet"
        try:
            self.dict_cursor.execute(sql)
            MysqlData=self.dict_cursor.fetchall()
            return MysqlData
        except MySQLdb.Error as e: 
            print 'error in getOnePttSource:',e
            return False
    def getOneOracletAllMessage(self,oracletNumber):
        sql="SELECT * FROM `message` as m,oraclet as o WHERE m.`o_number`=o.number and o.number='%s'"%\
            (str(oracletNumber))
        try:
            self.dict_cursor.execute(sql)
            MysqlData=self.dict_cursor.fetchall()
            return MysqlData
        except MySQLdb.Error as e: 
            print 'error in getOnePttSource:',e
            return False    
        pass  
    def getALLPredictorAccuracy(self):
        sql="SELECT predict_people ,COUNT(*) count,SUM(`results`) sum, SUM(`results`)/COUNT(*) accuracy FROM `oraclet` WHERE `result_status`=1 Group BY `predict_people` ORDER BY COUNT(*) DESC"
        try:
            self.dict_cursor.execute(sql)
            MysqlData=self.dict_cursor.fetchall()
            return MysqlData
        except MySQLdb.Error as e: 
            print 'error in getOnePttSource:',e
            return False 
    def getOnePredictorAccuracy(self,predictor):
        sql="SELECT predict_people ,COUNT(*) count,SUM(`results`) sum, SUM(`results`)/COUNT(*) accuracy FROM `oraclet` WHERE `result_status`=1 and `predict_people`='%s'Group BY `predict_people` ORDER BY COUNT(*) DESC"\
            (predictor.encode('utf-8'))
        try:
            self.dict_cursor.execute(sql)
            MysqlData=self.dict_cursor.fetchall()
            return MysqlData
        except MySQLdb.Error as e: 
            print 'error in getOnePttSource:',e
            return False      
    
         
    def getPredictorOracletCount(self,predict_people):
        sql="SELECT predict_people ,COUNT(*) count FROM `oraclet` WHERE predict_people='%s'"%\
            (predict_people.encode('utf-8'))
        try:
            self.dict_cursor.execute(sql)
            MysqlData=self.dict_cursor.fetchall()
            return MysqlData
        except MySQLdb.Error as e: 
            print 'error in getOnePttSource:',e
            return False            
        
        
