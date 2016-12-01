# -*- coding:utf-8 -*-
'''
Created on 2016年6月27日

@author: ben
'''
import MySQLdb
import datetime
import logging
import json
class performanceMysqlHd():
    def __init__(self,percentage):
        '''
        Constructor
        '''
        self.ip="140.118.7.46"
        self.account="s8107072004"
        self.password="ben60514"
        self.schema="ptt_test"
        self.db=MySQLdb.connect(self.ip,self.account,self.password,self.schema,charset='utf8')
        self.dict_cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        self.percentage=percentage
        
    def __del__(self):
        self.db.close()
    def dictToDb(self,d):
#         textType=u'%a %b %d %H:%M:%S %Y'
#         print d['d_date']
#         date_object = datetime.datetime.strptime(d['d_date'], textType)
        dStr = d['d_date'].strftime('%Y-%m-%d %H:%M:%S')
        sql=u"INSERT INTO ptt_performance_20 (author,date,title,ip,link,content,message,messageNum)VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(d['b_author'],dStr,d['c_title'],d['e_ip'],d['link'],d['f_content'].decode('utf-8'),d['g_message'],str(d['h_messageNum']).decode('utf-8'))
#         print sql
        try:
            self.dict_cursor.execute(sql)
            self.db.commit()
        except MySQLdb.Error as e: 
            print e
            logging.exception("parseGos")        
