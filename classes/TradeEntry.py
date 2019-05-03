from utils.TimeUtil import revConvertTime

class TradeEntry:

    def __init__(self, enterPrice, timeEntered, targetPercentage, stopLossPercentage, tradeType):
        self._enterPrice = enterPrice
        self._targetPercentage = targetPercentage
        self._stopLossPercentage = stopLossPercentage
        self._lossWindow = self._enterPrice * stopLossPercentage
        self._timeEntered = timeEntered
        self._tradeType = tradeType
        self._targetPrice, self._stopLossPrice = self.populateBasedOnType()
        self._exitPrice = None
        self._timeExited = None
        self._profitPercentage = None
        pass

    def populateBasedOnType(self):
        if self._tradeType == 1:
            targetMargin = 1 + self._targetPercentage
            stopLossMargin = 1 - self._stopLossPercentage
        else:
            targetMargin = 1 - self._targetPercentage
            stopLossMargin = 1 + self._stopLossPercentage

        targetPrice = self._enterPrice * targetMargin
        stopLossPrice = self._enterPrice * stopLossMargin
        return targetPrice, stopLossPrice

    def exitTrade(self, exitType, timeExited, verbose = False):
        self.exitTrade(exitType, timeExited, 0, verbose)

    def exitTrade(self, exitType, timeExited, eodPrice, verbose = False):
        brokerage = 0.0002
        self._timeExited = timeExited
        if exitType == 'stopLoss':
            self._exitPrice = self._stopLossPrice
        elif exitType == 'target':
            self._exitPrice = self._targetPrice
        elif exitType == 'eod':
            self._exitPrice = eodPrice
        self._profitPercentage = 100*(self._exitPrice*(1-brokerage) - self._enterPrice)/(1.0*self._enterPrice)
        if verbose:
            print(self._enterPrice, self._exitPrice, revConvertTime(self._timeEntered), revConvertTime(self._timeExited), self._profitPercentage)

    def updateTrail(self, listPrice):
        # #trailing stopLoss stopGain calculations.
        #check with raju
        # trail = (listPrice - self._stopLossPrice)
        # if abs(trail) > self._lossWindow:
        #     climb = abs(trail) - self._lossWindow
        #     self._stopLossPrice += climb

        if self._tradeType == 1:
            trail = (listPrice - self._stopLossPrice)
            if trail > self._lossWindow:
                climb = trail - self._lossWindow
                self._stopLossPrice += climb
        else:
            trail = (self._stopLossPrice - listPrice)
            if trail > self._lossWindow:
                climb = trail - self._lossWindow
                self._stopLossPrice -= climb

