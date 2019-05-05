class Renko:
    def __init__(self, low, high, renkoType):
        self.low = low
        self.high = high
        self.renkoType = renkoType

    def toString(self, verbose):
        if verbose:
            print('low: {}, high: {}, type: {}'.format(self.low, self.high, self.renkoType))
