#-*- coding:utf-8 -*-
'''
Created on 2016年3月20日

@author: ben
'''
import json
import requests
import MySQLdb
from bs4 import BeautifulSoup  
import re
from MySQLHandler.MySQLHandler import MySQLHandler
from datetime import datetime
import sys
import logging
import csv
from getWebHandler.getPrices import *
from setOracletHandler.setOracletHandler import *

from time import sleep
class routineMain(object):
    '''
    classdocs
    '''

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
    
    
    def __init__(self):
        self.isContinue=True
        self.lastIndex=0
        self.twseDict=self.csvToList('../data/twseStockList.csv')
        self.gtsmDict=self.csvToList('../data/gtsmStockList.csv')
        
        '''
        Constructor
        '''
    
    def findLastIndex(self):
        resp = requests.get(
        url="http://www.ptt.cc/bbs/Stock/index.html"
        )
        a = BeautifulSoup(resp.text).find_all("div","btn-group pull-right")[0].find_all("a")[1]
        link=str(a).split("\"")
        tempList=re.findall('(?<![0-9])[0-9]{1,6}(?![0-9])',link[3])
        return int(tempList[0])+1
    def findCode(self,tempstr):
        tempList=re.findall('(?<![0-9])[0-9]{1,6}(?![0-9])',tempstr)
    #     print tempList
    #     global twseStockList
        if len(tempList)==1:       
            if (self.twseDict.get(tempList[0].encode('utf-8'))!=None):
                return [tempList[0].encode('utf-8'),self.twseDict.get(tempList[0].encode('utf-8')),5]                                                          
            if (self.gtsmDict.get(tempList[0].encode('utf-8'))!=None):
                return [tempList[0].encode('utf-8'),self.gtsmDict.get(tempList[0].encode('utf-8')),6]
                pass
            pass
        return False
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
            classificationStr=content.encode('utf-8').split('2. 分類：')[1].splitlines()[0]
        except IndexError as e:
            logging.exception("getEvent")
            return u'買進'
        if '空' in classificationStr:
            return u'賣出'
        elif '多' in classificationStr:
            return u'買進'
        else:
            return False
    def getOccurTime(self,content,date):
        try:
            tempstr=content.encode('utf-8').split('4. 進退場機制：')[1].replace('(停損價位/出場條件/長期投資)','')
            print tempstr
        except:
            print "getOccurTime........"
            return date+datetime.timedelta(days = 35)
            
        if '長期投資' in tempstr:
            return date+datetime.timedelta(days = 380)
        else :
            return date+datetime.timedelta(days = 35)
        
        pass
    def pttBuild(self,d):
        dbHandler=MySQLHandler()
        mysqlData=dbHandler.getOnePttSource(d['b_author'],d['d_date'])[0]
        oracletDict={}
        print mysqlData['title']
        print type(mysqlData['title'])
        codeInfo=self.newFindCode(mysqlData['title'],mysqlData['content'])
        
        if codeInfo!=False:
            oracletDict['name']=mysqlData['author'].split(u'(')[0]
            oracletDict['date']=mysqlData['date'].date()
            oracletDict['code']=codeInfo[0]
            oracletDict['targetName']=codeInfo[1]
            oracletDict['type']=codeInfo[2]
            oracletDict['event']=self.getEvent(mysqlData['content'])
            oracletDict['occurTime']=self.getOccurTime(mysqlData['content'],oracletDict['date'])
            if oracletDict['type']==5:
                oracletDict['nowprice']=TwseHandler().getNowPrice(oracletDict['date'],oracletDict['code'])
            elif oracletDict['type']==6:
                oracletDict['nowprice']= GtsmHandler().getNowPrice(oracletDict['date'],oracletDict['code'])
            
#             if oracletDict['name']==u'bbs3379':
#                 print 'test'
#             4/5問題集1，目前先用==None代替
            if oracletDict['nowprice']==False  or oracletDict['nowprice'] == 0 \
                or oracletDict['nowprice'] ==None or oracletDict['event']==False:
                return False
            else:
