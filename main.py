import pandas as pd
import random
from Data import Knapsack
from Data import Barang
from Iterasi import Iterasi
from GlobalLog import GlobalLog

# IMPORT DATA DARI EXCEL
dataKnapsack = pd.read_excel (r'input\data.xlsx', sheet_name='knapsack')
dataBarang = pd.read_excel (r'input\data.xlsx', sheet_name='barang')

dataKnapsack = dataKnapsack.to_numpy()
dataBarang = dataBarang.to_numpy()

# MEMASUKAN DATA KE DALAM LIST OBJECT
barangs = []
knapsacks = []

for index, i in enumerate(dataBarang):
    barangs.append(Barang(i[0], i[1], i[2]))

for index, i in enumerate(dataKnapsack):
    knapsacks.append(Knapsack(i[0], i[1]))

ndata = len(barangs)
iterasiMax = 10
evaporasi = 0.25
pheromone = 0.5
tj0 = [pheromone] * ndata
tj1 = [pheromone] * ndata
iterasi = [None] * iterasiMax
isInit = True
globalHst = []

srb = [0] * ndata
sgb = [0] * ndata

for i in range(iterasiMax):
    print('-'*60)
    print('Itearasi : ', (i+1))
    barang = barangs[:]
    knapsack = knapsacks[:]
    iterasi[i] = Iterasi(barang, knapsack, evaporasi)
    # iterasi[i].testing()
    cf, nextCf, tj0, tj1, restart = iterasi[i].pheromoneUpdate(tj0, tj1, isInit, sgb, srb)
    cf = float("%.2f" % round(cf, 2))
    isInit = False
    
    sgb, profit = iterasi[i].getProfit()
    log = GlobalLog(sgb, profit)
    globalHst.append(log)
    globalHst.sort(key=lambda x: x.getProfit(), reverse=True)
    sgb = globalHst[0].getSgb()[:]

    if restart:
        sgb = globalHst[0].getSgb()[:]
        tj0 = [pheromone] * ndata
        tj1 = [pheromone] * ndata

    del barang[:]
    del knapsack[:]
    print('Iterasi ', (i + 1), end=' | ')
    print('cf : %s' % (cf), end=' \n ')
    # print('Profit : %s' % (iterasi[i].getProfit()))
    print('-' * 50)

for i in globalHst:
    print(i.getSgb(), ' | ', i.getProfit())