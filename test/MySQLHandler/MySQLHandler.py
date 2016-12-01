# -*- coding:utf-8 -*-
'''
Created on 2016年3月21日

@author: ben
'''
import MySQLdb
import datetime
import logging
import json
class MySQLHandler(object):
    '''
    classdocs
    '''
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
        self.days=7
    def __del__(self):
        self.db.close()
    def setOnePredictPeople(self,name,type):
        sql="INSERT INTO predict_people(predict_people,type) VALUES ('%s','%s')"%\
            (name.encode('utf-8'),str(type))
        try:
            self.dict_cursor.execute(sql)
            self.db.commit()
            return True
        except MySQLdb.Error as e:
            print 'error in getOnePttSource:',e 
            return False
    def getSQL(self,sql):
        try:
            self.dict_cursor.execute(sql)
            MysqlData=self.dict_cursor.fetchall()
            return MysqlData
        except MySQLdb.Error as e: 
            logging.exception("parseGos")
        pass
    def getAllCanUpdatePrice(self,date):
        sql="SELECT * FROM oraclet WHERE `predict_time`<'%s' AND now_price = 0  "%\
        (date.strftime('%Y-%m-%d'))
        try:
            self.dict_cursor.execute(sql)
            MysqlData=self.dict_cursor.fetchall()
            return MysqlData
        except MySQLdb.Error as e: 
            logging.exception("parseGos")
        pass
    def getAllOraclets(self):
        sql="SELECT * FROM oraclet"
        try:
            self.dict_cursor.execute(sql)
            MysqlData=self.dict_cursor.fetchall()
            return MysqlData
        except MySQLdb.Error as e: 
            logging.exception("parseGos")
        pass
    def getAllCanVerifyOraclets(self):
        sql="SELECT * FROM oraclet Where result_status is NULL  AND `occur_time` <'%s' ORDER BY `oraclet`.`number` ASC"%\
        (datetime.datetime.now().date().strftime('%Y-%m-%d'))
        try:
            self.dict_cursor.execute(sql)
            MysqlData=self.dict_cursor.fetchall()
#             print MysqlData
            if len(MysqlData)==0:
                return False
            else:
                return MysqlData
            pass
        except MySQLdb.Error as e: 
            print 'error in getOnePttSource:',e
        pass
    def getPredictPeople(self,name):
        sql="SELECT * FROM `predict_people` WHERE `predict_people`='%s'"%\
            (name.encode('utf8'))
        try:
            self.dict_cursor.execute(sql)
            MysqlData=self.dict_cursor.fetchall()
            print MysqlData
            if len(MysqlData)==0:
                return False
            else:
                return MysqlData
            pass
        except MySQLdb.Error as e: 
            print 'error in getOnePttSource:',e
    def verifyUpdateToDb(self,oraclet):
        for (i, roi) in enumerate(oraclet.roi):
            print i
