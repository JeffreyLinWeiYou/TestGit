#-*- coding:utf-8 -*-
'''
Created on 2016年6月28日

@author: ben
'''
import datetime
import logging
import json
from performanceDetect.performanceMysqlHd import performanceMysqlHd
if __name__ == '__main__':
    performanceHd=performanceMysqlHd('ptt_performance_10')
    mySqlData=performanceHd.getCanPerfomance('2016-06-23 18:34:54','2014-08-08 13:17:36')
    print '總共有',len(mySqlData),'筆'
    x=0
    for data in mySqlData:
        print '---------------------------------------------------'
        x+=1
        print '第',x,'筆'
        print data['link']
        type = raw_input(">>> type: ")
        remark=raw_input(">>> remark: ")
        performanceHd.updatePerformance(data,str(type),str(remark))
        print data['date']
#         break
    print len(mySqlData)
#     print mySqlData
    pass