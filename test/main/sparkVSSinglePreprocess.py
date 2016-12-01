# -*- coding:utf-8 -*-
'''
Created on 2016年6月8日

@author: ben
'''
import MySQLdb
import datetime
import logging
import json
if __name__ == '__main__':
    ip="140.118.7.46"
    account="s8107072004"
    password="ben60514"
    schema="spark_test"
    db=MySQLdb.connect(ip,account,password,schema,charset='utf8')
    dict_cursor = db.cursor(MySQLdb.cursors.DictCursor)
#     sql="select * from oraclet as o,predict_people as p where o.predict_people=p.predict_people and p.type=1 and o.`occur_time` <'%s' and o.`result_status`is  NULL order by rand() limit 500"%\
#         (datetime.datetime.now().date().strftime('%Y-%m-%d'))
    sql="select * from oraclet as o,predict_people as p where o.predict_people=p.predict_people  and o.`occur_time` <'%s' and o.`result_status`is  NULL"%\
        (datetime.datetime.now().date().strftime('%Y-%m-%d'))
    x=0
    start =datetime.datetime.now()
    try:    
        dict_cursor.execute(sql)
        MysqlData=dict_cursor.fetchall()
        
        print len(MysqlData)
#         for sqlData in MysqlData:
#             print sqlData
# #             刪除new_results
#             sql="DELETE FROM `new_results` WHERE `o_number`=%s"%\
#                 (sqlData['number'])
#             dict_cursor.execute(sql)
# #             刪除results_record                
#             sql="DELETE FROM `results_record` WHERE `o_number`=%s"%\
#                 (sqlData['number'])
#             dict_cursor.execute(sql)
# #             oraclet 的result_status、results設成null                
#             sql="update `oraclet` SET `result_status`=NULL,`results`=NULL where number='%s' "%\
#                 (sqlData['number'])
#                  
#             dict_cursor.execute(sql)
#             db.commit()
#             x+=1
#             if x==1:
#                 break
        endTime =datetime.datetime.now()
        print 'startTime:',start
        print 
        
    
    except MySQLdb.Error as e: 
        print 'error in getOnePttSource:',e    
    pass