import pandas as pd
import random
from Data import Knapsack
from Data import Barang

class Iterasi:
    def __init__(self, barangs, knapsacks, evaporasi):
        self.__barangs = barangs[:]
        self.__knapsacks = knapsacks[:]
        self.__evaporasi = evaporasi

        self.__ndata = len(barangs)
        self.__randList = []
        self.__freeItem = []

        self.__sgb = None

    def barangSort(self):
        self.__barangs.sort(key=lambda x: x.getUtility(), reverse=True)

    def randomValue(self):
        del self.__randList[:]
        for i in range(3):
            self.__randList.append([])

        index = 0
        for i in range(3):
            while len(self.__randList[i]) < 5:
                randNum = random.randint(0, self.__ndata - 1)
                if not any(randNum in sublist for sublist in self.__randList):
                    self.__randList[i].append(randNum)

    def randomSolution(self):
        for knap, randEl in zip(self.__knapsacks, self.__randList):
            del knap.getBarang()[:]
            for i in randEl:
                knap.add(self.__barangs[i])
    
    def dropPhase(self):
        for knap in self.__knapsacks:
            knap.sortBarang()
            while(knap.getKapasitas() < knap.getBobotBarang()):
                knap.drop()

    def getFreeItems(self):
        del self.__freeItem[:]
        for b in self.__barangs:
            isExist = False
            for k in self.__knapsacks:
                if any(b.getName() in knapBarang.getName() for knapBarang in k.getBarang()):
                    isExist = True
                    break
            if not isExist:
                self.__freeItem.append(b)

    def addPhase(self):
        for knap in self.__knapsacks:
            for fi in self.__freeItem:
                if fi.getBobot() + knap.getBobotBarang() <= knap.getKapasitas():
                    knap.add(fi)
                    self.__freeItem.remove(fi)

    def calculateCF(self, tj0, tj1):
        result = 0
        for j0, j1 in zip(tj0, tj1):
            result += abs(j0 - j1)
        
        return result / self.__ndata
    
    def getProfit(self):
        result = 0
        for knap in self.__knapsacks:
            for i in knap.getBarang():
                # print('nama : ', i.getName())
                # print('profit : ', i.getProfit())
                result += i.getProfit()
        
        result = float("%.2f" % round(result, 2))
        return self.__sgb, result

    def getW(self, cf):
        wib = 0
        wrb = 0
        wgb = 0
        restart = False

        if cf < 0.2:
            wib = 1
            wrb = 0
            wgb = 0
        elif cf >= 0.2 and cf < 0.4:
            wib = 2/3
            wrb = 1/3
            wgb = 0
        elif cf >= 0.4 and cf < 0.6:
            wib = 1/3
            wrb = 2/3
            wgb = 0
        elif cf >= 0.6 and cf < 0.8:
            wib = 0
            wrb = 1
            wgb = 0
        elif cf >= 0.8 and cf < 0.83:
            wib = 0
            wrb = 0
            wgb = 1
        else:
            restart = True

        return wib, wrb, wgb, restart

    def testing(self):
        self.barangSort()
        self.randomValue()
        self.randomSolution()
        
        self.printKnapsacks()

    def pheromoneUpdate(self, tj01, tj11, isInit, sgbVal, srbVal):
        self.barangSort()
        self.randomValue()
        self.randomSolution()
        print('-'*30)
        print('Hasil acak : ')
        self.printKnapsacks()
        self.dropPhase()
        self.getFreeItems()
        self.addPhase()
        print('-'*30)
        print('Hasil akhir : ')
        self.printKnapsacks()

        cf = self.calculateCF(tj01, tj11)
        wib, wrb, wgb, restart = self.getW(cf)

        sib = []
        for i in self.__barangs:
            if not any(i.getName() in j.getName() for j in self.__freeItem):
                sib.append(1)
            else:
                sib.append(0)
        self.__sgb = sib[:]

        sgb = None
        if isInit:
            srb = [0] * self.__ndata
            sgb = sib[:]
        else:
            srb = srbVal[:]
            sgb = sgbVal[:]

        sibVal = False
        sgbVal = False
        if sib == sgb:
            sibVal = True
            sgbVal = True
        if sib == srb:
            sibVal = True
        if restart and sgb == srb:
            sgbVal = True

        for i in range(self.__ndata):
            sib[i] *= wib
            srb[i] *= wrb
            sgb[i] *= wgb

        wx = []
        for i in range(self.__ndata):
            wx.append(sib[i] + srb[i] + sgb[i])

        tj02 = []
        for i in range(self.__ndata):
            a = (1 - self.__evaporasi) * tj01[i]
            b = self.__evaporasi * wx[i]
            tj02.append(a + b)

        tj12 = []
        for i in range(self.__ndata):
            val = 1 - tj02[i]
            tj12.append(val)

        cfUpdate = self.calculateCF(tj02, tj12)
        return cf, cfUpdate, tj02, tj12, restart, sibVal, sgbVal

    def printKnapsacks(self):
        print('-'*60)
        totalBobot = 0
        totalProfit = 0
        for knap in self.__knapsacks:
            for i in knap.getBarang():
                print(i.getName(), end=' ')
                print('dengan bobot\t: ', i.getBobot())
            totalBobot += knap.getBobotBarang()
            totalProfit += knap.getProfitBarang()
            
            print('TOTAL BOBOT : ', float("%.2f" % round(knap.getBobotBarang(), 2)))
            print('TOTAL PROFIT : ', float("%.2f" % round(knap.getProfitBarang(), 2)))
            print()
        print('Total semua Bobot : ', float("%.2f" % round(totalBobot, 2)))
        print('Total semua Profit : ', float("%.2f" % round(totalProfit, 2)))