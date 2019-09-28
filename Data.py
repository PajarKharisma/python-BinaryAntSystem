class Barang:
    def __init__(self):
        pass

    def __init__(self, name, profit, bobot):
        self.__name = name
        self.__profit = profit
        self.__bobot = bobot
        self.__utility =  float("%.2f" % round(profit / bobot, 2))

    def getName(self):
        return self.__name

    def getProfit(self):
        return self.__profit

    def getBobot(self):
        return self.__bobot

    def getUtility(self):
        return self.__utility

class Knapsack:
    def __init__(self):
        pass

    def __init__(self, name, kapasitas):
        self.__name = name
        self.__kapasitas = kapasitas
        self.__barang = []
        
    def getName(self):
        return self.__name

    def getKapasitas(self):
        return self.__kapasitas

    def add(self, barang):
        self.__barang.append(barang)

    def drop(self):
        del self.__barang[-1]
    
    def getBarang(self):
        return self.__barang
    
    def getBobotBarang(self):
        total = 0
        for i in self.__barang:
            total += i.getBobot() 
        return total