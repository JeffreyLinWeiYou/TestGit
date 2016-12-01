#-*- coding:utf-8 -*-
'''
Created on 2015年11月20日

@author: ben
'''
import requests
import re
import sys
import json
import requests
from time import sleep
from bs4 import BeautifulSoup  
import MySQLdb
from datetime import datetime
db=MySQLdb.connect("140.118.7.46","s8107072004","ben60514","crawler_test",charset="utf8")
def crawler(start,end):
    page = start; times = end-start+1; g_id = 0;
    for a in range(times):
        print('index is '+ str(page))
        resp = requests.get(
        url="http://www.ptt.cc/bbs/Stock/index"+str(page)+".html", 
        cookies={"over18": "1"}
        )
        soup = BeautifulSoup(resp.text)
#         print soup        
        for tag in soup.find_all("div","r-ent"):
            try:
                link = str(tag.find_all("a"))
#                 print link.decode('unicode_escape')
#                 print link
                link = link.split("\"")
#                 print link[2]
#                 print link[2].decode('unicode_escape')
                if '[\u6a19\u7684]'in link[2] and not 'Re' in link[2]:
#                     print "true"
                    link = "http://www.ptt.cc"+link[1]
                    g_id = g_id+1
                    parseGos(link,g_id)
            except:
                pass
        
        sleep(0.2)
        page += 1
def dataToMYsql(d):
#     sql="INSERT INTO ptt_source (author,date,title,ip,link,content,message,messageNum)\
#         VALUES ('test','2015-11-18 21:21:52','11','140.118.7.46','http://www.ptt.cc/bbs/Gossiping/M.1369245377.A.A93.html','content','message','messageNum')"
    
    textType=u'%a %b %d %H:%M:%S %Y'
    date_object = datetime.strptime(d['d_date'], textType)
    dStr = date_object.strftime('%Y-%m-%d %H:%M:%S')
    
#     print dStr
#     print d['f_content'].decode('utf-8')
#     print type(d['f_content'].decode('utf-8'))
    
#     sql=u"INSERT INTO ptt_source (author,date,title,ip,link,content,message,messageNum)\
#         VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"%\
#         (d['b_author'],dStr,d['c_title'],d['e_ip'],d['link'],d['f_content'].decode('utf-8'),str(d['g_message']).decode('utf-8'),str(d['h_messageNum']).decode('utf-8'))
    #目前sql是unicode
    sql=u"INSERT INTO ptt_source (author,date,title,ip,link,content,message,messageNum)VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(d['b_author'],dStr,d['c_title'],d['e_ip'],d['link'],d['f_content'].decode('utf-8'),d['g_message'],str(d['h_messageNum']).decode('utf-8'))
    #sql編碼成utf-8
    sql=sql.encode('utf-8')
#     print sql
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
    except MySQLdb.Error as e:
        print "Error %d: %s" % (e.args[0], e.args[1])
    
    pass
def parseGos(link , g_id):
    resp = requests.get(url=str(link),cookies={"over18":"1"})
    soup = BeautifulSoup(resp.text)
#     print 'link:',link
#     print soup
#     print(resp)
    # author
    author  = soup.find(id="main-container").contents[1].contents[0].contents[1].string.replace(' ', '')
#     print'author:',author
    # title
    title = soup.find(id="main-container").contents[1].contents[2].contents[1].string.replace(' ', '')
    # date
    date = soup.find(id="main-container").contents[1].contents[3].contents[1].string
#     print 'date:',date
    # ip
    try:
        ip = soup.find(text=re.compile(u"※ 發信站:"))
#         print "ip:",ip
        ip = re.search(u"[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*",ip).group()
    except:
        ip = "ip is not find"
    # content
    a = str(soup.find(id="main-container").contents[1])
    a = a.split("</div>")
    a = a[4].split("<span class=\"f2\">※ 發信站: 批踢踢實業坊(ptt.cc)")
    content = a[0].replace("\'",'*')
#     print type(content)
#     print'content:',content
    # message
    num , all , g , b , n ,message = 0,0,0,0,0,[]
    for tag in soup.find_all("div","push"):
        num += 1
        push_tag = tag.find("span","push-tag").string.replace(' ', '')
        push_userid = tag.find("span","push-userid").string.replace(' ', '')
        push_content = tag.find("span","push-content").string.replace('\n', '').replace('\t', '')
        print(push_content)
        push_ipdatetime = tag.find("span","push-ipdatetime").string.replace('\n', '')
        message.append({"status":push_tag,"id":push_userid,"content":push_content,"time":push_ipdatetime})
        #推
#         print push_tag
#         print type(push_tag)
#         print type(u"推")
        if push_tag == u'推':
#             print "11"
            g += 1
        #噓
        elif push_tag == u'噓':
#             print "22"
            b += 1
        else:
#             print "33"
            n += 1            
    messageNum = {"g":g,"b":b,"n":n,"all":num}
    
    # json-data
#     message =str(message).encode('utf-8')
#     print message['1']['content']
    message = json.dumps(message,indent=1, encoding='utf-8',ensure_ascii=False)
    messageNum = json.dumps(messageNum,indent=1,sort_keys=True)
#     print message
    d={ "link":link,"a_ID":g_id , "b_author":author , "c_title":title , "d_date":date , "e_ip":ip , "f_content":content , "g_message":message, "h_messageNum":messageNum }
#     dataToMYsql(d)
#     return d
#     print 'd:',d
#     print d["a_ID"],",",d["b_作者"]
#     print d['c_標題']
#     print json_data
        
if __name__ == '__main__':
    global db
    parseGos('https://www.ptt.cc/bbs/Stock/M.1448268961.A.751.html','100')
#     crawler(2697,2698)
    
 
#     crawler(2513,2701)
    db.close
#     with open('data.json', 'r') as f:
#         p = f.read()
#     with open('data.json', 'w') as f:
#         f.write(p.replace(',]',']'))
    pass