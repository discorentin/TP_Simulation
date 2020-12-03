import numpy as np

import math

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
    donnee.sort()
    index = 0
    O1 = 0
    O2 = 0
    O3 = 0
    O4 = 0
    O5 = 0
    O6 = 0
    O7 = 0

    while(donnee[index] < 0.5):
        O1 = O1 + 1
        index  = index + 1
        
    while(donnee[index] >= 0.5 and donnee[index] < 1.0):
        O2 = O2 + 1
        index  = index + 1
        
    while(donnee[index] >= 1.0 and donnee[index] < 1.5):
        O3 = O3 + 1
        index  = index + 1

    while(donnee[index] >= 1.5 and donnee[index] < 2.0):
        O4 = O4 + 1
        index  = index + 1
        
    while(donnee[index] >= 2.0 and donnee[index] < 2.5):
        O5 = O5 + 1
        index  = index + 1
 
    while(donnee[index] >= 2.5 and donnee[index] < 3.0):
        O6 = O6 + 1
        index  = index + 1
        
    for j in range(index, len(donnee)):
        O7 = O7 + 1
        index  = index + 1
    result.append(O1)
    result.append(O2)
    result.append(O3)
    result.append(O4)
    result.append(O5)
    result.append(O6)
    result.append(O7)
 
def faire_tri_dureeControle(donnee,result):
    donnee.sort()
    index = 0
    O2 = 0
    O3 = 0
    O4 = 0
    O5 = 0
    

    while(donnee[index] >= 0.25 and donnee[index] < 0.5):
        O2 = O2 + 1
        index  = index + 1

    while(donnee[index] >= 0.5 and donnee[index] < 0.75):
        O3 = O3 + 1
        index  = index + 1

    while(donnee[index] >= 0.75 and donnee[index] < 1.0):
        O4 = O4 + 1
        index  = index + 1

    for j in range(index, len(donnee)):
        O5 = O5 + 1
        index  = index + 1
    result.append(O2)
    result.append(O3)
    result.append(O4)
    result.append(O5)

def calculZ(arrObser, arrTheri):
    z = 0
    for k in range(len(arrTheri) - 1):
        temp = arrObser[k] - arrTheri[k]
        z = z + pow(temp, 2)/arrTheri[k]
    return z

def processus(donneeAccess):
    i = 0
    donneeExit = []
    donneeExit.append(donneeAccess[0])
    temp = len(donneeAccess) - 2
    while i <= temp:
       donneeExit.append(donneeAccess[i+1] - donneeAccess[i])
       i = i + 1
    return donneeExit

def processus_duree_controle(donneeAccess):
    i = 0
    donneeExit = []
    donneeExit.append(donneeAccess[0])
    temp = len(donneeAccess) - 2
    while i <= temp:
       donneeExit.append(donneeAccess[i+1] - donneeAccess[i])
       i = i + 1
    return donneeExit
    
def obtenirTheoriArriveTemp(arrTheri):
    lam = 0.5
    p1 = math.exp(-lam*0) - math.exp(-lam*0.5)
    p2 = math.exp(-lam*0.5) - math.exp(-lam*1.0)
    p3 = math.exp(-lam*1.0) - math.exp(-lam*1.5)
    p4 = math.exp(-lam*1.5) - math.exp(-lam*2.0)
    p5 = math.exp(-lam*2.0) - math.exp(-lam*2.5)
    p6 = math.exp(-lam*2.5) - math.exp(-lam*4.0)
    p7 = math.exp(-lam*4.0) - math.exp(-lam*160)

    n1 = p1*75
    n2 = p2*75
    n3 = p3*75
    n4 = p4*75
    n5 = p5*75
    n6 = p6*75
    n7 = p7*75

    arrTheri.append(n1)
    arrTheri.append(n2)
    arrTheri.append(n3)
    arrTheri.append(n4)
    arrTheri.append(n5)
    arrTheri.append(n6)
    arrTheri.append(n7)

def obtenirTheoriDureeControle(arrTheri):
#F(x) = x - a/b - a
    b = 1.083333
    a = 0.25
    p2 = (0.5-0.25)/(b - a)
    p3 = (0.75-0.5)/(b - a)
    p4 = (1.0-0.75)/(b - a)
    p5 = (b-1.0)/(b - a)
    
    n2 = p2*75
    n3 = p3*75
    n4 = p4*75
    n5 = p5*75

    arrTheri.append(n2)
    arrTheri.append(n3)
    arrTheri.append(n4)
    arrTheri.append(n5)


donneArriveControle = []
donneDureeControle = []


arrTheriArriveControle = []
arrTheriDureeControle = []

#effectif observe pour arrive temps
observeArriveTemp = []
#effectif theorique
theoriqueArriveTemp = []

#effectif observe pour duree controle
observeDureeControle = []
#effectif theorique pour duree controle
theoriqueDureeControle = []


lire_txt('DonneesControle.txt',donneArriveControle,donneDureeControle)
donneeApres = processus(donneArriveControle)
faire_tri_arriveTemp(donneeApres,observeArriveTemp)
obtenirTheoriArriveTemp(arrTheriArriveControle)

result_arrive_temp = calculZ(observeArriveTemp, arrTheriArriveControle)


obtenirTheoriDureeControle(theoriqueDureeControle)

faire_tri_dureeControle(donneDureeControle, observeDureeControle)
result_duree_controle = calculZ(observeDureeControle, theoriqueDureeControle)

print("le nombre de chaque group des effectifs theoriques d'arrive_temp:")
print(arrTheriArriveControle)
print("le nombre de chaque group des effectifs theoriques de duree controle:")
print(theoriqueDureeControle)
print("Résultat du test du chi carré du arrive de temps:"+str(result_arrive_temp))
print("Résultat du test du chi carré du duree controle:" + str(result_duree_controle))


