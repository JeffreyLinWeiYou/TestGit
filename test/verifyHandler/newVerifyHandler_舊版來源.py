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
            return
        if AuthenType==u'上市' :
            getPricrHandler=TwseHandler()
        elif AuthenType==u'上櫃' : 
            getPricrHandler=GtsmHandler()
            
        priceList=getPricrHandler.getAuthenticationSource(oraclet.predictTargetcode, oraclet.startDate
                                                          , oraclet.endDate, oraclet.period)
        while len(priceList)>oraclet.listLen:
            priceList.pop()
        if u'--' in priceList:
            logging.warning(str(oraclet.number)+',reason:--')
            return False
        print priceList
        print len(priceList)
        if len(priceList)==oraclet.listLen:
            if oraclet.listLen==20:
                oraclet=self.shorTermROI(priceList,oraclet)
                for roi in oraclet.roi:
                    if roi>0:
                        oraclet.results.append(True)
                    else:
                        oraclet.results.append(False)
            else:
                oraclet.roi.append(self.calculateROI(priceList,oraclet.nowPrice,oraclet.eventContent))
                if oraclet.roi!=None:
                    if oraclet.roi[0]>0:
                        oraclet.results.append(True)
                    else:
                        oraclet.results.append(False)
            return oraclet
        else:
            return False            
      
      
    
    def OneOracletVerify(self,oraclet):
        self.dbHandler.updateOracletResults(oraclet,0)
        if oraclet.eventContent==u'買進' or oraclet.eventContent==u'賣出':
            oraclet=self.rankVerify(oraclet)
#             外資目標價驗證，還沒做~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        else:
            pass

#         update到卜卦庫，還沒做~~
        if oraclet != False:
            print oraclet.roi
            print oraclet.results
            self.dbHandler.verifyUpdateToDb(oraclet)
            self.dbHandler.updateOracletResults(oraclet,1)
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
#             x+=1
#             if x==10:
#                 break
        pass  
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