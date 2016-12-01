#-*- coding:utf-8 -*-
'''
Created on 2016年3月27日

@author: ben
'''
import csv
import MySQLdb
import time
import datetime
from getWebHandler.getPrices import *
from MySQLHandler.MySQLHandler import MySQLHandler
from oraclets import Oraclet
import logging
from newDbHandler.newGetdbHandler import GetDbHandler
from newDbHandler.newSetDbHandler import SetDbHandler
logging.basicConfig(filename='logging1.txt')
class NewVerifyHandler(object):
    
    '''
    classdocs
    '''


    def __init__(self,twseDict,gtsmDict):
        '''
        Constructor
        '''
        self.dbHandler=MySQLHandler()
        self.getDbHandler=GetDbHandler()
        self.setDbHandler=SetDbHandler()
        self.twseDict=twseDict
        self.gtsmDict=gtsmDict
    def determineAuthenticationSource(self,code):
        if (self.twseDict.get(str(code))!=None):
            return u'上市'                                                         
        if (self.gtsmDict.get(str(code))!=None):
            return u'上櫃' 
        return False
    
    def calculateROI(self,priceList,nowPrice,eventContent):
        ROI=0
#         代表是長期投資，每20筆取一筆即可
        tempPriceList=[]
        if len(priceList)>100:
            tempPriceList.append(priceList[0])
            for i in range(1,7,1):
                tempPriceList.append(priceList[(20*i)-1])
            priceList=tempPriceList
            
        print 'tempPriceList:',  priceList
        for price in priceList:
            price=float(price)
#             print type(price)
#             print type(self.nowPrice)
            ROI+=(price-nowPrice)/nowPrice
        ROI/=len(priceList)
        
        if eventContent==u"賣出":
            ROI=ROI*(-1)
        roi=ROI
        return roi
#     回傳oraclet，roi及result長度為4
    def shorTermROI(self,priceList,oraclet):
        while len(priceList)!=0:
            weekpriceList=[]
            weekpriceList=priceList[:5]
            del priceList[0:5]
            ROI=0
            for price in weekpriceList:
                price=float(price)
#             print type(price)
#             print type(self.nowPrice)
                ROI+=(price-oraclet.nowPrice)/oraclet.nowPrice
            ROI/=len(weekpriceList)
            if oraclet.eventContent==u"賣出":
                ROI=ROI*(-1)
            oraclet.roi.append(ROI)
        return oraclet
    def rankVerify(self,oraclet):
        AuthenType=self.determineAuthenticationSource(oraclet.predictTargetcode)
        if AuthenType==False:
            return False
        if AuthenType==u'上市' :
            getPricrHandler=TwseHandler()
        elif AuthenType==u'上櫃' : 
            getPricrHandler=GtsmHandler()
            
        priceDict=getPricrHandler.getAuthenticationSource2(oraclet.predictTargetcode, oraclet.startDate
                                                          , oraclet.period,oraclet.listLen)
        if priceDict==False:
            return False
        else:
            oraclet.roi=self.calculateROI(priceDict['price'],oraclet.nowPrice,oraclet.eventContent)
            if oraclet.roi!=None:
                if oraclet.roi>0:
                    oraclet.results=True
                else:
                    oraclet.results=False
                oraclet.priceList=priceDict['price']
                oraclet.dateList=priceDict['date']
                return oraclet
            else:
                return False
            
    def foreignTargetPriceVerify(self,oraclet):  
        AuthenType=self.determineAuthenticationSource(oraclet.predictTargetcode)
        if AuthenType==False:
            print 'AuthenType False'
            return False
        if AuthenType==u'上市' :
            getPricrHandler=TwseHandler()
        elif AuthenType==u'上櫃' : 
            getPricrHandler=GtsmHandler()
            
        priceDict=getPricrHandler.getAuthenticationSource2(oraclet.predictTargetcode, oraclet.startDate
                                                          , oraclet.period,oraclet.listLen)
        if priceDict==False:
            print 'priceDict False'
            return False
        else:
            oraclet.priceList=priceDict['price']
            oraclet.dateList=priceDict['date']
            oraclet.results=False
#             5/22修改 要看有沒有錯!!!!!!!
            if float(oraclet.eventContent)>float(oraclet.nowPrice):
                for price in priceDict['price']:
                    if float(price) > float(oraclet.eventContent):
                        oraclet.results=True
                        break
            else:
                for price in priceDict['price']:
                    if float(price) < float(oraclet.eventContent):
                        oraclet.results=True
                        break
            return oraclet
      
      
    
    def OneOracletVerify(self,oraclet):

        self.dbHandler.updateOracletResultStatus(oraclet.number,0)
        if oraclet.eventContent==u'買進' or oraclet.eventContent==u'賣出':
            oraclet=self.rankVerify(oraclet)
#             外資目標價驗證，還沒做~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        else:
            oraclet=self.foreignTargetPriceVerify(oraclet)
            pass
# setresultRecord  一次要更新兩個
        if oraclet != False:
            for idx, date in enumerate(oraclet.dateList):
                temp=date.split('/')
                temp[0]=int(temp[0])+1911
                tempDate=datetime.datetime.strptime(str(temp[0])+temp[1]+temp[2], '%Y%m%d').date()                
                self.dbHandler.setresultRecord(oraclet.number, tempDate, oraclet.priceList[idx]) 
            if self.dbHandler.newVerifyUpdateToDb(oraclet):
                self.dbHandler.updateOracletResults(oraclet, oraclet.results)
                self.dbHandler.updateOracletResultStatus(oraclet.number,1)
#                 更新預測人預測準確率(未驗證)
#                 predictorData=self.getDbHandler.getOnePredictorAccuracy(oraclet.predictPeople)[0]
#                 OracletCount=self.getDbHandler.getPredictorOracletCount(oraclet.predictPeople)[0]
#                 self.setDbHandler.updatePredictorStatus(predictorData['predict_people'], OracletCount[0]['count'],
#                                             predictorData['count'], predictorData['sum'],
#                                             predictorData['accuracy'])
                print "true---------------------------"
            pass
        
        
    def main(self):
#         從資料庫撈取results等於null，且發生日期小於今天
        MysqlData=self.dbHandler.getAllCanVerifyOraclets()
        x=0
        for record in MysqlData:
            print 'record:',record
            oraclet=Oraclet(record)
            self.OneOracletVerify(oraclet)
            pass
            x+=1
            if x==1000:
                break
#         pass  
def csvToList(filePath):
    f=open(filePath,'r')
    codeList=[]
    nameList=[]
    resultDict={}
    for row in csv.reader(f):
        codeList.append(row[0])
        nameList.append(row[1])
        resultDict[row[0]]=row[1]
    f.close()
    return resultDict 
if __name__ == '__main__':
    twseDict=csvToList('../data/twseStockList.csv')
    gtsmDict=csvToList('../data/gtsmStockList.csv')
    verify=NewVerifyHandler(twseDict,gtsmDict)
    verify.main()