#         pass    
    def getAllSource(self):
        sql="SELECT * FROM %s ORDER BY `date` DESC"%(self.percentage)
        try:
            self.dict_cursor.execute(sql)
            MysqlData=self.dict_cursor.fetchall()
            return MysqlData
        except MySQLdb.Error as e: 
            print e
            logging.exception("parseGos") 
    def getOneOraclet(self,name,predictDate,code):
        sql="SELECT * FROM oraclet WHERE predict_people ='%s' and predict_time='%s' and predict_targetcode='%s'"%\
            (name.encode('utf-8'),predictDate.strftime('%Y-%m-%d'),code.encode('utf-8'))
        try:
            self.dict_cursor.execute(sql)
            MysqlData=self.dict_cursor.fetchall()
            return MysqlData
        except MySQLdb.Error as e: 
            return []
            print e
            logging.exception("parseGos") 
    def getSubject(self):
        sql="SELECT * FROM %s WHERE isSubject='1' ORDER BY `date` DESC"%(self.percentage)
        try:
            self.dict_cursor.execute(sql)
            MysqlData=self.dict_cursor.fetchall()
            return MysqlData
        except MySQLdb.Error as e: 
            print e
            logging.exception("parseGos") 
        
    def getCanPerfomance(self,startdate,endDate):
        sql="SELECT * FROM `%s` WHERE `isSubject`=1 and `builded` is NULL and `date` <='%s' and `date` >= '%s' ORDER BY `date` DESC"%\
        (self.percentage,startdate,endDate)
        
        try:
            self.dict_cursor.execute(sql)
            MysqlData=self.dict_cursor.fetchall()
            return MysqlData
        except MySQLdb.Error as e: 
            print e
            logging.exception("parseGos")         
        pass 
    def getCanPrecision(self,startdate,endDate):
        sql="SELECT * FROM `%s` WHERE `is_oraclet`=1 and `precision_build` is NULL and `date` <='%s' and `date` >= '%s' ORDER BY `date` DESC"%\
        (self.percentage,startdate,endDate)
        try:
            self.dict_cursor.execute(sql)
            MysqlData=self.dict_cursor.fetchall()
            return MysqlData
        except MySQLdb.Error as e: 
            print e
            logging.exception("parseGos")         
        pass    
    def getAllcanPrecision(self):
        sql="SELECT * FROM `%s` WHERE `is_oraclet`=1 and `precision_build` is NULL ORDER BY `date` DESC"%\
        (self.percentage)
        try:
            self.dict_cursor.execute(sql)
            MysqlData=self.dict_cursor.fetchall()
            return MysqlData
        except MySQLdb.Error as e: 
            print e
            logging.exception("parseGos")         
        pass         
    def getCanRePrecision(self):
        sql="SELECT * FROM `%s` WHERE `oracletT_F`=0 and `reBuild` is NULL ORDER BY `date` DESC"%\
        (self.percentage)
        try:
            self.dict_cursor.execute(sql)
            MysqlData=self.dict_cursor.fetchall()
            return MysqlData
        except MySQLdb.Error as e: 
            print e
            logging.exception("parseGos")         
        pass    
    def getAllCanPerfomance(self):
        sql="SELECT * FROM `%s` WHERE `isSubject`=1 and `builded` is NULL ORDER BY `date` DESC"%\
        (self.percentage)
        try:
            self.dict_cursor.execute(sql)
            MysqlData=self.dict_cursor.fetchall()
            return MysqlData
        except MySQLdb.Error as e: 
            print e
            logging.exception("parseGos")         
        pass        
    def updateisSubject(self,data,isSubject):
        sql="UPDATE %s SET isSubject ='%s' WHERE `author`='%s' and date='%s' and title ='%s'" %\
        (self.percentage,str(isSubject),data['author'].encode('utf8'),data['date'].strftime("%Y-%m-%d %H:%M:%S"),data['title'].encode('utf8'))  
        try:
            self.dict_cursor.execute(sql)
            self.db.commit()
        except MySQLdb.Error as e: 
            print e
            logging.exception("parseGos")
    def updateIsOraclet(self,data,isOraclet):
        sql="UPDATE %s SET `is_oraclet` ='%s' WHERE `author`='%s' and date='%s' and title ='%s'"%\
            (self.percentage,str(isOraclet),data['author'].encode('utf8'),data['date'].strftime("%Y-%m-%d %H:%M:%S"),data['title'].encode('utf8'))
        try:    
            self.dict_cursor.execute(sql)
            self.db.commit()
        except MySQLdb.Error as e: 
            print e
            logging.exception("parseGos")             
    def updatePerformance(self,data,type1,remark):
        sql="UPDATE %s SET `builded` ='1',`type`='%s',`Remark`='%s' WHERE `author`='%s' and date='%s' and title ='%s'"%\
        (self.percentage,type1,remark,data['author'].encode('utf8'),data['date'].strftime("%Y-%m-%d %H:%M:%S"),data['title'].encode('utf8'))
        print sql
        try:
            self.dict_cursor.execute(sql)
            self.db.commit()
        except MySQLdb.Error as e: 
            print e
            logging.exception("parseGos")     
    def updatePrecision(self,data,oracletT_F,oraclet_remark):
        sql="UPDATE %s SET `precision_build` ='1',`oracletT_F`='%s',`oraclet_remark`='%s' WHERE `author`='%s' and date='%s' and title ='%s'"%\
        (self.percentage,oracletT_F,oraclet_remark,data['author'].encode('utf8'),data['date'].strftime("%Y-%m-%d %H:%M:%S"),data['title'].encode('utf8'))
        print sql
        try:
            self.dict_cursor.execute(sql)
            self.db.commit()
        except MySQLdb.Error as e: 
            print e
            logging.exception("parseGos") 
    def updateRePrecision(self,data,oracletT_F,oraclet_remark):
        sql="UPDATE %s SET `reBuild` ='1',`oracletT_F`='%s' WHERE `author`='%s' and date='%s' and title ='%s'"%\
        (self.percentage,oracletT_F,data['author'].encode('utf8'),data['date'].strftime("%Y-%m-%d %H:%M:%S"),data['title'].encode('utf8'))
        print sql
        try:
            self.dict_cursor.execute(sql)
            self.db.commit()
        except MySQLdb.Error as e: 
            print e
            logging.exception("parseGos")         

        
        
             
        
        
        