# coding=UTF-8
'''
Created on 2016年3月20日

@author: ben
'''
import MySQLdb
if __name__ == '__main__':
    db=MySQLdb.connect("140.118.7.46","s8107072004","ben60514","test",charset="utf8")
    sql="SELECT * FROM `oraclet` WHERE 1 GROUP BY `predict_people` ORDER BY `number` ASC"
    dict_cursor=db.cursor(MySQLdb.cursors.DictCursor)
    dict_cursor.execute(sql)
    MysqlData=dict_cursor.fetchall()
    for record in MysqlData:
        if record['type']>4:
#             print record["predict_people"]
            sql="INSERT INTO predict_people(name,type) VALUES ('%s','%s')"%(record["predict_people"],'2')
        else:
            sql="INSERT INTO predict_people(name,type) VALUES ('%s','%s')"%(record["predict_people"],'1')
        try:
            dict_cursor.execute(sql)
            db.commit()
        except MySQLdb.Error as e:
            print e
#         break
    db.close()
    pass