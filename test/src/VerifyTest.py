#-*- coding:utf-8 -*-
'''
Created on 2015年12月8日

@author: ben
'''
from pandas import Series,DataFrame
import pandas as pd
import datetime
def addMonth(date):
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

def getWebToDataframe(code,startDate,endDate):
    tempStartDate=datetime.date(startDate.year,startDate.month,1)
    resultFrameData=DataFrame()
    tempEndDate=addMonth(endDate)
    while tempStartDate<=tempEndDate:
        if (tempStartDate-endDate).days>0:
            break     
        url = "http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/genpage/Report%s/%s_F3_1_8_%d.php?STK_NO=%d&myear=%s&mmon=%s"%\
        (tempStartDate.strftime('%Y%m'),tempStartDate.strftime('%Y%m'),code,code,tempStartDate.strftime('%Y'),tempStartDate.strftime('%m'))
        print tempStartDate
        data = pd.read_html(url)
        frameData=data[len(data)-2].drop([0])
        frameData1=DataFrame(frameData.values,index=frameData[0].get_values(),columns=frameData.iloc[0].get_values())
        frameData1=frameData1.drop(u'日期').drop(u'日期', axis=1)
#         print frameData1
        resultFrameData=resultFrameData.append(frameData1)
        tempStartDate=addMonth(tempStartDate)
    print resultFrameData
    return resultFrameData
def getAuthenticationSource(code,startDate,endDate,period):    
    dateList=[]
    resultList=[] 
    resultFrameData=getWebToDataframe(code,startDate,endDate)
    periodDate=startDate
#     print resultFrameData
#     print resultFrameData.loc['104/09/30']
    for date in resultFrameData.index:
        temp=date.split('/')
        temp[0]=int(temp[0])+1911
        tempDate=datetime.date(temp[0],int(temp[1]),int(temp[2]))
        if (tempDate-endDate).days>0:
            break
        if (periodDate-tempDate).days<=0:
            dateList.append(date)
            resultList.append(resultFrameData.loc[date,u'收盤價'])
            periodDate=periodDate+datetime.timedelta(days=period)
         
    print len(dateList)
    print dateList
    print len(resultList)
    print resultList
    pass
if __name__ == '__main__':
    nowDate=datetime.date(2015,12,10)
    startDate=datetime.date(2015,6,10) 
    getAuthenticationSource(3673, startDate, nowDate,30)
       
    pass