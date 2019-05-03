class Day:

    def __init__(self, boughtFlag = 0, money = 1):
        self.boughtFlag = boughtFlag
        self.dailyTrades = 0
        self.money = money
        self.trades = []

    def addTrade(self, trade):
        self.money = self.money*(1 + trade.profitPercentage/100.0)
        self.trades.append(trade)
        self.dailyTrades = len(self.trades)
        self.reset()

    def getLastTrade(self):
        return self.trades[self.dailyTrades - 1]

    def reset(self):
        self.boughtFlag = 0

    # @property
    # def enterPrice(self):
    #     return self.enterPrice
    #
    # @enterPrice.setter
    # def enterPrice(self, value):
    #     self.enterPrice = value
    #
    # #
