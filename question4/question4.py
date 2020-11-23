import numpy as np
from SimulationMaintenanceBus import SimulationMaintenanceBus

def lire_txt(str_file, donne1,donne2):
    f = open(str_file,'r')
    result = list()
    for line in open(str_file):
        line = f.readline()
        temp = line.split()
        donne1.append(float(temp[0]))
        donne2.append(float(temp[1]))
        result.append(line)
    f.close()
    
def faire_tri_arriveTemp(donnee,result):
    index = 0
    O1 = 0
    O2 = 0
    O3 = 0
    O4 = 0
    O5 = 0
    while(donnee[index] < 32):
        O1 = O1 + 1
        index  = index + 1
        
    while(donnee[index] >= 32 and donnee[index] < 64):
        O2 = O2 + 1
        index  = index + 1
        
    while(donnee[index] >= 64 and donnee[index] < 96):
        O3 = O3 + 1
        index  = index + 1

    while(donnee[index] >= 96 and donnee[index] < 128):
        O4 = O4 + 1
        index  = index + 1

    for j in range(index, len(donnee)):
        O5 = O5 + 1
        index  = index + 1
    result.append(O1)
    result.append(O2)
    result.append(O3)
    result.append(O4)
    result.append(O5)
 
def faire_tri_dureeControle(donnee,result):
    donnee.sort()
    index = 0
    O1 = 0
    O2 = 0
    O3 = 0
    O4 = 0
    O5 = 0

    while(donnee[index] >= 1/4 and donnee[index] < 5/12):
        O1 = O1 + 1
        index  = index + 1
        
    while(donnee[index] >= 5/12 and donnee[index] < 7/12):
        O2 = O2 + 1
        index  = index + 1

    while(donnee[index] >= 7/12 and donnee[index] < 9/12):
        O3 = O3 + 1
        index  = index + 1
        
    while(donnee[index] >= 9/12 and donnee[index] < 11/12):
        O4 = O4 + 1
        index  = index + 1
        
    for j in range(index, len(donnee)):
        O5 = O5 + 1
        index  = index + 1
    result.append(O1)
    result.append(O2)
    result.append(O3)
    result.append(O4)
    result.append(O5)

def calculZarriveTemp(donnee, arrObser,arrTheri):
    faire_tri_arriveTemp(donnee,arrObser)
    sb1 = SimulationMaintenanceBus()
    sb1.simulateur(160,1)
    list1 = sb1.arrive_temps
    list1.sort()

    faire_tri_arriveTemp(list1,arrTheri)
    z = 0
    for k in range(5):
        temp = arrObser[k] - arrTheri[k]
        z = z + pow(temp, 2)/arrTheri[k]
    return z

def calculZdureeControle(donnee, arrObser,arrTheri):
    faire_tri_dureeControle(donnee,arrObser)
    sb1 = SimulationMaintenanceBus()
    sb1.simulateur(160,1)
    list1 = sb1.duree_controle
    list1.sort()
    
    faire_tri_dureeControle(list1,arrTheri)
    z = 0
    for k in range(5):
        temp = arrObser[k] - arrTheri[k]
        z = z + pow(temp, 2)/arrTheri[k]
    return z

donneArriveControle = []
donneDureeControle = []

#effectif observe pour arrive temps
# 0-159 divise par 5.
observeArriveTemp = []
#effectif theorique
theoriqueArriveTemp = []


#effectif observe pour duree controle
# 0-159 divise par 5.
observeDureeControle = []
#effectif theorique pour duree controle
theoriqueDureeControle = []


lire_txt('DonneesControle.txt',donneArriveControle,donneDureeControle)
result_arrive_temp = calculZarriveTemp(donneArriveControle,observeArriveTemp, theoriqueArriveTemp)

donneDureeControle.sort()
result_duree_controle = calculZdureeControle(donneDureeControle, observeDureeControle,theoriqueDureeControle)

print("Résultat du test du chi carré du arrive de temps:"+str(result_arrive_temp))
print("Résultat du test du chi carré du duree controle:" + str(result_duree_controle))


