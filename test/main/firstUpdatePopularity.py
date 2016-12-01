# -*- coding:utf-8 -*-
'''
Created on 2016年5月22日

@author: ben
'''
from newDbHandler.newGetdbHandler import GetDbHandler
from newDbHandler.newSetDbHandler import SetDbHandler
if __name__ == '__main__':
    getHandler=GetDbHandler()
    setHandler=SetDbHandler()
    allOraclet=getHandler.getAllOraclet()
    for oraclet in allOraclet:
        print oraclet['number']
        allMessage=getHandler.getOneOracletAllMessage(oraclet['number'])
        if len(allMessage)>0:
            setHandler.updateOracletPopularity(oraclet['number'], len(allMessage))
            pass
    pass