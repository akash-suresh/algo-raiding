from utils.TimeUtil import revConvertTime

class Renko:
    def __init__(self, low, high, renkoType, time):
        self.low = low
        self.high = high
        self.renkoType = renkoType
        self.time = time

    def toString(self, verbose):
        if verbose:
            print('time: {}, low: {}, high: {}, type: {}'.format(revConvertTime(self.time), self.low, self.high, self.renkoType))
