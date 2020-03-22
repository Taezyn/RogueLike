import numpy as np

"""
0 : sol
-1 : sortie
-2 : mur
-3 : depart
-4 : fin
-5 : cle
"""


class salle:
    def __init__(self, numsalle):
        self.__long = np.random.randint(5, 15)
        self.__haut = np.random.randint(5, 8)
        self.room = np.zeros((self.__haut, self.__long))
        self.nbsortie = 0
        # Creation murs
        for i in range(self.__long):
            self.room[0, i] = -2
            self.room[self.__haut - 1, i] = -2
        for i in range(self.__haut):
            self.room[i, 0] = -2
            self.room[i, self.__long - 1] = -2
        # Creation sorties
        pos_sortie = [[False, False, True, True], [True, False, True, True], [True, False, False, True], [False, True, True, True], [True, True, True, True], [True, True, False, True], [False, True, True, False], [True, True, True, False], [True, True, False, False]]
        if pos_sortie[numsalle][0]:
            coord_sortie = (np.random.randint(1, self.__haut - 1), 0)
            self.room[coord_sortie] = -1
            self.nbsortie += 1
        if pos_sortie[numsalle][1]:
            coord_sortie = (0, np.random.randint(1, self.__long - 1))
            self.room[coord_sortie] = -1
            self.nbsortie += 1
        if pos_sortie[numsalle][2]:
            coord_sortie = (np.random.randint(1, self.__haut - 1), self.__long - 1)
            self.room[coord_sortie] = -1
            self.nbsortie += 1
        if pos_sortie[numsalle][3]:
            coord_sortie = (self.__haut - 1, np.random.randint(1, self.__long - 1))
            self.room[coord_sortie] = -1
            self.nbsortie += 1

    @property
    def long(self):
        return self.__long

    @property
    def haut(self):
        return self.__haut

