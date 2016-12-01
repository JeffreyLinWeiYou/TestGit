#-*- coding:utf-8 -*-
'''
Created on 2016年5月26日

@author: ben
'''
from newDbHandler.newGetdbHandler import GetDbHandler
from newDbHandler.newSetDbHandler import SetDbHandler
if __name__ == '__main__':
    getDbHandler=GetDbHandler()
    setDbHandler=SetDbHandler()
    aLLPridictorAccuracy=getDbHandler.getALLPredictorAccuracy()
    for PridictorAccuracy in aLLPridictorAccuracy:
        OracletCount=getDbHandler.getPredictorOracletCount(PridictorAccuracy['predict_people'])
        print PridictorAccuracy['predict_people']
        print OracletCount[0]['count']
        setDbHandler.updatePredictorStatus(PridictorAccuracy['predict_people'], OracletCount[0]['count'],
                                            PridictorAccuracy['count'], PridictorAccuracy['sum'],
                                            PridictorAccuracy['accuracy'])
        
        
        
    pass