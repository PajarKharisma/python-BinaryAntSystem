import pandas as pd
import random
from Data import Knapsack
from Data import Barang

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
barangs.sort(key=lambda x: x.getUtility(), reverse=True)

for index, i in enumerate(dataKnapsack):
    knapsacks.append(Knapsack(i[0], i[1]))

print('DATA KNAPSACK')
for knapsack in knapsacks:
    print('Nama : %s |Kapasitas : %s' % (knapsack.getName(), knapsack.getKapasitas()))

print()
print('DATA BARANG SETELAH DILAKUKAN PROSES SORTING')
for barang in barangs:
    print('Nama : %s \t|Profit : %s \t|Bobot : %s' % (barang.getName(), barang.getProfit(), barang.getBobot()))

# RANDOM NILAI UNTUK MEMILIH BARANG YANG AKAN DIMASUKAN DALAM KNAPSACK
randList = []
for i in range(3):
    randList.append([])
    
index = 0
for i in range(3):
    while len(randList[i]) < 5:
        randNum = random.randint(0,15)
        if not any(randNum in sublist for sublist in randList):
            randList[i].append(randNum)
    index += 1

# MEMILIH BARANG RANDOM UNTUK DIMASUKAN DALAM KNAPSACK
for knap, randEl in zip(knapsacks, randList):
    for i in randEl:
        knap.add(barangs[i])

print()
print('='*60)        
print('ISI KNAPSACK SEBELUM DILAKUKAN FASE DROP')
for knap in knapsacks:
    for i in knap.getBarang():
        print(i.getName(), end=' ')
        print('dengan bobot\t: ', i.getBobot())
    print('total bobot : ', knap.getBobotBarang())
    print()

# FASE DROP UNTUK MENGELUARKAN BARANG YANG MELEBIHI KAPASITAS KNAPSACK
for knap in knapsacks:
    while(knap.getKapasitas() < knap.getBobotBarang()):
        knap.drop()

print()
print('='*60)
print('SETELAH DILAKUKAN FASE DROP')
for knap in knapsacks:
    for i in knap.getBarang():
        print(i.getName(), end=' ')
        print('dengan bobot\t: ', i.getBobot())
    print('total bobot : ', knap.getBobotBarang())
    print()

# MEMBUAT LIST UNTUK MENAMPUNG BARANG YANG BELUM MASUK KE DALAM KNAPSACK
freeItem = []

for b in barangs:
    isExist = False
    for k in knapsacks:
        if any(b.getName() in knapBarang.getName() for knapBarang in k.getBarang()):
            isExist = True
            break
    if not isExist:
        freeItem.append(b)

print()
print('='*60)
print('DATA BARANG YANG BELUM MASUK DALAM KNAPSACK')
for fi in freeItem:
    print('Nama : %s \t|Profit : %s \t|Bobot : %s' % (fi.getName(), fi.getProfit(), fi.getBobot()))

# FASE ADD UNTUK MENAMBAH BARANG HINGGA MAXIMUM KAPASITAS KNAPSACK
for knap in knapsacks:
    for fi in freeItem:
        if fi.getBobot() + knap.getBobotBarang() <= knap.getKapasitas():
            knap.add(fi)
            freeItem.remove(fi)

print()
print('='*60)
print('SETELAH DILAKUKAN FASE ADD')
for knap in knapsacks:
    for i in knap.getBarang():
        print(i.getName(), end=' ')
        print('dengan bobot\t: ', i.getBobot())
    print('total bobot : ', knap.getBobotBarang())
    print()

# HITUNG NILAI CF
pheromone = 0.5
tj01 = [pheromone] * 16
tj11 = [pheromone] * 16

cf = 0
for tj0, tj1 in zip(tj01, tj11):
    cf += abs(tj0 - tj1)

cf = cf / 16
print()
print('='*60)
print('NILAI CF ADALAH : ', cf)

# MENENTUKAN NILAI WIB WRB WGB
wib = 0
wrb = 0
wgb = 0

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
elif cf >= 0.8 and cf < 0.85:
    wib = 0
    wrb = 0
    wgb = 1
else:
    pheromone = 0.5

print()
print('='*60)  
print('wib : ', wib)
print('wrb : ', wrb)
print('wgb : ', wgb)

# PHEROMONE UPDATE
sib = []
for i in barangs:
    if not any(i.getName() in j.getName() for j in freeItem):
        sib.append(1)
    else:
        sib.append(0)

initValue = 0
srb = [initValue] * 16
sgb = sib[:]

for i in range(16):
    sib[i] *= wib
    srb[i] *= wrb
    sgb[i] *= wgb

print()
print('sib : ', sib)
print('srb : ', srb)
print('sgb : ', sgb)

# MENGHITUNG WX
wx = []
for i in range(16):
    wx.append(sib[i] + srb[i] + sgb[i])

print()
print('='*60)  
print('wx : ', wx)

evaporasi = 0.25

# MENGHITUNG NILAI TJ02 DAN TJ12
tj02 = []
for i in range(16):
    a = (1 - evaporasi) * tj01[i]
    b = evaporasi * wx[i]
    tj02.append(a + b)

tj12 = []
for i in range(16):
    val = 1 - tj02[i]
    tj12.append(val)

print()
print('='*60)  
print('tj02 : ', tj02)
print('tj12 : ', tj12)

# MENGHITUNG UPDATE CF
cf = 0
for tj0, tj1 in zip(tj02, tj12):
    cf += abs(tj0 - tj1)

cf = cf / 16
print()
print('='*60)
print('NILAI CF ADALAH : ', cf)
