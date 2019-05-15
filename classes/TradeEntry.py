from utils.TimeUtil import revConvertTime
import logging

class Trade:

    def __init__(self, enterPrice, timeEntered, targetPercentage, stopLossPercentage, tradeType):
        self.enterPrice = enterPrice
        self.targetPercentage = targetPercentage
        self.stopLossPercentage = stopLossPercentage
        self.lossWindow = self.enterPrice * stopLossPercentage
        self.timeEntered = timeEntered
        self.tradeType = tradeType
        self.targetPrice, self.stopLossPrice = self.populateBasedOnType()
        self.exitPrice = None
        self.timeExited = None
        self.profitPercentage = None

    def populateBasedOnType(self):
        if self.tradeType == 1:
            targetMargin = 1 + self.targetPercentage
            stopLossMargin = 1 - self.stopLossPercentage
        else:
            targetMargin = 1 - self.targetPercentage
            stopLossMargin = 1 + self.stopLossPercentage
        targetPrice = self.enterPrice * targetMargin
        stopLossPrice = self.enterPrice * stopLossMargin
        return targetPrice, stopLossPrice

    def exitTrade(self, exitType, timeExited, verbose = False):
        self.exitTrade(exitType, timeExited, 0, verbose)

    def exitTrade(self, exitType, timeExited, eodPrice, verbose = False):
        logging.debug('Inside exitTrade fn')
        brokerage = 0.0002
        self.timeExited = timeExited
        if exitType == 'stopLoss':
            self.exitPrice = self.stopLossPrice
        elif exitType == 'target':
            self.exitPrice = self.targetPrice
        elif exitType == 'eod' or exitType == 'renkoExit':
            self.exitPrice = eodPrice
        #todo - combine
        if self.tradeType == 1:
            self.calculateProfitPercentage(self.enterPrice, self.exitPrice, brokerage)
        elif self.tradeType == -1:
            self.calculateProfitPercentage(self.exitPrice, self.enterPrice, brokerage)
        self.toString(verbose)

    def toString(self, verbose = False):
        if verbose:
            print("{:d}, {:.4f}, {:.4f}, {:.4f}".format(self.tradeType, self.enterPrice, self.exitPrice, self.profitPercentage))
            print("{} {}\n".format(self.timeEntered, self.timeExited))

    def calculateProfitPercentage(self, buyPrice, sellPrice, brokerage):
        self.profitPercentage = 100*(sellPrice*(1-brokerage) - buyPrice)/(1.0*buyPrice)

    def updateTrail(self, listPrice):
        trail = abs(listPrice - self.stopLossPrice)
        if trail > self.lossWindow:
            climb = trail - self.lossWindow
            self.stopLossPrice += self.tradeType*climb
