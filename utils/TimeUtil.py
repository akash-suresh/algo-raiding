from datetime import date
from dateutil.relativedelta import relativedelta, TH

def convertTime(timeString):
    timeArr = timeString.split(':')
    time = int(timeArr[0])*60 + int(timeArr[1])
    return time

def revConvertTime(timeInt):
    timeHr = timeInt/60
    timeMin = timeInt%60
    return str(timeHr) + ':' + str(timeMin)

def isLastThursdayOfMonth(currentDate):
    dateString = str(currentDate)
    dt = date(int(dateString[:4]), int(dateString[4:6]),int(dateString[6:8]))
    thursdayDate = (dt + relativedelta(day=31, weekday=TH(-1)))
    return thursdayDate.strftime("%Y%m%d") == dateString

def getMarketDetails(stockType):
    if stockType == 'INTRADAY':
        marketOpen = 570
        marketClose = 900
    elif stockType == 'FUTURES':
        marketOpen = 540
        marketClose = 930
    return marketOpen, marketClose
