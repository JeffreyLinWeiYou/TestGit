# coding=UTF-8
'''
Created on 2015年12月15日

@author: ben
'''
import pandas as pd
from pandas import Series,DataFrame
import requests
import datetime
from bs4 import BeautifulSoup 
import json
from log.logHelper import *
#上市公司
class TwseHandler():
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        pass
    def addMonth(self,date):
        tempMonth=date.month+1 
        if(tempMonth>12):
            tempMonth=1
            tempYear=date.year+1
        else:
            tempYear=date.year
        if(date.day>28):
            tempDay=28
        else:
            tempDay=date.day
    #     print 'year:',tempYear
    #     print 'month:',tempMonth
    #     print 'day:',tempDay
        return datetime.date(tempYear,tempMonth,tempDay)
    def getWebToDataframe2(self,code,year,month):
        tempStartDate=datetime.date(year,month,1)
        resultFrameData=DataFrame()
        url = "http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/genpage/Report%s/%s_F3_1_8_%d.php?STK_NO=%d&myear=%s&mmon=%s"%\
        (tempStartDate.strftime('%Y%m'),tempStartDate.strftime('%Y%m'),code,code,tempStartDate.strftime('%Y'),tempStartDate.strftime('%m'))
        print url
        try:
            data = pd.read_html(url)
#       HTTP Error 404 
        except :
            return DataFrame()
        frameData=data[len(data)-2].drop([0])
        try:
            frameData1=DataFrame(frameData.values,index=frameData[0].get_values(),columns=frameData.iloc[0].get_values())
#       網頁是空白的，ex:個股在此日期尚未上市(2069,2016,2) 
        except IndexError:
            return DataFrame()
        frameData1=frameData1.drop(u'日期').drop(u'日期', axis=1)
#         print frameData1
        resultFrameData=resultFrameData.append(frameData1)
        return resultFrameData
        pass
    def getWebToDataframe(self,code,startDate,endDate):
        tempStartDate=datetime.date(startDate.year,startDate.month,1)
        resultFrameData=DataFrame()
        tempEndDate=self.addMonth(endDate)
        while tempStartDate<=tempEndDate:
            if (tempStartDate-endDate).days>0:
                break     
            url = "http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/genpage/Report%s/%s_F3_1_8_%d.php?STK_NO=%d&myear=%s&mmon=%s"%\
            (tempStartDate.strftime('%Y%m'),tempStartDate.strftime('%Y%m'),code,code,tempStartDate.strftime('%Y'),tempStartDate.strftime('%m'))
            print url
#             print url
            data = pd.read_html(url)
            frameData=data[len(data)-2].drop([0])
            frameData1=DataFrame(frameData.values,index=frameData[0].get_values(),columns=frameData.iloc[0].get_values())
            frameData1=frameData1.drop(u'日期').drop(u'日期', axis=1)
    #         print frameData1
            resultFrameData=resultFrameData.append(frameData1)
            tempStartDate=self.addMonth(tempStartDate)
#         print resultFrameData
        return resultFrameData
    def getAuthenticationSource2(self,code,startDate,period,listLength):
        nowLength=0
        dateList=[]
        resultList=[] 
        resultDict={}
        year=startDate.year
        month=startDate.month
        periodDate=startDate+datetime.timedelta(days=period)
        frameData=self.getWebToDataframe2(code,year,month)
        while not frameData.empty:
            for date in frameData.index:
                temp=date.split('/')
                temp[0]=int(temp[0])+1911
                tempDate=datetime.date(temp[0],int(temp[1]),int(temp[2]))
                if (periodDate-tempDate).days<=0 and frameData.loc[date,u'收盤價'] !='--':
                    nowLength+=1
                    dateList.append(date)
                    resultList.append(frameData.loc[date,u'收盤價'])
                    periodDate=periodDate+datetime.timedelta(days=period)
                    if nowLength==listLength:
                        break 
            if nowLength==listLength:
                break 
            month+=1
            if month>=12:
                month=1
                year+=1
            frameData=self.getWebToDataframe2(code, year, month)
        print 'dateList:',dateList
        print 'resultList',resultList    
        if len(resultList)!= listLength:
            return False  
        else:
            resultDict['price']=resultList
            resultDict['date']=dateList
            return resultDict
        pass
    def getAuthenticationSource(self,code,startDate,endDate,period):    
        dateList=[]
        resultList=[] 
        resultFrameData=self.getWebToDataframe(code,startDate,endDate)
        periodDate=startDate+datetime.timedelta(days=period)
    #     print resultFrameData
    #     print resultFrameData.loc['104/09/30']
        for date in resultFrameData.index:
            temp=date.split('/')
            temp[0]=int(temp[0])+1911
            tempDate=datetime.date(temp[0],int(temp[1]),int(temp[2]))
