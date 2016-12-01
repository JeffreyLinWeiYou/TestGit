# -*- coding:utf-8 -*-
'''
Created on 2016年6月27日

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
import random
from performanceDetect.performanceMysqlHd import performanceMysqlHd
from time import sleep
class detectMain(object):
    def __init__(self):
        self.MaxCounter=10
        self.lastIndex=0
        self.nowCount=0
        self.linkList=[]
        self.performanceHd=performanceMysqlHd()
    def findLastIndex(self):
        resp = requests.get(
        url="http://www.ptt.cc/bbs/Stock/index.html"
        )
#         print BeautifulSoup(resp.text).find_all("div","btn-group btn-group-paging")[0]
#         原本:btn-group pull-right  修改後:btn-group btn-group-paging 05/02
        a = BeautifulSoup(resp.text).find_all("div","btn-group btn-group-paging")[0].find_all("a")[1]
        link=str(a).split("\"")
        tempList=re.findall('(?<![0-9])[0-9]{1,6}(?![0-9])',link[3])
        return int(tempList[0])+1
        pass
    def dataToMYsql(self,d):
        self.performanceHd.dictToDb(d)
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
            try:
                push_ipdatetime = tag.find("span","push-ipdatetime").string.replace('\n', '')
            except AttributeError:
                continue
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
#         print d
        self.dataToMYsql(d)
    def main(self):
        self.lastIndex=self.findLastIndex()
        breakcount=0
        x=0
        for i in range(self.lastIndex,0,-1):
            print str(i)
            try:
                resp = requests.get(
                url="http://www.ptt.cc/bbs/Stock/index"+str(i)+".html"
                )
            except:
                continue
            soup = BeautifulSoup(resp.text)
            
            for tag in soup.find_all("div","r-ent"):
                try:
                    link = tag.find_all("a")[0].encode("utf-8")
                    link = link.split("\"")
                    link = "http://www.ptt.cc"+link[1]
                    self.linkList.append(link)
                except IndexError:
                    print 'IndexError.............................'
                    logging.basicConfig(filename='logging.txt')
                    logging.exception("IndexError")
                except Exception as e:
                    logging.basicConfig(filename='logging.txt')
                    logging.exception("message") 
                    
                if len(self.linkList)>4:
                    tempLink=random.choice(self.linkList)
                    try:
                        self.parseGos(tempLink)
                    except IndexError:
                        pass
                    except Exception:
                        pass
                    self.linkList=[]
                    x=0
                    pass  
                x+=1
                breakcount+=1
                print 'x:',x
#                 print 'breakcount:',breakcount
#                 if breakcount>300:
#                     print 'break12'
#                     break 
#             if breakcount>300:
#                 print 'break1'
#                 break  
        sleep(0.1)          
if __name__ == '__main__':
#     temp=performanceMysqlHd()
    detect=detectMain()
    detect.main()
    pass