# -*- coding:utf-8 -*-
'''
Created on 2016年6月27日

@author: ben
'''
import MySQLdb
import datetime
import logging
import json
from performanceDetect.performanceMysqlHd import performanceMysqlHd
if __name__ == '__main__':
    performanceHd=performanceMysqlHd('ptt_performance_20')
    mySqlData=performanceHd.getAllSource()
    x=0
    for data in mySqlData:
        if u'[標的]' in data['title'] and not u'Re' in data['title']:
            performanceHd.updateisSubject(data,1)
            print data['title']
            x+=1
#             break
            
            pass
    print x
#         print data['title']
    pass