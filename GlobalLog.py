class GlobalLog:
    def __init__(self, sgb, profit):
        self.__sgb = sgb
        self.__profit = profit

    def getSgb(self):
        return self.__sgb

    def getProfit(self):
        return self.__profit