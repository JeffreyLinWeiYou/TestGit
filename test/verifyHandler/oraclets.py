#-*- coding:utf-8 -*-
'''
Created on 2016年1月10日

@author: ben
'''
import datetime
class Oraclet(object):
    '''
    classdocs
    '''


    def __init__(self, record):
        self.predictPeople=record['predict_people']
        self.prdictTime=record['predict_time']
        self.predictTargetcode=record['predict_targetcode']
        self.predictTargetName=record['predict_targetname']
        self.occurTime=record['occur_time']
        self.eventContent=record['event_content']
        self.type=record['type']
        self.nowPrice=record['now_price']
        self.results=None
        self.roi=None
        self.number=record['number']
        self.Dateduration=self.occurTime-self.prdictTime
        self.determineVerifyDate()
        self.priceList=[]
        self.dateList=[]
    
    def determineVerifyDate(self):
        if self.eventContent==u'買進' or self.eventContent==u'賣出':
            print self.Dateduration.days
            print type(self.Dateduration.days)
            if self.Dateduration.days < 40:
                self.startDate=self.prdictTime
                self.endDate=self.occurTime
                self.period=1
                self.listLen=20
            elif self.Dateduration.days < 190:
                self.startDate=self.prdictTime
                self.endDate=self.occurTime
                self.period=1
                self.listLen=120
                pass
            else :
                self.startDate=self.prdictTime+datetime.timedelta(days = 180)
                self.endDate=self.occurTime
                self.period=1
                self.listLen=120
                pass
#             目交價預測
        else:
            self.startDate=self.prdictTime
            self.endDate=self.occurTime
            self.period=1
            self.listLen=240
        pass
        
        
        
        
        
        