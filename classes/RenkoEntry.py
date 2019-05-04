class Renko:
    def __init__(self, low, high):
        self.low = low
        self.high = high
        self.renkoType = self.getRenkoType()

    def getRenkoType(self):
        if self.low > self.high:
            renkoType = -1
        elif self.high > self.low:
            renkoType = 1
        else:
            renkoType = 0
        return renkoType

    def toString(self):
        print('low - {}, high - {}, type - {}'.format(self.low, self.high, self.renkoType))
