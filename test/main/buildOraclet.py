# coding=UTF-8
'''
Created on 2015年12月11日
外資卜卦立案
@author: ben
'''
import MySQLdb
from pandas import Series,DataFrame
import pandas as pd
import datetime
from _mysql import NULL
import csv
from getWebHandler.getPrices import *



posRankList=[]
negRankList=[]
gtsmStockList=[]
twseStockList=[]
    
def readForeignSource():
    try:
        db=MySQLdb.connect("140.118.7.46","s8107072004","ben60514","crawler_test",charset="utf8")
        sql="SELECT * FROM foreign_original Where builded is NULL or targetPriceBuilded is NULL"
        cursor=db.cursor()
        cursor.execute(sql)
        
        results = cursor.fetchall()
        sqlDate=[]
        sqlcode=[]
        sqlcompany=[]
        sqltraderCompany=[]
        sqlOriginalRate=[]
        sqlriseOrDrop=[]
        sqlnewRate=[]
        sqlnewTargetPrice=[]
        sqltype=[]
        sqlTargetBuildList=[]
        for record in results:
            sqlDate.append(str(record[0]))
            sqlcode.append(record[1]) 
            if str(record[1]) in twseStockList:
                sqltype.append(1)  
            elif str(record[1]) in gtsmStockList:
                sqltype.append(3)
            else:
                sqltype.append(10)
            sqlcompany.append(record[2])
            sqltraderCompany.append(record[3])
            sqlOriginalRate.append(record[4])
            sqlriseOrDrop.append(record[5])
            sqlnewRate.append(record[6])
            sqlTargetBuildList.append(record[13])          
            sqlnewTargetPrice.append(record[9])
        print len(results)
        data={'predictPeople':sqltraderCompany,'predictTime':sqlDate,
              'predictTargetCode':sqlcode,'predictTargetName':sqlcompany,
              'eventConten':sqlnewRate}
        frameData=DataFrame(data)
        
        frameData['type']=sqltype
        frameData['occurTime']=NULL
        frameData['nowPrice']=NULL
        frameData['newTargetPrice']=sqlnewTargetPrice
        frameData['sqlTargetBuild']=sqlTargetBuildList
        frameData.to_csv("test.csv", sep=',', encoding='utf-8')
        print frameData
        return frameData
    except MySQLdb.Error as e:
        Log.i("Error %d- %s in readForeignSource" % (e.args[0],e.args[1]))
#         print "Error %d: %s" % (e.args[0],e.args[1])    
    pass

def normalizeData(data):
    n=0
    gtsmHandler=GtsmHandler()
    twseHandler=TwseHandler()
    for index,row in data.iterrows():
        d = datetime.datetime.strptime(row[4], '%Y%m%d')
        d=datetime.date(d.year,d.month,d.day)
        data.loc[index,u'predictTime']=d
        row[4]=d        
        data.loc[index,u'occurTime']=d+datetime.timedelta(days = 370)
        row[6]=d+datetime.timedelta(days = 370)
        if str(row[2]) in twseStockList:
            data.loc[index,u'nowPrice']=twseHandler.getNowPrice(d,row[2])
        if str(row[2]) in gtsmStockList:
            data.loc[index,u'nowPrice']=gtsmHandler.getNowPrice(d,row[2])
        
        row[7]=data.loc[index,u'nowPrice']
        if data.loc[index,u'nowPrice']!=False:
            insertTodb(index, row)
            pass
#         n+=1
#         if n>50:
#             break
         
def insertTodb(index,row):
    global  posRankList
    global  negRankList
    row[0]=row[0].encode('utf-8').strip().lstrip().rstrip(',')
    
    if row[0] in posRankList:
        row[0]="買進"
        hasRank=True
    elif row[0] in negRankList:
        row[0]="賣出"
        hasRank=True
    else:
        hasRank=False
#     print row[9]
    if row[9]!=1.0 and row[8] > 0:
        try:
#             print 'target'
            sql="INSERT INTO oraclet(predict_people,predict_time,predict_targetcode,predict_targetname,occur_time,event_content,type,\
                now_price)\
                VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" %\
                (row[1].encode('utf-8'),row[4].strftime("%Y-%m-%d"),str(row[2]),row[3].encode('utf-8'),row[6].strftime("%Y-%m-%d"),str(row[8]),str(row[5]+1),str(row[7]))
            cursor.execute(sql)
            db.commit()
            sql="UPDATE foreign_original SET targetPriceBuilded = 1 WHERE date = %s AND code = %s AND traderCompany = '%s'"\
                    %(row[4].strftime("%Y%m%d"),str(row[2]),row[1].encode('utf-8'))
            cursor.execute(sql)
            db.commit()
            
        except MySQLdb.Error as e:
            Log.i("Error %d- %s in insertTodb-target" % (e.args[0],e.args[1]))
    #評等卜卦    
    if hasRank==True:
        try:
#             print 'hasRank'
            sql="INSERT INTO oraclet(predict_people,predict_time,predict_targetcode,predict_targetname,occur_time,event_content,type,\
                now_price)\
                VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" %\
                (row[1].encode('utf-8'),row[4].strftime("%Y-%m-%d"),str(row[2]),row[3].encode('utf-8'),row[6].strftime("%Y-%m-%d"),row[0],str(row[5]),str(row[7]))
#             print sql
            cursor.execute(sql)
            db.commit()
            sql="UPDATE foreign_original SET builded = 1 WHERE date = %s AND code = %s AND traderCompany = '%s'"\
                %(row[4].strftime("%Y%m%d"),str(row[2]),row[1].encode('utf-8'))
            cursor.execute(sql)
            db.commit()
        except MySQLdb.Error as e:
            Log.i("Error %d- %s in insertTodb-Rank" % (e.args[0],e.args[1]))
    
    pass  
#
def csvToList():
    f=open('../data/positiveRank.csv','r')
    global  posRankList
    for row in csv.reader(f):
        posRankList.append(row[0])
        print row[0]
    f.close()
    
    f=open('../data/negativeRank.csv','r')
    global  negRankList
    for row in csv.reader(f):
        negRankList.append(row[0])
        print row[0]
    f.close()
    
    f=open('../data/twseStockList.csv','r')
    global  twseStockList
    for row in csv.reader(f):
        twseStockList.append(row[0])
#         print row[0]
    f.close()
    
    f=open('../data/gtsmStockList.csv','r')
    global  gtsmStockList
    for row in csv.reader(f):
        gtsmStockList.append(row[0])
#         print row[0]
    f.close()
    
    
    
if __name__ == '__main__':
    global db
    db=MySQLdb.connect("140.118.7.46","s8107072004","ben60514","crawler_test",charset='utf8')
    global cursor
    cursor =db.cursor()
    csvToList(); 

    frameData=readForeignSource()
#     frameData=normalizeData(frameData)
    db.close()  
#     getNowPrice(datetime.date(2011,12,7),3034)
    pass