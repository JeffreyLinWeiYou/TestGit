#-*- coding:utf-8 -*-
'''
Created on 2016年6月30日

@author: ben
'''
import datetime
import logging
import json
from performanceDetect.performanceMysqlHd import performanceMysqlHd
import re
import csv
class OracletPrecision():
    def csvToList(self,filePath):
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
    def newFindCode(self,title,content):
        content=content.encode('utf-8')
        tempList=re.findall('(?<![0-9])[0-9]{1,6}(?![0-9])',title)
    #     print tempList
    #     global twseStockList
        if len(tempList)>=1:       
            if (self.twseDict.get(tempList[0].encode('utf-8'))!=None):
                return [tempList[0].encode('utf-8'),self.twseDict.get(tempList[0].encode('utf-8')),5]                                                          
            if (self.gtsmDict.get(tempList[0].encode('utf-8'))!=None):
                return [tempList[0].encode('utf-8'),self.gtsmDict.get(tempList[0].encode('utf-8')),6]
                pass
            pass
        else:
#             print 'test'
            try:
                tempList=re.findall('(?<![0-9])[0-9]{1,6}(?![0-9])',content.split('1. 標的：')[1].splitlines()[0])
            except IndexError as e:
#                 logging.exception("newFindCode")
                print e
                return False
            print tempList
            if len(tempList)>=1:       
                if (self.twseDict.get(tempList[0].encode('utf-8'))!=None):
                    return [tempList[0].encode('utf-8'),self.twseDict.get(tempList[0].encode('utf-8')),5]                                                          
                if (self.gtsmDict.get(tempList[0].encode('utf-8'))!=None):
                    return [tempList[0].encode('utf-8'),self.gtsmDict.get(tempList[0].encode('utf-8')),6]       
        return False
    def getEvent(self,content):
        try:
            classificationStr=content.encode('utf-8').split('2. 分類')[1].splitlines()[0].replace('多/空/請益/心得','')
        except IndexError as e:
#             print e
            logging.exception("getEvent")
            return u'買進'
        if '空' in classificationStr:
            return u'賣出'
        elif '多' in classificationStr:
            return u'買進'
        else:
            return False
    def __init__(self):
        self.twseDict=self.csvToList('../data/twseStockList.csv')
        self.gtsmDict=self.csvToList('../data/gtsmStockList.csv')         
        self.performanceHd=performanceMysqlHd('ptt_performance_10')
    def main(self):
        mySqlData=self.performanceHd.getCanRePrecision()
        
        print '總共有',len(mySqlData),'筆'
        x=0
        for data in mySqlData:
            print '---------------------------------------------------'
            x+=1
            print '第',x,'筆'
            print data['link']
            codeInfo=self.newFindCode(data['title'],data['content'])
            if codeInfo!=False:
                author=data['author'].split(u'(')[0]
                date=data['date'].date()
                event=self.getEvent(data['content'])
                print event
            temp=self.performanceHd.getOneOraclet(author,date,codeInfo[0])[0]
            print '卜卦的作者為:',temp['predict_people']
            print '卜卦的時間為:',temp['predict_time']
            print '卜卦的代碼為:',temp['predict_targetcode']
            print '卜卦的預測事件為:',temp['event_content']
            
            oracletT_F = raw_input(">>> oraclet解析正確或錯誤: ")
            oraclet_remark=raw_input(">>> remark: ")
            self.performanceHd.updateRePrecision(data,str(oracletT_F),str(oraclet_remark))
            print data['date']
#             break
        print len(mySqlData)         
if __name__ == '__main__':
    precision=OracletPrecision()
    precision.main()
