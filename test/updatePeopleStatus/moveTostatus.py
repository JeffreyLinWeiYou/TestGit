#-*- coding:utf-8 -*-
'''
Created on 2016年5月2日

@author: ben
'''
import json
from MySQLHandler.MySQLHandler import MySQLHandler
from datetime import date,datetime
if __name__ == '__main__':
    dbHandler=MySQLHandler()
#     mySQLData=dbHandler.getAllOraclets()
#     for SQLData in mySQLData:
#         print SQLData['results']
#         if SQLData['results']!=None:
#             dbHandler.updateOracletResultStatus(SQLData['number'],SQLData['results'])
# #             break
    sql="SELECT * FROM new_results"
    mySQLData=dbHandler.getSQL(sql)
    for SQLData in mySQLData:
        print SQLData
        priceList=json.loads(SQLData['price_list'])
        dateList=json.loads(SQLData['date_list'])
        for idx, date in enumerate(dateList):
            temp=date.split('/')
            temp[0]=int(temp[0])+1911
            tempDate=datetime.strptime(str(temp[0])+temp[1]+temp[2], '%Y%m%d').date()
            dateList[idx]=tempDate
            pass
        if len(dateList)==len(dateList):
            for idx, date in enumerate(dateList):
#                 print date
#                 print type(date)
                dbHandler.setresultRecord(SQLData['o_number'], dateList[idx], priceList[idx])
#                 break
                pass
        print dateList
        print priceList
#         dbHandler.updateOracletResultsForTemp(SQLData['o_number'], SQLData['result'])
#         break
#         break
        pass