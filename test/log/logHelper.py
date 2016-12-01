# coding=UTF-8
'''
Created on 2015年12月18日

@author: ben
'''
import datetime
class Log(object):
    '''
    classdocs
    '''
    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    @staticmethod
    def i(str):
        dateStr=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f = open("../data/debug.txt","a") #opens file with name of "test.txt"
        str='['+dateStr+']'+str+'\n'
        f.write(str)
        f.close()
        pass
if __name__ == '__main__':
    Log.i('Error code in gtsm:tttt')    