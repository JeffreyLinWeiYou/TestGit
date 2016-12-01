# -*- coding:utf-8 -*-
'''
Created on 2016年6月30日

@author: ben
'''
import MySQLdb
import datetime
import logging
import json
import re
import csv
from performanceDetect.performanceMysqlHd import performanceMysqlHd

class DetectOraclet():
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
        if len(tempList)==1:       
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
            if len(tempList)==1:       
                if (self.twseDict.get(tempList[0].encode('utf-8'))!=None):
                    return [tempList[0].encode('utf-8'),self.twseDict.get(tempList[0].encode('utf-8')),5]                                                          
                if (self.gtsmDict.get(tempList[0].encode('utf-8'))!=None):
                    return [tempList[0].encode('utf-8'),self.gtsmDict.get(tempList[0].encode('utf-8')),6]       
        return False
    def getEvent(self,content):
        try:
            classificationStr=content.encode('utf-8').split('2. 分類：')[1].splitlines()[0].replace('多/空/請益/心得','')
        except IndexError as e:
#             print e
#             logging.exception("getEvent")
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
        mySqlData=self.performanceHd.getSubject()
        for data in mySqlData:
            codeInfo=self.newFindCode(data['title'],data['content'])
            if codeInfo!=False:
                
                author=data['author'].split(u'(')[0]
                date=data['date'].date()
                event=self.getEvent(data['content'])
#                 if event==False:
#                     continue
#                 print author
#                 print date
#                 print event
                temp=self.performanceHd.getOneOraclet(author,date,codeInfo[0])
                if len(temp)>0:
                    self.performanceHd.updateIsOraclet(data,1)
#                 break
                pass
            print data['title']
            
        pass    
if __name__ == '__main__':
    detectOraclet=DetectOraclet()
    detectOraclet.main()
    pass