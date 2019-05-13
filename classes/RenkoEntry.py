from utils.TimeUtil import revConvertDateTime

class Renko:
    def __init__(self, low, high, renkoType, time):
        self.low = low
        self.high = high
        self.renkoType = renkoType
        self.time = time

    def toString(self, verbose=False):
        if verbose:
            print('time: {}, low: {}, high: {}, type: {}'.format(self.time, self.low, self.high, self.renkoType))
