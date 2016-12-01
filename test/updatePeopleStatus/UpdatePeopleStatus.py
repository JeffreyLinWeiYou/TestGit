#-*- coding:utf-8 -*-
'''
Created on 2016年4月15日

@author: ben
'''

class updatePeopleStatus(object):
    '''
    classdocs
    '''


    def __init__(self, dbHandler):
        '''
        Constructor
        '''
        self.dbHandler=dbHandler
    def main(self):
        self.dbHandler.getOracletGroupbyname()
        pass
    
if __name__ == '__main__':

        