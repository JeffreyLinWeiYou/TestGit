# coding=UTF-8
'''
Created on 2016年1月10日

@author: ben
'''
import MySQLdb
import time
import datetime
from getWebHandler.getPrices import *
class VerifyHandler(object):
    '''
    classdocs
    '''


    def __init__(self,row,db):
        self.predictPeople=row[0]
        self.prdictTime=row[1]
        self.predictTargetCode=row[2]
        self.predictTargetName=row[3]
        self.OccurTime=row[4]
        self.eventContent=row[5]
        self.type=row[6]
        self.nowPrice=row[7]
        self.result=None
        self.ROI=None
        self.db=db
    def calculateROI(self,priceList):
        ROI=0
        for price in priceList:
            price=float(price)
#             print type(price)
#             print type(self.nowPrice)
            ROI+=(price-self.nowPrice)/self.nowPrice
        ROI/=len(priceList)
        if self.eventContent==u"賣出":
            ROI=ROI*(-1)
        self.ROI=ROI
        
    def foreignRankVerify(self):
        startDate=self.prdictTime+datetime.timedelta(days = 180)
        endDate=self.prdictTime+datetime.timedelta(days = 365)
        if self.type==1:
            getPricrHandler=TwseHandler()
        if self.type==3:
            getPricrHandler=GtsmHandler()    
        priceList=getPricrHandler.getAuthenticationSource(self.predictTargetCode, startDate, endDate, 30)
        if len(priceList)==6:
            self.calculateROI(priceList)
            if self.ROI!=None:
                if self.ROI>0:
                    self.result=True;
                else:
                    self.result=False;
        else:
            #尚未測試過
            Log.i("foreignErrorLen %d-in %s,%s,%d" % (len(priceList),self.predictPeople.encode('utf-8'),self.prdictTime.strftime('%Y-%m-%d'),self.predictTargetCode))
    def foreignTargetPriceVerify(self):
        startDate=self.prdictTime
        endDate=self.prdictTime+datetime.timedelta(days = 360)
        if self.type==2:
            getPricrHandler=TwseHandler()
        if self.type==4:
            getPricrHandler=GtsmHandler()
        priceList=getPricrHandler.getAuthenticationSource(self.predictTargetCode, startDate, endDate, 1)   
        self.result=False
        print self.eventContent
        #比較要注意型態
        for price in priceList:
            if float(price) > float(self.eventContent):
#                 print price
                self.result=True
                
    def pTTRankVerify(self):
        startDate=self.prdictTime
        endDate=self.prdictTime+datetime.timedelta(days = 16)
        if self.type==5:
            getPricrHandler=TwseHandler()
        if self.type==6:
            getPricrHandler=GtsmHandler()
        priceList=getPricrHandler.getAuthenticationSource(self.predictTargetCode, startDate, endDate, 1)
        #還需做將priceList第七個元素以後的都刪掉(有做)
#         print len(priceList)
        while len(priceList)>7:
            priceList.pop()
        print priceList    
        if len(priceList)==7:
            self.calculateROI(priceList)
            if self.ROI!=None:
                if self.ROI>0:
                    self.result=True;
                else:
                    self.result=False;
        else:
            #尚未測試過
            Log.i("PTTErrorLen %d-in %s,%s,%d" % (len(priceList),self.predictPeople.encode('utf-8'),self.prdictTime.strftime('%Y-%m-%d'),self.predictTargetCode))
        pass   
    def updateToDb(self):
        try:
            if self.result!=None:
                cursor =self.db.cursor()
                #type1356
                if self.ROI!=None:
                    sql="UPDATE oraclet SET results = %s, roi = %s WHERE predict_people = '%s' AND predict_time = '%s' AND predict_targetcode = %d AND event_content='%s'"\
                    %(self.result,str(self.ROI),self.predictPeople.encode('utf-8'),self.prdictTime.strftime("%Y-%m-%d"),self.predictTargetCode,self.eventContent.encode('utf-8'))
                    cursor.execute(sql)
                    db.commit()
                else:
                    sql="UPDATE oraclet SET results = %s WHERE predict_people = '%s' AND predict_time = '%s' AND predict_targetcode = %d AND event_content='%s'"\
                    %(self.result,self.predictPeople.encode('utf-8'),self.prdictTime.strftime("%Y-%m-%d"),self.predictTargetCode,self.eventContent.encode('utf-8'))
                    cursor.execute(sql)
                    db.commit()
                    pass
        except MySQLdb.Error as e:
            Log.i("Error %d- %s in VerifyHandler" % (e.args[0],e.args[1]))                   
                 
    def main(self):
        if self.type==1 or self.type==3:
            self.foreignRankVerify()
        if self.type==2 or self.type==4:
            self.foreignTargetPriceVerify()
        if self.type==5 or self.type==6:
            self.pTTRankVerify()
        print self.ROI
        print self.result
        #還需作將驗正完的資料update到資料庫
        self.updateToDb()
        pass    

        
        
        
if __name__ == '__main__':
    db=MySQLdb.connect("140.118.7.46","s8107072004","ben60514","crawler_test",charset='utf8')
    cursor =db.cursor()   
    sql="SELECT * FROM oraclet Where results1 is NULL "
    cursor=db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    for record in results:
        if datetime.datetime.now().date()>record[4]:
            print record
        try:
            verify=VerifyHandler(record,db)
            verify.main()
        except:
            Log.i("Error-in VerifyHandler: %s,%s,%d,%s" % (record[0].encode('utf-8'),record[1].strftime('%Y-%m-%d'),record[2],record[5].encode('utf-8')))
            pass
        
    db.close()    
        