#       需判斷有沒有預測人啊!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
                if  dbHandler.getPredictPeople(oracletDict['name']) ==False:
                    dbHandler.setOnePredictPeople(oracletDict['name'], '2')
                    pass             
                dbHandler.setOneOraclet(oracletDict)
                return oracletDict
        else:
            return False
        pass
    def updatePttAndMessage(self,pttSource,d):
        messagestr=d['g_message'].replace('\\','')
        message = json.loads(messagestr)
        dbHandler=MySQLHandler()
#        把是否有oraclet的判斷移到外面
#                  self.newFindCode(mysqlData['title'],mysqlData['content'])
        codeInfo=self.newFindCode(pttSource[0]['title'],pttSource[0]['content'])
        print codeInfo
        if codeInfo!=False:
            try:
                oracletNumber=dbHandler.getOneOraclet(pttSource[0]['author'].split(u'(')[0].encode('utf-8'),
                                  pttSource[0]['date'].date().strftime("%Y-%m-%d"), 
                                  str(codeInfo[0]),
                                  self.getEvent(pttSource[0]['content']).encode('utf-8'))[0]['number']
            except IndexError as e:
                logging.exception("updatePtt")
                return False
            except AttributeError as e:
                logging.exception("updatePttGetEvent")
                return False
            dbMessage=json.loads(pttSource[0]['message'])
            updateName=set()
            #         如果新撈到的留言筆數比原資料庫中的筆數多
            if len(dbMessage) < len(message):
#                 需更新pttsource資料庫!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                dbHandler.updatePttsource(pttSource[0]['author'], pttSource[0]['date'], messagestr)
                for temp in message:
    #                 不確定能不能用，需確認
                    if temp not in dbMessage:
                        updateName.add(temp['id'])
                
                message=SetOracletHandler.normalizeMessage(messagestr)
                print message
                for temp in  message:
                    if temp['id'] in updateName:
#                         需要測試!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        dbHandler.updateOrInsetMessage(temp['id'],pttSource[0]['date'],temp['time'],temp['content'].replace(' ',''),oracletNumber,temp['status'])
    def  dataToMYsql(self,d):
        dbHandler=MySQLHandler()
        pttSource=dbHandler.getOnePttSource(d['b_author'], d['d_date'])
        if  pttSource==False:
#           新增ptt_source
            dbHandler.setOnePttSource(d)
#           卜卦立案  
            oracletDict=self.pttBuild(d)
            if oracletDict!=False:
#                 毛盾卜卦找尋集更新、更新留言庫
#            3_23 留言資料庫更新coding完成，需要測試~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                dbHandler.setOneContradiction(oracletDict)
                
                messagestr=d['g_message'].replace('\\','')
                message=SetOracletHandler.normalizeMessage(messagestr)
                dbHandler.setNewMessage(message,oracletDict)
        else:
#             拿取oracelt 沒拿到代表不用做更新
            dbHandler.updatePttsource(d['b_author'],d['d_date'],d['g_message'])
            self.updatePttAndMessage(pttSource,d)
#             檢查是否需要更新ptt_source、更新留言庫
            pass
        pass   
    def parseGos(self,link):
        print link
        resp = requests.get(url=str(link))
        soup = BeautifulSoup(resp.text)
        try:
            author  = soup.find(id="main-container").contents[1].contents[0].contents[1].string.replace(' ', '')
            title = soup.find(id="main-container").contents[1].contents[2].contents[1].string.replace(' ', '')
            date = soup.find(id="main-container").contents[1].contents[3].contents[1].string
            textType=u'%a %b %d %H:%M:%S %Y' 
            date = datetime.datetime.strptime(date, textType)
        except AttributeError as e:
            logging.exception("parseGos")
            return False
        try:
            ip = soup.find(text=re.compile(u"※ 發信站:"))
    #         print "ip:",ip
            ip = re.search(u"[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*",ip).group()
        except:
            ip = "ip is not find"
        a = str(soup.find(id="main-container").contents[1])
        a = a.split("</div>")
        a = a[4].split("<span class=\"f2\">※ 發信站: 批踢踢實業坊(ptt.cc)")
        content = a[0].replace("\'",'*')
