# -*- coding:utf-8 -*-
'''
Created on 2016年6月13日

@author: ben
'''
import requests
from bs4 import BeautifulSoup
from datetime import timedelta
import datetime
from time import sleep
import csv
if __name__ == '__main__':
    test=datetime.datetime(2014, 3, 1)
#     print test
    tempList=[]
    tempList2=[]
    for i in range(1, 31):
        print test,'------------------------------------------------------------'
        url="http://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=466920&datepicker=%s"%\
            (test.strftime('%Y-%m-%d'))
        print url
        resp = requests.get(
        url
        )
        tempList.append(test)
        tempList.append(url)
        soup = BeautifulSoup(resp.text)
        temp1=soup.findAll("tr")
        i=0
        for temp in temp1:
            if i>2:
                stringg=str(temp.contents[7]).split('<td>')[1].split('</td>')[0]
                print  str(temp.contents[7]).split('<td>')[1].split('</td>')[0]
                tempList.append(stringg)
    #             print type( str(temp.contents[7]))
            i+=1
        test=test+timedelta(days=1)
        sleep(0.3)
        pass
    tempList2.append(tempList)
    f = open("stock.csv","wb")
    w = csv.writer(f)
    for temp in tempList:
        temp2=[]
        temp2.append(temp)
        w.writerows([temp2])
    
    f.close()
#     
#     url="http://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=466920&datepicker=2014-02-16"
#     
#     resp = requests.get(
#         url
#         )
#     soup = BeautifulSoup(resp.text)
#     temp1=soup.findAll("tr")
#     i=0
#     for temp in temp1:
#         if i>2:
#             temp.contents[7]
#             print  str(temp.contents[7]).split('<td>')[1].split('</td>')[0]
# #             print type( str(temp.contents[7]))
#         i+=1
# #     print temp1
# #     i=0
# #     for temp in temp1:
# #         if 
# #         i+=1
# #     print temp[3]
    pass