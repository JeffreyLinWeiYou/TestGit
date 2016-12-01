# -*- coding:utf-8 -*-
'''
Created on 2016年3月11日

@author: ben
'''
import datetime
import json
import MySQLdb
from pandas.core.frame import DataFrame
import re
class SetOracletHandler(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    @staticmethod     
    def MysqlToDataframe(MysqlData):
        date=[]
        name=[]
        event=[]
        code=[]
        for record in MysqlData:
            date.append(record["predict_time"])
            name.append(record["predict_people"])
            event.append(record["event_content"])
            code.append(record["predict_targetcode"])
        data={'name':name,'date':date,'event':event,'code':code}
        frameDate=DataFrame(data)
        return frameDate
    
    @staticmethod
    def normalizeMessage(messagestr):
#         print messagestr
        message = json.loads(messagestr)
#         message=[]
        result=[]
        repeat=[]
#         for i in range(1,500,1):
#             try:
#                 message.append(d[str(i)])
#                 pass
#             except KeyError, e:
#                 pass
        for idx, val in enumerate(message):
            val['content']=val['content'].replace(u":",u"")
            temp=val
            for idx2,val2 in enumerate(message):
                if idx>=idx2:
                    continue
                if idx2 in repeat:
                    continue
                if val['id']==val2['id']:
                    repeat.append(idx2)
                    temp['content']+=','+val2['content'].replace(u":",u"")
            if not idx in repeat:        
                result.append(temp)               
#         print len(result)
#         for temp in result:
#             print 'id:',temp['id']
#             print 'content:',temp['content']
        return result
    
    
    @staticmethod
    def setMessageToDb():
        db=MySQLdb.connect("140.118.7.42","s8107072004","ben60514","test",charset="utf8")
        sql="SELECT * FROM ptt_source ORDER BY RAND() LIMIT 0,1000"
        dict_cursor = db.cursor(MySQLdb.cursors.DictCursor)
        dict_cursor.execute(sql)
        mysqlData=dict_cursor.fetchall()
        for record in mysqlData:
#             print record
            print record['number']
            print record['date']
            print record['date']
            messagestr=record['message'].replace('\\','')
#             messagestr=messagestr.encode('utf8')
#             print messagestr
#             print type(messagestr)
            message=SetOracletHandler.normalizeMessage(messagestr)
#             print "message:",message
#             print record['title']
            try:
                code=re.findall('(?<![0-9])[0-9]{1,6}(?![0-9])',record['title'])[0]
            except IndexError:
                continue
            print "code:",code
            sql="SELECT number FROM oraclet WHERE `predict_people`='%s' AND `predict_time`='%s' AND `predict_targetcode`='%s' AND type >4"%\
                    (record['author'].split(u'(')[0],record['date'].strftime("%Y-%m-%d"),str(code))
            print sql
            dict_cursor.execute(sql)
            number=dict_cursor.fetchone()
            if number==None:
                print 'flase'
                continue
#             print type(number['number'])
#             print number['number']

            
            d = datetime.datetime.strptime('2010-11-16 20:10:58', '%Y-%m-%d %H:%M:%S')
            for row in message:
#                 時間做處理!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!測試塞的資料塞的對不對
                try:
                    print record['number']
                    print row['time']
                    tempTime=row['time'].split(' ')
                    row['content']=row['content'].replace(' ','')
                    try:
                        tempstr='%s-%s %s'%(record['date'].strftime("%Y"),tempTime[1],tempTime[2])
                    except IndexError:
                        tempstr='%s-%s %s'%(record['date'].strftime("%Y"),tempTime[0],tempTime[1])
                    d = datetime.datetime.strptime(tempstr, '%Y-%m/%d %H:%M')
#                     print type(row["status"].encode('utf-8'))
#                     row["status"]=row["status"].encode('utf-8')
                    sql="INSERT INTO message(name,time,o_number,content,status) VALUES ('%s','%s','%s','%s','%s')"%\
                    (row['id'].encode('utf-8'),d.strftime("%Y-%m-%d %H:%M"),str(number['number']),row['content'].encode('utf-8'),row["status"].encode('utf-8'))
                    print sql
                    dict_cursor.execute(sql)
                    db.commit()
                    pass
                except MySQLdb.Error as e:
                    print e
                    
                    pass
#             break
        db.close()
        pass
    #檢查是不是有矛盾卜卦，有的話hasContradiction變成true   
    @staticmethod    
    def setContradiction():
        db=MySQLdb.connect("140.118.7.42","s8107072004","ben60514","crawler_test",charset="utf8")
        sql="SELECT * FROM `oraclet` WHERE `hasContradiction` IS NULL AND (`event_content`='買進' OR `event_content`='賣出')"
        dict_cursor = db.cursor(MySQLdb.cursors.DictCursor)
        dict_cursor.execute(sql)
        MysqlData=dict_cursor.fetchall()
        for record in MysqlData:
            sql ="SELECT * FROM `oraclet` WHERE `predict_targetcode`='%s' AND `predict_time`='%s' AND `results` IS NOT NULL AND `type`!= 2 AND `type`!=4"\
             % (record['predict_targetcode'],record['predict_time'])
            dict_cursor.execute(sql) 
            data=dict_cursor.fetchall()
            
            if  len(data)>1:
                print "/n"
                for temp in data:
                    print temp['predict_time'].strftime("%Y-%m-%d")
                    sql="UPDATE `oraclet` SET hasContradiction = true WHERE `predict_people` = '%s' AND `predict_time` = '%s' AND `predict_targetcode` = %s AND `event_content` = '%s'"\
                        %(temp['predict_people'].encode('utf8'),temp['predict_time'].strftime("%Y-%m-%d"),str(temp['predict_targetcode']),temp['event_content'].encode('utf8'))
                    print sql
                    dict_cursor.execute(sql)
                    db.commit()
        db.close()
#         print grouped
        pass
if __name__ == '__main__':
    SetOracletHandler.setMessageToDb()  