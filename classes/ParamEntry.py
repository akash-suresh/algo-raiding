class ParamEntry:
    def __init__(self, params, stockName):
        self._shortTerm = params['shortTerm']
        self._longTerm = params['longTerm']
        self._targetPercentage = params['targetPercentage']
        self._stopLossPercentage = params['stopLossPercentage']
        self._entryDifference = params['entryDifference']
        self._stockName = stockName
        self._profitPercentage = None

    def getCsvPoint(self):
        newPoint = {'stockName':self._stockName,
                     'shortTerm':self._shortTerm,
                     'longTerm':self._longTerm,
                     'targetPercentage':self._targetPercentage,
                     'stopLossPercentage':self._stopLossPercentage,
                     'entryDifference':self._entryDifference,
                     'profitPercentage':self._profitPercentage,
                     }
        return newPoint
