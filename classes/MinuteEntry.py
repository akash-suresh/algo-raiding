from utils.TimeUtil import convertTime


def parseMinuteData(minuteData, shortTerm, longTerm):
    time = convertTime(minuteData[1].time)
    openingPrice = minuteData[1].openingPrice
    low = minuteData[1].low
    high = minuteData[1].high
    closingPrice = minuteData[1].closingPrice
    diff = minuteData[1]["MA_" + str(longTerm)] - minuteData[1]["MA_" + str(shortTerm)]
    return time, openingPrice, low, high, closingPrice, diff


class Minute:

    def __init__(self, minuteData, shortTerm, longTerm):
        self.time, self.openingPrice, self.low, self.high, self.closingPrice, self.diff = parseMinuteData(minuteData, shortTerm, longTerm)
        self.listPrice = 0.5 * (self.openingPrice + self.closingPrice)
