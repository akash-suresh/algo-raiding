class Year:
    def __init__(self):
        self.days = []
        self.trades = []

    def dayOver(self, day):
        self.days.append(day)
        map(lambda trade : self.trades.append(trade), day.trades)
