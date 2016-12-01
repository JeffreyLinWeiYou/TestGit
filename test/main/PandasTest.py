#-*- coding:utf-8 -*-
#撈取鉅亨網資料
import pandas as pd
import MySQLdb
import time
import datetime
'''
Created on 2015年10月23日

@author: ben
'''

if __name__ == '__main__':
    stop=False
    nowDate=datetime.date.today()
    endDate=datetime.date(2012,01,01) 
    temp=nowDate-endDate
    db=MySQLdb.connect("140.118.7.46","s8107072004","ben60514","test",charset='utf8')
    cursor =db.cursor()
    while temp.days>0:
        firstDate=nowDate
        secondDate=nowDate-datetime.timedelta(days=30)
#         print "firstDate=",firstDate
#         print "secondDate=",secondDate
        i=1
        while True:
            try:
                url = "http://www.cnyes.com/twstock/twstock_qfii_sc.asp?x=33&y=13&id=&tel=&selpage=%d&ratetype=QFII&ratedate1=%s&ratedate2=%s&sortorder=date"%\
                (i,secondDate.strftime('%Y%m%d'),nowDate.strftime('%Y%m%d'))
                print url
                data = pd.read_html(url)
                frameData=data[len(data)-3][2:]
                #print frameData
#                 print frameData
                i+=1
            except:
                break
            for index,row in frameData.iterrows():
#                     sql="INSERT INTO foreign_original(date,code,company,traderCompany,originalRate,riseOrDrop,newRate,\
#                         EPS,oldTargetPrice,newTargetPrice,nowPrice,remark)\
#                         VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %\
#                         (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11])
#                     try:
#                         cursor.execute(sql)
#                         db.commit()
#                     except MySQLdb.Error as e:
#                         print "Error %d: %s" % (e.args[0], e.args[1])
                    print type(row[10])
                    print row[10]
                  
        break
        
        nowDate=nowDate-datetime.timedelta(days=31)
        temp=nowDate-endDate
    db.close()   
        
    
    
#     print type(temp.days)
#     print temp.days
#     
#     print nowDate.strftime('%Y%m%d')
#     print type(nowDate)
    url = 'http://www.cnyes.com/twstock/twstock_qfii_sc.asp?x=33&y=13&id=&tel=&selpage=2&ratetype=QFII&ratedate1=20150708&ratedate2=20151023&sortorder=date'
    #http://www.cnyes.com/twstock/twstock_qfii_sc.asp?x=33&y=13&id=&tel=&selpage=2&ratetype=QFII&ratedate1=20150708&ratedate2=20151023&sortorder=date
#    data = pd.read_html(url)
#    print len(data)
#    frameData=data[len(data)-3]
#    print (frameData.iloc[[2]])[0]
#    print type(frameData.iloc[[2]])


#     db=MySQLdb.connect("140.118.7.46","s8107072004","ben60514","crawler_test",charset='utf8')
#     cursor =db.cursor()
#     sql="INSERT INTO foreign_original(date,code,company,traderCompany,originalRate,riseOrDrop,newRate,\
#          EPS,oldTargetPrice,newTargetPrice,nowPrice,remark)\
#          VALUES ('%d','%d','%s','%s','%s','%s','%s','%s','%f','%f','%f','%s')" %\
#          (20150713,2382,'廣達','麥格理','--','首次','超越市場表現','--',0,86,57.10,'--')
#     try:
#         cursor.execute(sql)
#         db.commit()
#     except MySQLdb.Error as e:
#         print "Error %d: %s" % (e.args[0], e.args[1])
#     db.close()
         
    #print type(data[len(data)-3])
    #print data[len(data)-3]

    #data[0]
    
    pass