#             print tempDate
            if (tempDate-endDate).days>0:
                break
            if (periodDate-tempDate).days<=0:
                dateList.append(date)
                resultList.append(resultFrameData.loc[date,u'收盤價'])
                periodDate=periodDate+datetime.timedelta(days=period)
             
    #     print len(dateList)
        print dateList
    #     print len(resultList)
        print resultList  
        return  resultList
    def getNowPrice(self,date,code):
#     date=date+datetime.timedelta(days = 1)
        try :
            url = "http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/genpage/Report%s/%s_F3_1_8_%d.php?STK_NO=%d&myear=%s&mmon=%s"%\
                (date.strftime('%Y%m'),date.strftime('%Y%m'),int(code),int(code),date.strftime('%Y'),date.strftime('%m'))
            print url
            data =pd.read_html(url)
    #             print data
#             print 'fffff',data
            frameData1=data[len(data)-2].drop([0])
    #             print frameData.iloc[0].get_values(),type(frameData.iloc[0].get_values())
    #             print frameData1
#             print date,",",code
            frameData1=DataFrame(frameData1.values,index=frameData1[0].get_values(),columns=frameData1.iloc[0].get_values())
            frameData1=frameData1.drop(u'日期').drop(u'日期', axis=1)
#                 print frameData1
            for Date1 in frameData1.index:
                temp=Date1.split('/')
                temp[0]=int(temp[0])+1911
                tempDate=datetime.date(temp[0],int(temp[1]),int(temp[2]))
                if (tempDate - date).days>=0 and frameData1.loc[Date1,u'收盤價']!='--':
    #                     print Date1
    #                     print frameData.loc[Date1,u'收盤價']
                    print frameData1
                    return frameData1.loc[Date1,u'收盤價']
            return False
        except:
            Log.i("Error code,date in twse: %s,%s" % (str(code),date.strftime('%Y/%m/%d')))
            return False
            pass

#上櫃公司
class GtsmHandler():   
    def __init__(self):
        self.templateUrl="http://www.tpex.org.tw/web/stock/aftertrading/daily_trading_info/st43_result.php?l=zh-tw&d=%s/%s&stkno=%s"
        pass
    def addrow(self,df,row,thisIndex):
        return df.append(DataFrame(row,index=[thisIndex]))  
    def addMonth(self,date):
        tempMonth=date.month+1 
        if(tempMonth>12):
            tempMonth=1
            tempYear=date.year+1
        else:
            tempYear=date.year
        if(date.day>28):
            tempDay=28
        else:
            tempDay=date.day 
        return datetime.date(tempYear,tempMonth,tempDay)    
    def getWebToDataframe(self,code,startDate,endDate):
        tempStartDate=datetime.date(startDate.year,startDate.month,1)
        tempEndDate=self.addMonth(endDate) 
        frameData=DataFrame(columns=[u'成交千股',u'成交千元',u'開盤',u'最高',u'最低',u'收盤',u'漲跌',u'筆數'])
        while tempStartDate<=tempEndDate:
            url=self.templateUrl % (str(tempStartDate.year-1911),str(tempStartDate.month),str(code))  
            print tempStartDate
