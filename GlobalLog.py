class GlobalLog:
    def __init__(self, sgb, profit, iterasi):
        self.__sgb = sgb
        self.__profit = profit
        self.__iterasi = iterasi

    def getSgb(self):
        return self.__sgb

    def getProfit(self):
        return self.__profit

    def getIterasi(self):
        return self.__iterasi