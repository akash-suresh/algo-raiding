from utils.TimeUtil import convertTime, revConvertTime, revConvertDateTime


def parseMinuteData(minuteData, shortTerm, longTerm):
    time = convertTime(minuteData[1].time)
    openingPrice = minuteData[1].openingPrice
    low = minuteData[1].low
    high = minuteData[1].high
    closingPrice = minuteData[1].closingPrice
    diff = None
    if shortTerm>0 and longTerm>0:
        diff = minuteData[1]["MA_" + str(longTerm)] - minuteData[1]["MA_" + str(shortTerm)]
    return time, openingPrice, low, high, closingPrice, diff

class Minute:

    # def __init__(self, minuteData, shortTerm = 0, longTerm = 0):
    #     self.time, self.openingPrice, self.low, self.high, self.closingPrice, self.diff = parseMinuteData(minuteData, shortTerm, longTerm)
    #     self.listPrice = 0.5 * (self.openingPrice + self.closingPrice)

    def __init__(self, timestamp, last_price):
        # self.openingPrice = None
        # self.low = None
        # self.high = None
        # self.closingPrice= None
        # self.diff = None
        self.time = timestamp
        self.listPrice = last_price

    def toString(self, verbose):
        if verbose:
            print 'Time: {}, ListPrice: {}'.format(self.time, self.listPrice)