#         print  content
        num , all , g , b , n ,message = 0,0,0,0,0,[]
        for tag in soup.find_all("div","push"):
#             ptt網頁留言有網址時，會跳出此錯誤 https://www.ptt.cc/bbs/Stock/M.1458874559.A.8C5.html
            try:
                push_content = tag.find("span","push-content").string.replace('\n', '').replace('\t', '').replace("\'",'*').replace("\"",'').replace("\\",'')
            except AttributeError:
                continue
            num += 1
            push_tag = tag.find("span","push-tag").string.replace(' ', '')
            push_userid = tag.find("span","push-userid").string.replace(' ', '')
            push_ipdatetime = tag.find("span","push-ipdatetime").string.replace('\n', '')
            message.append({"status":push_tag,"id":push_userid,"content":push_content,"time":push_ipdatetime})
#             print push_content
            #推
            if push_tag == u'推':
                g += 1
            #噓
            elif push_tag == u'噓':
                b += 1
            else:
                n += 1     
        messageNum = {"g":g,"b":b,"n":n,"all":num}
        message = json.dumps(message,indent=1, encoding='utf-8',ensure_ascii=False)
        messageNum = json.dumps(messageNum,indent=1,sort_keys=True)
        d={ "link":link, "b_author":author , "c_title":title , "d_date":date , "e_ip":ip , "f_content":content , "g_message":message, "h_messageNum":messageNum }
        self.dataToMYsql(d)
    def main(self):
        self.lastIndex=self.findLastIndex()
#         print self.lastIndex    
        for i in range(11, 0, -1):
            print self.lastIndex
#             測試修改，完成後需要改回來!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            resp = requests.get(
            url="http://www.ptt.cc/bbs/Stock/index"+str(self.lastIndex)+".html"
            )
            soup = BeautifulSoup(resp.text)
            x=0
            for tag in soup.find_all("div","r-ent"):
                try:
                    link = tag.find_all("a")[0].encode("utf-8")
                    link = link.split("\"")
                    if '[標的]'in link[2] and not 'Re' in link[2]:
                        print tag
                        link = "http://www.ptt.cc"+link[1]
#                         print "標的:",link
                        self.parseGos(link)
                        print'---------------------------------------------------------------'
                        x+=1
                        if x==1:
                            break
                except IndexError:
                    print 'IndexError.............................'
                    logging.basicConfig(filename='logging.txt')
                    logging.exception("IndexError")
                except Exception as e:
                    logging.basicConfig(filename='logging.txt')
                    logging.exception("message")
                    sys.exit()
                    break
            sleep(0.2)
#             break
            self.lastIndex-=1
        pass
    
if __name__ == '__main__':
    routine=routineMain()
    routine.main()

#     dbHandler=MySQLHandler()
#     tempdate = datetime.datetime.strptime('2016-03-31 16:51:24', '%Y-%m-%d %H:%M:%S')
#     print tempdate
#     mysqldata=dbHandler.getOnePttSource(u'id520(反指標)',tempdate)
#     print mysqldata[0]['content']
#          
#     temp=routine.newFindCode('',mysqldata[0]['content'].encode('utf8'))
#     print temp
#     print temp[1]
#     temp=routine.getEvent(mysqldata[0]['content'].encode('utf8'))
#     print temp
    
#     temp=routine.getOccurTime(mysqldata[0]['content'].encode('utf8'))
#     print temp
#     print routineMain().twseDict
#      MySQLHandler().getOnePttSource(u'simpleisbest(簡單就是最好)', datetime(2007,6,14,8,19,52))
        