
# coding: utf-8

# In[1]:


import time
from multiprocessing import Pool
from sklearn.model_selection import ParameterGrid
import csv
from utils.PreProcess import preProcessData
from utils.TimeUtil import convertTime
from scripts.dayScript import dayScript
from classes.ParamEntry import ParamEntry
from classes.DayEntry import Day
from utils.TimeUtil import isLastThursdayOfMonth
# import copy 


# In[2]:


def getSellEndOfDay(currentDate, stockType):
    if stockType == 'FUTURES':
        return isLastThursdayOfMonth(currentDate)
    else:
        return True

def movingAverageExperiment(paramList, stockType = 'FUTURES', verbose=False):
    df, dateList, paramEntry = paramList
    money = 1
    newDay = Day(0, money, getSellEndOfDay(dateList[0], stockType))

    for date in dateList:
        new_df = df[(df.date == date)]
        day = dayScript(new_df, paramEntry, newDay, stockType, verbose)
        if verbose:
            print(date, newDay.money, day.money, day.dailyTrades)
            day.printOpenTrade()
        sellEndOfDay = getSellEndOfDay(date, stockType)
        newDay = day.initializeNextDay(sellEndOfDay)   
        
    yearlyProfitPercentage = (day.money - 1) * 100
    print(yearlyProfitPercentage)
    paramEntry.profitPercentage = yearlyProfitPercentage
    paramEntry.toString()
   
    return paramEntry


# In[3]:


def bruteAnalysis(stockName, parameterDict, pool, threadPoolSize):
    csvList = []
    parameterGrid = getParameterGrid(parameterDict)
    folderName = "IntradayData_2018"
    df, dateList = preProcessData(folderName, stockName, parameterDict['shortTerm'], parameterDict['longTerm'], 'exponential')
    parameterGridSize = len(parameterGrid)
    print('param combination = ' , parameterGridSize)
    i=0
    while i<parameterGridSize:
        paramEntryList =[]
        for j in range(threadPoolSize):
            if i+j < parameterGridSize:
                params = parameterGrid[i+j]
                paramEntry = ParamEntry(params, stockName)
                paramEntryList.append([df, dateList, paramEntry])
        start = time.time()
        resultList = pool.map(movingAverageExperiment, paramEntryList)
        end = time.time()
        for paramEntry in resultList:
            csvList.append(paramEntry.getCsvPoint())
        print('Time - ',end - start)
        i+=threadPoolSize
        print(i,parameterGridSize)
    return csvList


# In[4]:


# stockList = ['ACC_F1','ASHOKLEY_F1','AXISBANK_F1','BHARTIARTL_F1','RELIANCE_F1','INFY_F1','WIPRO_F1','PNB_F1','SBIN_F1','SUNPHARMA_F1','GRASIM_F1','LUPIN_F1','LT_F1','HINDUNILVR_F1']
stockList = ['LUPIN_F1', 'ASHOKLEY_F1','ACC_F1']


# In[5]:


def getParameterGrid(parameterDict):
    parameterGrid = ParameterGrid(parameterDict)
    return parameterGrid

def getParameterDict():
    # # #old
#     shortTerm = [1,4,12,20]
#     longTerm = [100,200,500,1000]
#     targetPercentage = [0.01, 0.05, 0.075]
#     stopLossPercentage = [0.002, 0.006, 0.008, 0.010]
#     entryDifference = [0.00001, 0.00005, 0.00010, 0.0002]
    # # #new
    shortTerm = [4,8,12,16]
    longTerm = [100,200,300,400,500]
    targetPercentage = [0.01, 0.05, 0.075]
    stopLossPercentage = [0.006, 0.007, 0.008, 0.010]
    entryDifference = [0.00005, 0.000075, 0.0001]
    # # # #v3
#     shortTerm = [8]
#     longTerm = [200]
#     targetPercentage = [0.01]
#     stopLossPercentage = [0.006]
#     entryDifference = [0.00005]
    parameterDict = {
                    'shortTerm' : shortTerm, 
                    'longTerm': longTerm, 
                    'targetPercentage': targetPercentage, 
                    'stopLossPercentage': stopLossPercentage, 
                    'entryDifference':entryDifference
                }
    return parameterDict


# In[ ]:


threadPoolSize = 24
parameterDict = getParameterDict()
pool = Pool(threadPoolSize)
with open('result.csv', 'w') as f_out:
    out_colnames = ["stockName","shortTerm", "longTerm", "targetPercentage", "stopLossPercentage", "entryDifference","profitPercentage"]
    csv_writer = csv.DictWriter(f_out, fieldnames = out_colnames)
    csv_writer.writeheader()
    for stock in stockList:
        csvList = bruteAnalysis(stock, parameterDict, pool, threadPoolSize)
        for point in csvList:
            csv_writer.writerow(point)
pool.terminate()
pool.join()


# In[6]:


# parameterDict = getParameterDict()
# parameterGrid = getParameterGrid(parameterDict)
# folderName = "IntradayData_2018"
# stockName = 'LUPIN_F1'
# df, dateList = preProcessData(folderName, stockName, parameterDict['shortTerm'], parameterDict['longTerm'], 'exponential')


# In[7]:


# money = 1
# stockType = 'FUTURES'
# verbose = False
# newDay = Day(0, money, getSellEndOfDay(dateList[0], stockType))


# In[8]:


# # newDay = Day(0, money)
# for date in dateList:
#     new_df = df[(df.date == date)]
#     day = dayScript(new_df, paramEntry, newDay, stockType, verbose)
#     if verbose:
#         print(date, newDay.money, day.money, day.dailyTrades)
#     sellEndOfDay = getSellEndOfDay(date, stockType)
#     day.printOpenTrade()
#     newDay = day.initializeNextDay(sellEndOfDay)    

# yearlyProfitPercentage = (day.money - 1) * 100
# print yearlyProfitPercentage    

