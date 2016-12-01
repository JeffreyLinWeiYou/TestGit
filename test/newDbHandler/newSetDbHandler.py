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
class SetDbHandler(object):
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
    def updateOracletPopularity(self,oracletNumber,popularity):  
        sql="UPDATE `oraclet` SET popularity ='%s' WHERE `number`='%s'"%\
            (str(popularity),str(oracletNumber))        
        try:
            self.dict_cursor.execute(sql)
            self.db.commit()
            return True
        except MySQLdb.Error as e:
            print e 
            return False        
    def updatePredictorStatus(self,predictor,oracletNo,verifiedOracletNo,rightOracletNo,accuracy):
        sql="UPDATE `predict_people` SET `allOraclet`='%s',`verifiedOraclet`='%s',`verifiedTrue`='%s',`accuracy`='%s' WHERE `predict_people`='%s'"%\
            (str(oracletNo),str(verifiedOracletNo),str(rightOracletNo),str(accuracy),predictor.encode('utf-8'))
        try:
            self.dict_cursor.execute(sql)
            self.db.commit()
            return True
        except MySQLdb.Error as e:
            print e    
            return False           
    def updatePredictorVerifiedSatus(self,predictor,verifiedOracletNo,rightOracletNo,accuracy):
        sql="UPDATE `predict_people` SET `verifiedOraclet`='%s',`verifiedTrue`='%s',`accuracy`='%s' WHERE `predict_people`='%s'"%\
            (str(verifiedOracletNo),str(rightOracletNo),str(accuracy),predictor.encode('utf-8'))    
        try:
            self.dict_cursor.execute(sql)
            self.db.commit()
            return True
        except MySQLdb.Error as e:
            print e    
            return False         
        
        