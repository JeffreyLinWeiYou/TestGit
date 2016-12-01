# coding=UTF-8
'''
Created on 2015年12月27日
PTT卜卦立案
@author: ben
'''
import MySQLdb
from pandas import Series,DataFrame
import pandas as pd
import datetime
from _mysql import NULL
import csv
from getWebHandler.getPrices import *
import re
gtsmCodeList=[]
gtsmNameList=[]
twseCodeList=[]
twseNameList=[]
twseDict={}
gtsmDict={}
def findCode(str):
    tempList=re.findall('(?<![0-9])[0-9]{1,6}(?![0-9])',str)
#     print tempList
#     global twseStockList

    if len(tempList)==1:
        
        if (twseDict.get(tempList[0].encode('utf-8'))!=None):
            return [tempList[0].encode('utf-8'),twseDict.get(tempList[0].encode('utf-8')),5]
                                                            
        if (gtsmDict.get(tempList[0].encode('utf-8'))!=None):
            return [tempList[0].encode('utf-8'),gtsmDict.get(tempList[0].encode('utf-8')),6]
            pass
        pass

    return False
def readPttSource():
    try:
        global db
        sql="SELECT * FROM ptt_source where `builded` IS NULL"
        cursor=db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
          
    except MySQLdb.Error as e:
        Log.i("Error %d- %s in readForeignSource" % (e.args[0],e.args[1]))
    sqlcode=[]
    sqlPrdict=[]
    sqlCompany=[]
    sqlType=[]
    sqlDate=[]
    sqlPttDate=[]
    sqlPttAuthor=[]
    sqlEvent=[]
    sqlOccurTime=[]  
    
    print len(results)
    for record in results:
#         print record[0]
        codes=findCode(record[2])
        if codes ==False:
            continue
        sqlPttAuthor.append(record[0])        
        sqlPrdict.append(record[0].split(u'(')[0])
        sqlPttDate.append(record[1])
        sqlDate.append(record[1].date())
        sqlcode.append(codes[0])
        sqlCompany.append(codes[1]) 
        sqlType.append(codes[2])
        sqlEvent.append(u"買進")
        sqlOccurTime.append(record[1].date()+datetime.timedelta(days = 10))
    data={'predictPeople':sqlPrdict,'predictTime':sqlDate,'predictTargetCode':sqlcode
          ,'predictTargetName':sqlCompany,'type':sqlType,'eventConten':sqlEvent}
    frameData=DataFrame(data)
    frameData['occurTime']=sqlOccurTime
    frameData['nowPrice']=NULL
    frameData['pttTime']=sqlPttDate
    frameData['pttAuthor']=sqlPttAuthor
    print frameData
    return frameData
#     print sqlcode
#     print sqlCompany
def normalizeData(data):
    n=0
    gtsmHandler=GtsmHandler()
    twseHandler=TwseHandler()
    for index,row in data.iterrows():
        
        if row[5] == 5:
            data.loc[index,u'nowPrice']=twseHandler.getNowPrice(row[4],row[2])
             
        if row[5] == 6:
            data.loc[index,u'nowPrice']=gtsmHandler.getNowPrice(row[4],row[2])  
        if data.loc[index,u'nowPrice']!=False:
            row[7]=data.loc[index,u'nowPrice']
            insertTodb(index, row)
        else:
            Log.i("FalseCode:%s in getPrice" % (row[2]))
            pass
#         n+=1
#         if n>100:
#         break 
    data.to_csv("test1.csv", sep=',', encoding='utf-8')          
#     print data
def insertTodb(index,row):
    try:
#             print 'hasRank'
        for temp in row:
            print temp,',',type(temp)
            
        sql="INSERT INTO oraclet(predict_people,predict_time,predict_targetcode,predict_targetname,occur_time,event_content,type,\
            now_price)\
            VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" %\
            (row[1].encode('utf-8'),row[4].strftime("%Y-%m-%d"),str(row[2]),row[3],row[6].strftime("%Y-%m-%d"),row[0].encode('utf-8'),str(row[5]),str(row[7]))
#             print sql
        cursor.execute(sql)
        db.commit()
        sql="UPDATE ptt_source SET builded = 1 WHERE date = '%s' AND author = '%s'"\
            %(unicode(row[8]).encode('utf-8'),row[9].encode('utf-8'))
        print sql
        cursor.execute(sql)
        db.commit()
    except MySQLdb.Error as e:
        Log.i("Error %d- %s in insertTodb-Rank" % (e.args[0],e.args[1]))
    pass
def csvToList():
    f=open('../data/twseStockList.csv','r')
    global  twseCodeList
    global  twseNameList
    global  twseDict
    for row in csv.reader(f):
        twseCodeList.append(row[0])
        twseNameList.append(row[1])
        twseDict[row[0]]=row[1]
#         print row[0]
    f.close()
    
    f=open('../data/gtsmStockList.csv','r')
    global  gtsmCodeList
    global  gtsmNameList
    global  gtsmDict
    for row in csv.reader(f):
        gtsmCodeList.append(row[0])
        gtsmNameList.append(row[1])
        gtsmDict[row[0]]=row[1]
#         print row[0]
    f.close()
if __name__ == '__main__':
    global db
    db=MySQLdb.connect("140.118.7.42","s8107072004","ben60514","test",charset='utf8')
    global cursor
    cursor =db.cursor()
    csvToList(); 
    frameData=readPttSource()
    frameData=normalizeData(frameData)
#     str=u"[標的]2357鑽全(空)"
#     print findCode(str)
#     print twseDict.get('2357')
#     print twsedict
    db.close()

    pass