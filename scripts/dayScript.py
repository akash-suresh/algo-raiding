from classes.DayEntry import Day
from classes.MinuteEntry import Minute
from classes.TradeEntry import Trade

def getMarketDetails(stockType):
    if stockType == 'INTRADAY':
        marketOpen = 570
        marketClose = 900
    elif stockType == 'FUTURES':
        marketOpen = 540
        marketClose = 930
    return marketOpen, marketClose

def dayScript(df, param, day, stockType, verbose = False):
    # day = Day(0, money)
    if day.currentTrade:
        trade = day.currentTrade
    marketOpen, marketClose = getMarketDetails(stockType)
    for row in df.iterrows():
        minute = Minute(row, param.shortTerm, param.longTerm)
        if marketOpen <= minute.time < marketClose:
            if day.boughtFlag == 0:
                #market enter logic
                if 0 < minute.diff < param.entryDifference*minute.listPrice:
                    #buy
                    day.boughtFlag = 1
                    trade = Trade(minute.listPrice, minute.time, param.targetPercentage, param.stopLossPercentage, day.boughtFlag)
                    day.currentTrade = trade
                elif 0 > minute.diff > -1*param.entryDifference*minute.listPrice:
                    #sell
                    day.boughtFlag = -1
                    trade = Trade(minute.listPrice, minute.time, param.targetPercentage, param.stopLossPercentage, day.boughtFlag)
                    day.currentTrade = trade
            elif day.boughtFlag == 1:
                #market exit logic (when already bought)
                if minute.high > trade.targetPrice:
                    trade.exitTrade('target', minute.time, verbose)
                    day.addTrade(trade)
                elif trade.stopLossPrice > minute.low:
                    trade.exitTrade('stopLoss', minute.time, verbose)
                    day.addTrade(trade)

                trade.updateTrail(minute.listPrice)
            else:
                #market exit logic (when already sold)
                if trade.targetPrice > minute.low:
                    trade.exitTrade('target', minute.time, verbose)
                    day.addTrade(trade)
                elif minute.high > trade.stopLossPrice:
                    trade.exitTrade('stopLoss', minute.time, verbose)
                    day.addTrade(trade)

                trade.updateTrail(minute.listPrice)

        elif minute.time >= marketClose and day.sellEndOfDay:
            if day.boughtFlag == 1:
                trade.exitTrade('eod', minute.time, minute.closingPrice, verbose)
                day.addTrade(trade)
            elif day.boughtFlag == -1:
                trade.exitTrade('eod', minute.time, minute.closingPrice, verbose)
                day.addTrade(trade)

    return day