#             '1' if oraclet.results[i] == True else '0'
            if oraclet.roi!= None:
                sql="INSERT INTO results(o_number,roi,result,week) VALUES ('%s','%s','%s','%s')"\
                    %(str(oraclet.number),str(roi),'1' if oraclet.results[i] == True else '0',str(i+1))
            else:
                sql="INSERT INTO results(o_number,result,week) VALUES ('%s','%s','%s')"\
                    %(str(oraclet.number),'1' if oraclet.results[i] == True else '0',str(i+1))
            print sql   
            try:
                self.dict_cursor.execute(sql)
                self.db.commit()
            except MySQLdb.Error as e:
                print 'error in getOnePttSource:',e             
                pass
    def newVerifyUpdateToDb(self,oraclet):
        oraclet.priceList = json.dumps(oraclet.priceList,indent=1, encoding='utf-8',ensure_ascii=False)
        oraclet.dateList = json.dumps(oraclet.dateList,indent=1, encoding='utf-8',ensure_ascii=False)
        sql="INSERT INTO `new_results`(o_number,result,price_list,date_list) VALUES ('%s','%s','%s','%s')"\
                    %(str(oraclet.number),'1' if oraclet.results == True else '0',oraclet.priceList,oraclet.dateList)
        try:
            self.dict_cursor.execute(sql)
            self.db.commit()
            return True
        except MySQLdb.Error as e:
            return False
            print 'error in getOnePttSource:',e            
    def updateOracletNowprice(self,mysqlOraclet):
        sql="UPDATE `oraclet` SET now_price ='%s' WHERE `number`='%s'"%\
            (str(mysqlOraclet['now_price']),str(mysqlOraclet['number']))
        try:
            self.dict_cursor.execute(sql)
            self.db.commit()
            return True
        except MySQLdb.Error as e:
            print 'error in getOnePttSource:',e 
            return False    
    def updateOracletResults(self,oraclet,result):
        if result==False:
            result=0
        elif result==True:
            result=1
        sql="UPDATE `oraclet` SET results ='%s' WHERE `number`='%s'"%\
            (str(result),str(oraclet.number))
        try:
            self.dict_cursor.execute(sql)
            self.db.commit()
            return True
        except MySQLdb.Error as e:
            print 'error in getOnePttSource:',e 
            return False        
        pass
    def updateOracletResultsForTemp(self,number,result):
        sql="UPDATE `oraclet` SET results ='%s' WHERE `number`='%s'"%\
            (str(result),str(number))
        try:
            self.dict_cursor.execute(sql)
            self.db.commit()
            return True
        except MySQLdb.Error as e:
            print 'error in getOnePttSource:',e 
            return False        
        pass
    def updateOracletResultStatus(self,number,ResultStatus):
        sql="UPDATE `oraclet` SET result_status ='%s' WHERE `number`='%s'"%\
            (str(ResultStatus),str(number))
        try:
            self.dict_cursor.execute(sql)
            self.db.commit()
            return True
        except MySQLdb.Error as e:
            print e 
            return False        
        pass
        pass
    def updatePttsource(self,author,date,message):
        sql="UPDATE `ptt_source` SET  message ='%s' WHERE `author`='%s' AND `date`='%s'"%\
            (message.encode('utf8'),author.encode('utf8'),date.strftime("%Y-%m-%d %H:%M:%S"))
#         print sql
        try:
            self.dict_cursor.execute(sql)
            self.db.commit()
            return True
        except MySQLdb.Error as e:
            print 'error in getOnePttSource:',e 
            return False    
        pass
    def updateOrInsetMessage(self,name,date,time,content,o_number,status):
        tempTime=time.split(' ')
        try:
            tempstr='%s-%s %s'%(date.strftime("%Y"),tempTime[1],tempTime[2])
        except IndexError:
            tempstr='%s-%s %s'%(date.strftime("%Y"),tempTime[0],tempTime[1])
        d = datetime.datetime.strptime(tempstr, '%Y-%m/%d %H:%M')
        sql="INSERT INTO message(name,time,o_number,content,status) VALUES ('%s','%s','%s','%s','%s')"%\
            (name.encode('utf-8'),d.strftime("%Y-%m-%d %H:%M"),
             o_number,content.encode('utf-8'),status.encode('utf-8'))
        try:
            self.dict_cursor.execute(sql)
            self.db.commit()
            return True
        except MySQLdb.Error as e:
            sql="UPDATE `message` SET  content ='%s' WHERE `name`='%s' AND `time`='%s'"%\
            (content.encode('utf-8'),name.encode('utf-8'),d.strftime("%Y-%m-%d %H:%M"))
            try:
                self.dict_cursor.execute(sql)
                self.db.commit()
                return True
            except MySQLdb.Error as e:
                return False
    def getOnePttSource(self,author,date):
#         print author
#         print type(author)
#         print date
#         print type(date)
        sql="SELECT * FROM `ptt_source` WHERE `author`='%s' AND `date`='%s'"%\
            (author.encode('utf8'),date.strftime('%Y-%m-%d %H:%M:%S'))
        print sql
        try:
            self.dict_cursor.execute(sql)
            MysqlData=self.dict_cursor.fetchall()
            print MysqlData
#             print MysqlData
            if len(MysqlData)==0:
#                 print 'ffff'
                return False
            else:
#                 print "tttt"
                return MysqlData
            pass
        except MySQLdb.Error as e: 
            print 'error in getOnePttSource:',e
            pass
        pass
    def getOneOraclet(self,name,date,code,event):
