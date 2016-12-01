# -*- coding:utf-8 -*-
'''
Created on 2016年6月28日

@author: ben
'''
import datetime
import logging
import json
from performanceDetect.performanceMysqlHd import performanceMysqlHd
if __name__ == '__main__':
    person=2
    performanceHd=performanceMysqlHd('ptt_performance_10')
    mySqlData=performanceHd.getAllcanPrecision()
    print len(mySqlData)
    halfNumber=(len(mySqlData))/2
    print halfNumber
    if person==1:
        print mySqlData[0]['date']
        print mySqlData[halfNumber-1]['date']
    if person==2:
        print mySqlData[halfNumber]['date']
        print mySqlData[len(mySqlData)-1]['date']
    pass