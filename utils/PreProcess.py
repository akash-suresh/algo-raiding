import pandas as pd

def readFromCsv(folderName, stockName):
    df = pd.read_csv(folderName+'/'+stockName+'.txt')
    return df

def getDateList(df):
    dateList = list(set(df.date.values))
    dateList = sorted(dateList, key=abs, reverse=False)
    return dateList

def calculateExponentialMovingAverage(df, shortTermList, longTermList):
    for term in shortTermList:
        df['MA_'+str(term)] = df['openingPrice'].ewm(span=term).mean()
    for term in longTermList:
        df['MA_'+str(term)] = df['openingPrice'].ewm(span=term).mean()
    return df

def calculateMovingAverage(df, shortTermList, longTermList):
    for term in shortTermList:
        df['MA_'+str(term)] = df['openingPrice'].rolling(window=term).mean()
    for term in longTermList:
        df['MA_'+str(term)] = df['openingPrice'].rolling(window=term).mean()
    return df

def basicPreProcessing(folderName, stockName):
    df = readFromCsv(folderName, stockName)
    df.columns = ['stock', 'date','time','openingPrice','high','low','closingPrice','volume','e']
    df = df.drop('e', 1)
    return df

def preProcessData(folderName, stockName, shortTermList, longTermList, movingAverage='normal'):
    df = basicPreProcessing(folderName, stockName)
    if movingAverage == 'normal' :
        df = calculateMovingAverage(df, shortTermList, longTermList)
    elif movingAverage == 'exponential':
        df = calculateExponentialMovingAverage(df, shortTermList, longTermList)
    return df, getDateList(df)