#         需將四個參數都變成字串
        sql="SELECT * FROM `oraclet` WHERE `predict_people`='%s' AND `predict_time`='%s' AND `predict_targetcode`='%s' AND `event_content`='%s'"%\
            (name,date,code,event)
        try:
            self.dict_cursor.execute(sql)
            MysqlData=self.dict_cursor.fetchall()
            return MysqlData
        except MySQLdb.Error as e:
            print 'error in getOnePttSource:',e
            return False
        pass
    def setresultRecord(self,oNumber,date,price):
        sql="INSERT INTO results_record(o_number,date,price) VALUES('%s','%s','%s')"%\
            (oNumber,date.strftime('%Y-%m-%d'),price)
        try:
            self.dict_cursor.execute(sql)
            self.db.commit()
        except MySQLdb.Error as e:
            print 'error in getOnePttSource:',e
    def setOnePttSource(self,d):
        sql="INSERT INTO ptt_source (author,date,title,ip,link,content,message,messageNum)VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%\
            (d['b_author'],d['d_date'].strftime('%Y-%m-%d %H:%M:%S'),d['c_title'],d['e_ip'],d['link'],d['f_content'].decode('utf-8'),d['g_message'],str(d['h_messageNum']).decode('utf-8'))
#         print sql
        try:
            self.dict_cursor.execute(sql)
            self.db.commit()
        except MySQLdb.Error as e:
            print 'error in getOnePttSource:',e
    def setOneNewMessage(self,dateNormalmessage,oracletNumber):
#         還需要拿到O_number
        sql="INSERT INTO message(name,time,o_number,content,status) VALUES ('%s','%s','%s','%s','%s')"%\
                    (dateNormalmessage['id'].encode('utf-8'),dateNormalmessage['date'].strftime("%Y-%m-%d %H:%M"),
                     str(oracletNumber),dateNormalmessage['content'].encode('utf-8'),dateNormalmessage["status"].encode('utf-8'))
        try:
            self.dict_cursor.execute(sql)
            self.db.commit()
        except MySQLdb.Error as e:
            print 'error in getOnePttSource:',e 
    def setNewMessage(self,message,oracletDict):
        oracletNumber=self.getOneOraclet(oracletDict['name'].encode('utf-8'),oracletDict['date'].strftime("%Y-%m-%d"), str(oracletDict['code']),oracletDict['event'].encode('utf-8'))[0]['number']
        for row in message:
            tempTime=row['time'].split(' ')
            row['content']=row['content'].replace(' ','')
            try:
                tempstr='%s-%s %s'%(oracletDict['date'].strftime("%Y"),tempTime[1],tempTime[2])
            except IndexError:
                tempstr='%s-%s %s'%(oracletDict['date'].strftime("%Y"),tempTime[0],tempTime[1])
            row['date'] = datetime.datetime.strptime(tempstr, '%Y-%m/%d %H:%M')
            self.setOneNewMessage(row, oracletNumber)
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
    def setOneOraclet(self,oracletDict):
#         print 'name:',type(oracletDict['name'])
#         print 'date:',type(oracletDict['date'])
#         print 'code:',type(oracletDict['code'])
#         print 'targetName:',type(oracletDict['targetName'])
#         print 'occurTime:',type(oracletDict['occurTime'])
#         print 'event:',type(oracletDict['event'])
#         print 'nowprice:',type(oracletDict['nowprice'])
        sql="INSERT INTO oraclet(predict_people,predict_time,predict_targetcode,predict_targetname,occur_time,event_content,type,\
            now_price)\
            VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" %\
            (oracletDict['name'].encode('utf-8'),oracletDict['date'].strftime("%Y-%m-%d"),oracletDict['code'],oracletDict['targetName'],oracletDict['occurTime'].strftime("%Y-%m-%d"),oracletDict['event'].encode('utf-8'),str(oracletDict['type']),str(oracletDict['nowprice']))
        print sql
        try:
            self.dict_cursor.execute(sql)
            self.db.commit()
        except MySQLdb.Error as e:
            print 'error in getOnePttSource:',e
        pass
    def closeDb(self):
        self.db.close()
if __name__ == '__main__':
    dbHandler=MySQLHandler()
    oracletDict={'code':"2454",'date':datetime.date(2012,8,1),}
    dbHandler.setOneContradiction(oracletDict)
        