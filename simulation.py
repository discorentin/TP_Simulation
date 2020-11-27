from numpy.random import default_rng
from operator import itemgetter


class SimulationMaintenanceBus:
    DEBUT_SIMULATION = 'debut_simulation'
    FIN_SIMULATION = 'fin_simulation'
    MAJ_AIRES = 'maj_aires'
    SIMULATEUR = 'simulateur'
    ARRIVEE_BUS = 'arrivee_bus'
    ARRIVEE_FILE_C = 'arrivee_file_c'
    ACCES_CONTROLE = 'acces_controle'
    DEPART_CONTROLE = 'depart_controle'
    ARRIVEE_FILE_R = 'arrivee_file_r'
    ACCES_REPARATION = 'acces_reparation'
    DEPART_REPARATION = 'depart_reparation'


    def __init__(self, duree):
        self.date_simu = 0
        self.duree_simu = duree

        self.nb_bus = 0
        self.nb_bus_rep = 0

        self.aire_qc = 0
        self.aire_qr = 0
        self.aire_br = 0

        self.qc = 0
        self.qr = 0
        self.bc = 0
        self.br = 0

        self.echeancier = []

        self.rng = default_rng()

    def executer_evenement(self, evt):
        switcher = {
            self.DEBUT_SIMULATION: self.debut_simulation,
            self.FIN_SIMULATION: self.fin_simulation,
            self.MAJ_AIRES: self.maj_aires,
            self.SIMULATEUR: self.simulateur,
            self.ARRIVEE_BUS: self.arrivee_bus,
            self.ARRIVEE_FILE_C: self.arrivee_file_c,
            self.ACCES_CONTROLE: self.acces_controle,
            self.DEPART_CONTROLE: self.depart_controle,
            self.ARRIVEE_FILE_R: self.arrivee_file_r,
            self.ACCES_REPARATION: self.acces_reparation,
            self.DEPART_REPARATION: self.depart_reparation
        }

        func = switcher.get(evt, lambda: "Evenement invalide")
        func()

    def maj_aires(self, d1, d2):
        self.aire_qc += (d2 - d1) * self.qc
        self.aire_qr += (d2 - d1) * self.qr
        self.aire_br += (d2 - d1) * self.br

    def simulateur(self):
        self.echeancier.append((self.DEBUT_SIMULATION, self.date_simu))

        while self.echeancier:
            self.echeancier = sorted(self.echeancier, key=itemgetter(1))
            # print(self.echeancier)

            evt, date = self.echeancier.pop(0)
            self.maj_aires(self.date_simu, date)
            self.date_simu = date
            self.executer_evenement(evt)

    def debut_simulation(self):
        self.echeancier.append((self.ARRIVEE_BUS, self.date_simu + self.rng.exponential(2)))
        self.echeancier.append((self.FIN_SIMULATION, self.duree_simu))

    def fin_simulation(self):
        self.echeancier.clear()
        temps_attente_moyen_avant_controle = self.aire_qc / self.nb_bus
        fc = self.aire_qc / self.duree_simu
        temps_attente_moyen_avant_reparation = self.aire_qr / self.nb_bus_rep
        fr = self.aire_qr / self.duree_simu
        taux_utilisation_centre_reparation = self.aire_br / (2 * self.duree_simu)

        #print("Temps d'attente moyen avant contrôle : " + str(temps_attente_moyen_avant_controle))
        #print("Temps d'attente moyen avant réparation : " + str(temps_attente_moyen_avant_reparation))
        #print("Taux d'utilisation du centre de réparation : " + str(taux_utilisation_centre_reparation) + "\n")
        return [temps_attente_moyen_avant_controle,temps_attente_moyen_avant_reparation,fc,fr,taux_utilisation_centre_reparation]

    def arrivee_bus(self):
        self.echeancier.append((self.ARRIVEE_BUS, self.date_simu + self.rng.exponential(2)))
        self.nb_bus += 1
        self.echeancier.append((self.ARRIVEE_FILE_C, self.date_simu))

    def arrivee_file_c(self):
        self.qc += 1
        if self.bc == 0:
            self.echeancier.append((self.ACCES_CONTROLE, self.date_simu))

    def acces_controle(self):
        self.qc -= 1
        self.bc = 1
        self.echeancier.append((self.DEPART_CONTROLE, self.date_simu + self.rng.uniform(0.25, 13 / 12)))

    def depart_controle(self):
        self.bc = 0
        if self.qc > 0:
            self.echeancier.append((self.ACCES_CONTROLE, self.date_simu))
        if self.rng.random() < 0.3:
            self.echeancier.append((self.ARRIVEE_FILE_R, self.date_simu))

    def arrivee_file_r(self):
        self.qr += 1
        self.nb_bus_rep += 1
        if self.br < 2:
            self.echeancier.append((self.ACCES_REPARATION, self.date_simu))

    def acces_reparation(self):
        self.qr -= 1
        self.br += 1
        self.echeancier.append((self.DEPART_REPARATION, self.date_simu + self.rng.uniform(2.1, 4.5)))

    def depart_reparation(self):
        self.br -= 1
        if self.qr > 0:
            self.echeancier.append((self.ACCES_REPARATION, self.date_simu))


def calcul_res(duree, nb_réplications):
    tc = 0
    tr = 0
    fc = 0
    fr = 0
    taux = 0

    for i in range(0,nb_réplications):
        simulation = SimulationMaintenanceBus(duree)
        simulation.simulateur()
        res = simulation.fin_simulation()
        tc = tc + res[0]
        tr = tr + res[1]
        fc = fc + res[2]
        fr = fr + res[3]
        taux = taux + res[4]
    print("------------------------" + str(duree)  + "heures------------------------")
    print("Temps d'attente moyen avant contrôle : " + str(tc/nb_réplications))
    print("Temps d'attente moyen avant réparation : " + str(tr/nb_réplications))
    print("Taille Moyenne de file contrôle : " + str(fc/nb_réplications))
    print("Taille Moyenne de file réparation : " + str(fr/nb_réplications))
    print("Taux d'utilisation du centre de réparation : " + str(taux/nb_réplications))


calcul_res(40,500)
calcul_res(80,500)
calcul_res(160,500)
calcul_res(240,500)
