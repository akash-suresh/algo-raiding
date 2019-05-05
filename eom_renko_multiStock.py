
# coding: utf-8

# In[23]:


import time
from multiprocessing import Pool
from sklearn.model_selection import ParameterGrid
import csv
from utils.PreProcess import preProcessData
from utils.TimeUtil import convertTime
from scripts.dayScript import dayScript, renkoScript
from classes.ParamEntry import ParamEntry, RenkoParamEntry
from classes.DayEntry import Day
from utils.TimeUtil import isLastThursdayOfMonth
from utils.FileUtil import getFutureList
from collections import deque
from utils.Constants import futuresList
# import copy 


# In[24]:


def getSellEndOfDay(currentDate, stockType):
    if stockType == 'FUTURES':
        return isLastThursdayOfMonth(currentDate)
    else:
        return True

def renkoExperiment(paramList, stockType = 'FUTURES', verbose=False):
    df, dateList, paramEntry = paramList
    money = 1
    newDay = Day(0, money, getSellEndOfDay(dateList[0], stockType))
    renkoDeque = deque(maxlen=paramEntry.stepCount)
    paramEntry.setBrickHeight(df['openingPrice'][0])
    for date in dateList:
        new_df = df[(df.date == date)]
        day = renkoScript(new_df, paramEntry, newDay, renkoDeque, stockType, verbose)
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


# In[25]:


def bruteAnalysis(stockName, parameterDict, pool, threadPoolSize):
    csvList = []
    parameterGrid = getParameterGrid(parameterDict)
    folderName = "IntradayData_2018"
    df, dateList = preProcessData(folderName, stockName, [], [], 'blah')
    parameterGridSize = len(parameterGrid)
    print('param combination = ' , parameterGridSize)
    i=0
    while i<parameterGridSize:
        paramEntryList =[]
        for j in range(threadPoolSize):
            if i+j < parameterGridSize:
                params = parameterGrid[i+j]
                paramEntry = RenkoParamEntry(params, stockName)
                paramEntryList.append([df, dateList, paramEntry])
        start = time.time()
        resultList = pool.map(renkoExperiment, paramEntryList)
        end = time.time()
        for paramEntry in resultList:
            csvList.append(paramEntry.getCsvPoint())
        print('Time - ',end - start)
        i+=threadPoolSize
        print(i,parameterGridSize)
    return csvList


# In[29]:


def getParameterGrid(parameterDict):
    parameterGrid = ParameterGrid(parameterDict)
    return parameterGrid

def getRenkoParameterDict():
    brickHeightPercentage = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
    stepCount = [3,4,5,7]
    parameterDict = {
                    'brickHeightPercentage' : brickHeightPercentage, 
                    'stepCount': stepCount
                }
    return parameterDict


# In[30]:


stockList = futuresList


# In[28]:


threadPoolSize = 24
parameterDict = getRenkoParameterDict()
pool = Pool(threadPoolSize)
with open('result.csv', 'w') as f_out:
    out_colnames = ["stockName","brickHeightPercentage", "stepCount", "profitPercentage"]
    csv_writer = csv.DictWriter(f_out, fieldnames = out_colnames)
    csv_writer.writeheader()
    for stock in stockList:
        csvList = bruteAnalysis(stock, parameterDict, pool, threadPoolSize)
        for point in csvList:
            csv_writer.writerow(point)
pool.terminate()
pool.join()


# In[6]:


# parameterDict = getRenkoParameterDict()
# parameterGrid = getParameterGrid(parameterDict)
# folderName = "IntradayData_2018"
# stockName = 'LUPIN_F1'
# df, dateList = preProcessData(folderName, stockName, [], [], 'bleh')


# In[3]:


# money = 1
# stockType = 'FUTURES'
# verbose = False
# newDay = Day(0, money, getSellEndOfDay(dateList[0], stockType))

# paramEntry = parameterGrid[0]


# In[4]:


# # newDay = Day(0, money)
# for date in dateList:
#     new_df = df[(df.date == date)]
#     day = renkoScript(new_df, paramEntry, newDay, stockType, verbose)
#     if verbose:
#         print(date, newDay.money, day.money, day.dailyTrades)
#     sellEndOfDay = getSellEndOfDay(date, stockType)
#     day.printOpenTrade()
#     newDay = day.initializeNextDay(sellEndOfDay)    
#     break
# yearlyProfitPercentage = (day.money - 1) * 100
# print yearlyProfitPercentage    


# In[17]:


len(futuresList)

