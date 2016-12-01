# coding=UTF-8

import MySQLdb

if __name__ == '__main__':
    try:
    # 建立DB 連線資訊定設定中文編碼utf-8
      db = MySQLdb.connect("140.118.7.46","s8107072004","ben60514","mem",charset='utf8')
      sql = "SELECT * FROM gps ORDER BY time DESC"
      # 執行SQL statement
      cursor = db.cursor()
      cursor.execute(sql)
    
      # 撈取多筆資料
      results = cursor.fetchall()
    
      # 迴圈撈取資料
      for record in results: 
          col1 = record[0]
          col2 = record[1]
        
          print "%s, %s" % (col1, col2)
    
      # 關閉連線
      db.close()
    except MySQLdb.Error as e:
      print "Error %d: %s" % (e.args[0], e.args[1])
    pass