class niveau:
    def __init__(self):
        self.liste_niveaux = []
        self.dep = np.random.randint(0, 9)
        self.fin = np.random.randint(0, 9)
        self.cle = np.random.randint(0, 9)
        while self.dep == self.fin:
            self.fin = np.random.randint(0, 9)
        while self.cle == self.fin or self.cle == self.dep:
            self.cle = np.random.randint(0, 9)
        for i in range(9):
            self.liste_niveaux.append(salle(i))
        # Creation du depart
        x_dep = np.random.randint(1, self.liste_niveaux[self.dep].long - 1)
        y_dep = np.random.randint(1, self.liste_niveaux[self.dep].haut - 1)
        self.liste_niveaux[self.dep].room[y_dep, x_dep] = -3
        self.coorddep = (self.dep, x_dep, y_dep)
        # Creation de la fin
        x_fin = np.random.randint(1, self.liste_niveaux[self.fin].long - 1)
        y_fin = np.random.randint(1, self.liste_niveaux[self.fin].haut - 1)
        self.liste_niveaux[self.fin].room[y_fin, x_fin] = -4
        # Creation de la cle
        x_cle = np.random.randint(1, self.liste_niveaux[self.cle].long - 1)
        y_cle = np.random.randint(1, self.liste_niveaux[self.cle].haut - 1)
        self.liste_niveaux[self.cle].room[y_cle, x_cle] = -5
        # Supprime deux entree-sortie
        # Supprime un lien avec la piece du centre
        for i in range(np.random.randint(2,4)):
            suppr_lien = np.random.randint(0, 4)
            if suppr_lien == 0:
                for i in range(self.liste_niveaux[4].room.shape[0]):
                    self.liste_niveaux[4].room[i, 0] = -2
                self.liste_niveaux[4].nbsortie -= 1
                for i in range(self.liste_niveaux[3].room.shape[0]):
                    self.liste_niveaux[3].room[i, self.liste_niveaux[3].long - 1] = -2
                self.liste_niveaux[3].nbsortie -= 1
            elif suppr_lien == 1:
                for i in range(self.liste_niveaux[4].room.shape[1]):
                    self.liste_niveaux[4].room[0, i] = -2
                self.liste_niveaux[4].nbsortie -= 1
                for i in range(self.liste_niveaux[1].room.shape[1]):
                    self.liste_niveaux[1].room[self.liste_niveaux[1].haut - 1, i] = -2
                self.liste_niveaux[1].nbsortie -= 1
            elif suppr_lien == 2:
                for i in range(self.liste_niveaux[4].room.shape[0]):
                    self.liste_niveaux[4].room[i, self.liste_niveaux[4].long - 1] = -2
                self.liste_niveaux[4].nbsortie -= 1
                for i in range(self.liste_niveaux[5].room.shape[0]):
                    self.liste_niveaux[5].room[i, 0] = -2
                self.liste_niveaux[5].nbsortie -= 1
            elif suppr_lien == 3:
                for i in range(self.liste_niveaux[4].room.shape[1]):
                    self.liste_niveaux[4].room[self.liste_niveaux[4].haut - 1, i] = -2
                self.liste_niveaux[4].nbsortie -= 1
                for i in range(self.liste_niveaux[7].room.shape[1]):
                    self.liste_niveaux[7].room[0, i] = -2
                self.liste_niveaux[7].nbsortie -= 1
        # Puis supprime un second lien mais pas avec le centre
        suppr_lien = np.random.randint(0, 4)
        suppr_cote = np.random.randint(0, 2)
        if suppr_lien == 0:
            if suppr_cote == 0:
                for i in range(self.liste_niveaux[0].room.shape[0]):
                    self.liste_niveaux[0].room[i, self.liste_niveaux[0].long - 1] = -2
                for i in range(self.liste_niveaux[1].room.shape[0]):
                    self.liste_niveaux[1].room[i, 0] = -2
                self.liste_niveaux[0].nbsortie -= 1
                self.liste_niveaux[1].nbsortie -= 1
            elif suppr_cote == 1:
                for i in range(self.liste_niveaux[0].room.shape[1]):
                    self.liste_niveaux[0].room[self.liste_niveaux[0].haut - 1, i] = -2
                for i in range(self.liste_niveaux[3].room.shape[1]):
                    self.liste_niveaux[3].room[0, i] = -2
                self.liste_niveaux[0].nbsortie -= 1
                self.liste_niveaux[3].nbsortie -= 1
        elif suppr_lien == 1:
            if suppr_cote == 0:
                for i in range(self.liste_niveaux[2].room.shape[0]):
                    self.liste_niveaux[2].room[i, 0] = -2
                for i in range(self.liste_niveaux[1].room.shape[0]):
                    self.liste_niveaux[1].room[i, self.liste_niveaux[1].long - 1] = -2
                self.liste_niveaux[2].nbsortie -= 1
                self.liste_niveaux[1].nbsortie -= 1
            elif suppr_cote == 1:
                for i in range(self.liste_niveaux[2].room.shape[1]):
                    self.liste_niveaux[2].room[self.liste_niveaux[2].haut - 1, i] = -2
                for i in range(self.liste_niveaux[5].room.shape[1]):
                    self.liste_niveaux[5].room[0, i] = -2
                self.liste_niveaux[2].nbsortie -= 1
                self.liste_niveaux[3].nbsortie -= 1
        elif suppr_lien == 2:
            if suppr_cote == 0:
                for i in range(self.liste_niveaux[6].room.shape[0]):
                    self.liste_niveaux[6].room[i, self.liste_niveaux[6].long - 1] = -2
                for i in range(self.liste_niveaux[7].room.shape[0]):
                    self.liste_niveaux[7].room[i, 0] = -2
                self.liste_niveaux[6].nbsortie -= 1
                self.liste_niveaux[7].nbsortie -= 1
            elif suppr_cote == 1:
                for i in range(self.liste_niveaux[6].room.shape[1]):
                    self.liste_niveaux[6].room[0, i] = -2
                for i in range(self.liste_niveaux[3].room.shape[1]):
                    self.liste_niveaux[3].room[self.liste_niveaux[3].haut - 1, i] = -2
                self.liste_niveaux[6].nbsortie -= 1
                self.liste_niveaux[3].nbsortie -= 1
        elif suppr_lien == 3:
            if suppr_cote == 0:
                for i in range(self.liste_niveaux[8].room.shape[0]):
                    self.liste_niveaux[8].room[i, 0] = -2
                for i in range(self.liste_niveaux[7].room.shape[0]):
                    self.liste_niveaux[7].room[i, self.liste_niveaux[7].long - 1] = -2
                self.liste_niveaux[8].nbsortie -= 1
                self.liste_niveaux[7].nbsortie -= 1
            elif suppr_cote == 1:
                for i in range(self.liste_niveaux[8].room.shape[1]):
                    self.liste_niveaux[8].room[0, i] = -2
                for i in range(self.liste_niveaux[5].room.shape[1]):
                    self.liste_niveaux[5].room[self.liste_niveaux[5].haut - 1, i] = -2
                self.liste_niveaux[8].nbsortie -= 1
                self.liste_niveaux[5].nbsortie -= 1

    def __str__(self):
        for i, lvl in enumerate(self.liste_niveaux):
            print(i)
            print(lvl.room)

class perso:
    def __init__(self, lvl):
        self.xp = 0
        self.maxxp = 100
        self.lvl = 1
        self.sante = 100
        self.current_room = lvl.coorddep[0]
        self.posx = lvl.coorddep[1]
        self.posy = lvl.coorddep[2]






if __name__ == "__main__":
    N = niveau()
    P = perso(N)
