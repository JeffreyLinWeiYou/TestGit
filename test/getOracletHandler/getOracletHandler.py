# -*- coding:utf-8 -*-
'''
Created on 2016�~3��5��

@author: ben
'''
from bson import *
import MySQLdb
import time
import datetime
import json

class GetOracletHandler(object):
    '''
    classdocs
    '''
    def date_handler(self,obj):
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj

    def __init__(self):
        '''
        Constructor
        '''
        self.db=MySQLdb.connect("140.118.7.42","s8107072004","ben60514","crawler_test",charset='utf8')
    
    @staticmethod
    def findPredictPeople(category):
        category=int(category)
        db=MySQLdb.connect("140.118.7.42","s8107072004","ben60514","crawler_test",charset='utf8')
        results=[]
        if category==0:
            cursor=db.cursor()
            sql="SELECT `predict_people` FROM `oraclet` WHERE `type`=1 OR `type`=3 group by `predict_people`"
            cursor.execute(sql)
            MysqlData=cursor.fetchall()
        elif category==1:
            cursor=db.cursor()
            sql="SELECT `predict_people` FROM `oraclet` WHERE `type`=5 OR `type`=6 group by `predict_people`"
            cursor.execute(sql)
            MysqlData=cursor.fetchall()
    #如果是大盤，還沒做
        elif category==3:
            return "尚未"
            pass
        else: 
            return False
        db.close()
        for record in MysqlData:
            results.append(record[0])
        return   results
    @staticmethod
    def findOraclet(peopleCategory,peopleName):
        peopleCategory=int(peopleCategory)
        print peopleName
        print type(peopleName)
        db=MySQLdb.connect("140.118.7.42","s8107072004","ben60514","crawler_test",charset='utf8')
        if peopleCategory<=1:
            dict_cursor = db.cursor(MySQLdb.cursors.DictCursor)
            sql="SELECT * FROM `oraclet` WHERE `predict_people`='%s' AND `results` IS NOT NULL"\
             % (peopleName.encode('utf-8'))
            dict_cursor.execute(sql)
            MysqlData=dict_cursor.fetchall()
            results=[]
            for record in MysqlData:
                record.pop('earn_Amount')
                record.pop('now_price')
                record.pop('type')
                record.pop('occur_time')
                results.append(record)
            db.close()
        return  results
    @staticmethod
    def findContradictoryOraclets(peopleCategory,predictCode,predictTime):
        db=MySQLdb.connect("140.118.7.42","s8107072004","ben60514","crawler_test",charset='utf8')
        peopleCategory=int(peopleCategory)
        if peopleCategory <2:
            sql ="SELECT * FROM `oraclet` WHERE `predict_targetcode`='%s' AND `predict_time`='%s' AND `results` IS NOT NULL AND `type`!= 2 AND `type`!=4"\
             % (str(predictCode),str(predictTime))
            dict_cursor = db.cursor(MySQLdb.cursors.DictCursor)
            dict_cursor.execute(sql)
            MysqlData=dict_cursor.fetchall()
            print len(MysqlData)
            results={}
            results["positive"]=[]
            results["negative"]=[]
            for record in MysqlData:
                record.pop('earn_Amount')
                record.pop('now_price')
                record.pop('type')
                record.pop('occur_time')
                if record['event_content']==u'買進':
                    results["positive"].append(record)
                elif record['event_content']==u'賣出':
                    results["negative"].append(record)
            db.close()
            return  results
            pass
        elif  peopleCategory==3:
            pass
        else:
            return False 
    