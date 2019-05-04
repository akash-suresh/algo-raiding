class ParamEntry:
    def __init__(self, params, stockName):
        self.shortTerm = params['shortTerm']
        self.longTerm = params['longTerm']
        self.targetPercentage = params['targetPercentage']
        self.stopLossPercentage = params['stopLossPercentage']
        self.entryDifference = params['entryDifference']
        self.stockName = stockName
        self.profitPercentage = None


    def getCsvPoint(self):
        newPoint = {'stockName':self.stockName,
                     'shortTerm':self.shortTerm,
                     'longTerm':self.longTerm,
                     'targetPercentage':self.targetPercentage,
                     'stopLossPercentage':self.stopLossPercentage,
                     'entryDifference':self.entryDifference,
                     'profitPercentage':self.profitPercentage,
                     }
        return newPoint

    def toString(self):
        print 'Stock Name: {}, ShortTerm: {}, LongTerm: {}, Target per {}, StopLossPer {} ' \
              'EntryDiff: {}, ProfitPer: {}'.format(self.stockName, self.shortTerm, self.longTerm, self.targetPercentage, self.stopLossPercentage,
                                                    self.entryDifference, self.profitPercentage)
    # @property
    # def shortTerm(self):
    #     return self.shortTerm
    #
    # @shortTerm.setter
    # def shortTerm(self, value):
    #     self.shortTerm = value