#             print url
            resp =requests.get(url=url)
            soup =BeautifulSoup(resp.text)
            content=soup.find("p").contents[0]
            content=json.loads(content)
            for temp in content["aaData"]:
                row={u"成交千股":str(temp[1]).replace(',', ''),u'成交千元':str(temp[2]).replace(',', '') ,u'開盤':temp[3],u'最高':temp[4],
                     u'最低':temp[5],u'收盤':temp[6].replace(',', ''),u'漲跌':temp[7],u'筆數':str(temp[8])
                     }
                frameData=self.addrow(frameData,row,str(temp[0]))
            tempStartDate=self.addMonth(tempStartDate)
        return frameData
        print frameData
    def getWebToDataframe2(self,code,year,month):
        frameData=DataFrame(columns=[u'成交千股',u'成交千元',u'開盤',u'最高',u'最低',u'收盤',u'漲跌',u'筆數']) 
        url=self.templateUrl % (str(year-1911),str(month),str(code)) 
        print url
        resp =requests.get(url=url)
        soup =BeautifulSoup(resp.text)
        content=soup.find("body").contents[0]
        content=json.loads(content)
        print content["aaData"]
        if len(content["aaData"])!=0:
            for temp in content["aaData"]:
                row={u"成交千股":str(temp[1]).replace(',', ''),u'成交千元':str(temp[2]).replace(',', '') ,u'開盤':temp[3],u'最高':temp[4],
                     u'最低':temp[5],u'收盤':temp[6].replace(',', ''),u'漲跌':temp[7],u'筆數':str(temp[8])
                     }
                try:
                    frameData=self.addrow(frameData,row,str(temp[0]))
                except UnicodeEncodeError :
                    continue
            return frameData
        else:
            frameData=DataFrame()
            if frameData.empty:
                print 'getWebToDataframe2_False:','true'
            else:
                print 'getWebToDataframe2_False:','Flase'
            return frameData
    def getAuthenticationSource(self,code,startDate,endDate,period):
        dateList=[]
        resultList=[]
        resultFrameData=self.getWebToDataframe(code,startDate,endDate)
        periodDate=startDate+datetime.timedelta(days=period)
        for date in resultFrameData.index:
            temp=date.split('/')
            temp[0]=int(temp[0])+1911
            tempDate=datetime.date(temp[0],int(temp[1]),int(temp[2]))
            if (tempDate-endDate).days>0:
                break
            if (periodDate-tempDate).days<=0:
                dateList.append(date)
                resultList.append(resultFrameData.loc[date,u'收盤'])
                periodDate=periodDate+datetime.timedelta(days=period)
        print dateList
        print resultList
        
        return resultList
        pass
    def getAuthenticationSource2(self,code,startDate,period,listLength):
        nowLength=0
        dateList=[]
        resultList=[]
        resultDict={}
        year=startDate.year
        month=startDate.month
        periodDate=startDate+datetime.timedelta(days=period)
        frameData=self.getWebToDataframe2(code, year, month)
        while not frameData.empty:
            for date in frameData.index:
                temp=date.split('/')
                temp[0]=int(temp[0])+1911
                tempDate=datetime.date(temp[0],int(temp[1]),int(temp[2]))
                if (periodDate-tempDate).days<=0 and frameData.loc[date,u'收盤']!='--':
                    nowLength+=1
                    dateList.append(date)
                    resultList.append(frameData.loc[date,u'收盤'])
                    periodDate=periodDate+datetime.timedelta(days=period)
                    if nowLength==listLength:
                        break
            if nowLength==listLength:
                break 
            month+=1
            if month>=12:
                month=1
                year+=1
            frameData=self.getWebToDataframe2(code, year, month)     
        print 'dateList:',dateList
        print 'resultList',resultList    
        if len(resultList)!= listLength:
            return False  
        else:
            resultDict['price']=resultList
            resultDict['date']=dateList
            return resultDict
            
        

    def getNowPrice(self,date,code):
        try:
            print date
            url=self.templateUrl % (str(date.year-1911),str(date.month),str(code))
            print url
            resp =requests.get(url=url)
            soup =BeautifulSoup(resp.text)
            content=soup.find("p").contents[0]
            content=json.loads(content)
#             print content["aaData"]
    #       dataFrame版---將row變成dataFrame(後面驗證會用到)
            '''
            frameData=DataFrame(columns=[u'成交千股',u'成交千元',u'開盤',u'最高',u'最低',u'收盤',u'漲跌',u'筆數'])
            for temp in content["aaData"]:
                row={u"成交千股":str(temp[1]),u'成交千元':str(temp[2]),u'開盤':temp[3],u'最高':temp[4],
                     u'最低':temp[5],u'收盤':temp[6],u'漲跌':temp[7],u'筆數':str(temp[8])
                     }
                frameData=self.addrow(frameData,row,str(temp[0]))
                pass
            print frameData
                '''
#            空值代表找不到個股資料
            if content["aaData"]==[]:
                f = open("../data/debug.txt","a") #opens file with name of "test.txt"
                f.write("Error code,date in gtsm:: %s,%s" % (str(code),date.strftime('%Y/%m/%d')))
                f.close()
                return False
            
            for temp in content["aaData"]:
                dateList=temp[0].split('/')
                dateList[0]=int(dateList[0])+1911
                tempdate=datetime.date(dateList[0],int(dateList[1]),int(dateList[2]))
                if(tempdate-date).days>=0 and temp[6]!='--':
#                     print temp[0],",",temp[6].replace(',', '')  
                    return temp[6].replace(',', '')         
        except:
#             目前有可能因為剛上櫃那天而跑到這邊
            Log.i("Error code,date in gtsm:: %s,%s" % (str(code),date.strftime('%Y/%m/%d')))
            return False
            pass      
#             print tempdate
    
if __name__ == '__main__':
    tempDate=datetime.date(2016,4,6)
    handler=TwseHandler()
    print handler.getNowPrice(tempDate, 3701)

#     twseHandler=TwseHandler()
#     startDate=datetime.date(2016,1,1) 
#     nowDate=datetime.date(2015,3,26)
#     twseHandler.getAuthenticationSource(3492,startDate,1,20)
#     print  twseHandler.getWebToDataframe2(2069,2016,5)
#     twseHandler.getAuthenticationSource(5011, startDate, nowDate,1)
#     twseHandler.getAuthenticationSource2(3701,startDate,1,20)
#     
#     nowDate=datetime.date(2013,12,10)
#     startDate=datetime.date(2013,6,10) 
#     gtsmHandler=GtsmHandler()
#     gtsmHandler.getAuthenticationSource(3567, startDate, nowDate,30)
    
