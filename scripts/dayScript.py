from classes.DayEntry import Day
from classes.MinuteEntry import Minute
from classes.TradeEntry import Trade
from utils.TimeUtil import getMarketDetails
from classes.RenkoEntry import Renko

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

from utils.RenkoUtil import *

def renkoScript(df, param, day, renkoDeque, stockType, verbose = False):
    if day.currentTrade:
        trade = day.currentTrade
    marketOpen, marketClose = getMarketDetails(stockType)
    for row in df.iterrows():
        minute = Minute(row)
        # minute.toString(verbose)
        renkoDeque = generateRenko(minute, renkoDeque, param.brickHeight, param.stepCount, verbose)
        if len(renkoDeque) == param.stepCount:
            if marketOpen <= minute.time < marketClose:
                if day.boughtFlag == 0:
                    #market enter logic
                    if getEmotion(renkoDeque) == param.stepCount:
                        #buy
                        day.boughtFlag = 1
                        trade = Trade(renkoDeque[-1].high, minute.time, 0, 0, day.boughtFlag)
                        day.currentTrade = trade
                    elif getEmotion(renkoDeque) == -1 * param.stepCount:
                        #sell
                        day.boughtFlag = -1
                        trade = Trade(renkoDeque[-1].low, minute.time, 0, 0, day.boughtFlag)
                        day.currentTrade = trade

                elif day.boughtFlag == 1:
                    #market exit logic (when already bought)
                    if renkoExitLogic(renkoDeque, param.stepCount, day.boughtFlag):
                        trade.exitTrade('renkoExit', minute.time, renkoDeque[-1].low, verbose)
                        day.addTrade(trade)
                else:
                    #market exit logic (when already sold)
                    if renkoExitLogic(renkoDeque, param.stepCount, day.boughtFlag):
                        trade.exitTrade('renkoExit', minute.time, renkoDeque[-1].high, verbose)
                        day.addTrade(trade)

            elif minute.time >= marketClose and day.sellEndOfDay:
                if day.boughtFlag == 1:
                    trade.exitTrade('eod', minute.time, minute.closingPrice, verbose)
                    day.addTrade(trade)
                elif day.boughtFlag == -1:
                    trade.exitTrade('eod', minute.time, minute.closingPrice, verbose)
                    day.addTrade(trade)

    return day
