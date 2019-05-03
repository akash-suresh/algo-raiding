from utils.TimeUtil import revConvertTime

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
        brokerage = 0.0002
        self.timeExited = timeExited
        if exitType == 'stopLoss':
            self.exitPrice = self.stopLossPrice
        elif exitType == 'target':
            self.exitPrice = self.targetPrice
        elif exitType == 'eod':
            self.exitPrice = eodPrice
        #todo - combine
        if self.tradeType == 1:
            self.calculateProfitPercentage(self.enterPrice, self.exitPrice, brokerage)
        elif self.tradeType == -1:
            self.calculateProfitPercentage(self.exitPrice, self.enterPrice, brokerage)
        if verbose:
            print(self.tradeType, self.enterPrice, self.exitPrice, revConvertTime(self.timeEntered), revConvertTime(self.timeExited), self.profitPercentage)

    def calculateProfitPercentage(self, buyPrice, sellPrice, brokerage):
        self.profitPercentage = 100*(sellPrice*(1-brokerage) - buyPrice)/(1.0*buyPrice)

    def updateTrail(self, listPrice):
        trail = abs(listPrice - self.stopLossPrice)
        if trail > self.lossWindow:
            climb = trail - self.lossWindow
            self.stopLossPrice += self.tradeType*climb
