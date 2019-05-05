class Day:

    def __init__(self, boughtFlag = 0, money = 1, sellEndOfDay = True):
        self.boughtFlag = boughtFlag
        self.dailyTrades = 0
        self.money = money
        self.trades = []
        self.currentTrade = None
        self.sellEndOfDay = sellEndOfDay

    def initializeNextDay(self, sellEndOfDay = True):
        nextDay = Day(self.boughtFlag, self.money, sellEndOfDay)
        nextDay.currentTrade = self.currentTrade
        return nextDay

    def addTrade(self, trade):
        self.money = self.money*(1 + trade.profitPercentage/100.0)
        self.trades.append(trade)
        self.dailyTrades = len(self.trades)
        self.reset()

    def getLastTrade(self):
        return self.trades[self.dailyTrades - 1]

    def reset(self):
        self.boughtFlag = 0
        self.currentTrade = None

    def printOpenTrade(self):
        if self.currentTrade:
            print 'OpenTrade - Enter Price: {}, Enter Time: {}, TradeType: {}'.format(self.currentTrade.enterPrice, self.currentTrade.timeEntered, self.currentTrade.tradeType)

    def printAllTrades(self, verbose = False):
        for trade in self.trades:
            trade.toString(verbose)

    # @property
    # def enterPrice(self):
    #     return self.enterPrice
    #
    # @enterPrice.setter
    # def enterPrice(self, value):
    #     self.enterPrice = value
    #
    # #
