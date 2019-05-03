class TradeEntry:

    def __init__(self, boughtFlag = 0, money = 1):
        self._boughtFlag = boughtFlag
        self._dailyTrades = 0
        self._money = money
        self._trades = []
        pass

    def addTrade(self, trade):
        self._money = self._money*(1 + trade.profitPercentage/100)
        self._trades.append(trade)
        self._dailyTrades = len(self._trades)
        self.reset()

    def getLastTrade(self):
        return self._trades[self._dailyTrades - 1]

    def reset(self):
        self._boughtFlag = 0
    #
    # @property
    # def enterPrice(self):
    #     return self._enterPrice
    #
    # @enterPrice.setter
    # def enterPrice(self, value):
    #     self._enterPrice = value
    #
    # #
