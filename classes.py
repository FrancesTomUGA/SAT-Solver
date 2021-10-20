from random import random, choice
import subprocess


class Litteral:
    """
    Littéral de la forme : (int i, int j, bool n)
    (i,j) sont les coordonnées de la case corresondant à la variable logique
    n est vrai pour avoir la négation de la variable
    """

    def __init__(self, i, j, n=False):
        self.couple = (i, j)
        self.negation = n

    def neg(self):
        i, j = self.couple
        n = not self.negation
        return Litteral(i, j, n)

    def __repr__(self):
        s = ""
        if self.negation:
            s = "-"
        return s + str(self.couple)


class Fnc:
    """
    Fnc de la forme : liste (conjonction) de clauses. Une clause est une liste (disjonction) de littéraux.
    méthodes : append, traduction
    """

    # faire une methode pour simplifier la fnc ? enlever les doublons etc.

    def __init__(self):
        self.clauses = []
        self.nb_clauses = 0

    def append(self, c):
        self.clauses.append(c)
        self.nb_clauses += 1

    def traduction(self, dico):
        # traduit en instuctions lisibles pour le solveur
        file = open("light_up.cnf", "w")
        nb_var = len(dico)
        nb_clause = self.nb_clauses
        en_tete = f"p cnf {nb_var} {nb_clause}\n"
        file.write(en_tete)
        for c in self.clauses:
            c_dimacs = ""
            for litt in c:
                coord = litt.couple
                n = dico[str(coord)]
                if litt.negation:
                    c_dimacs += '-'
                c_dimacs += f"{n} "
            c_dimacs += '0\n'
            file.write(c_dimacs)
        file.close()

    def execution_minisat(self, dico):
        self.traduction(dico)
        subprocess.run(["minisat", "light_up.cnf", "resultat.out"])
        file = open("resultat.out", "r")
        sat = file.readline()
        if sat == "SAT\n":
            print("\nCe plateau possède au moins une solution.\n")
            res = file.readline()
            liste_car = res.split(' ')      # on récupère les éléments 1 par 1
            liste_car.pop()        # on supprime le dernier caractère '0\n'
            liste_cases = []
            for elem in liste_car:
                liste_cases.append(int(elem))
            return liste_cases
        else:
            print("\nCe plateau n'a pas de solution.\n")
            return []

    def __repr__(self):
        for c in self.clauses:
            for m in c:
                print(m, end="")
                print(" + ", end="")
            print("\b\b ")
        return ""


class Plateau:
    """
    Plateau de la forme : tableau d'entiers à 2 dimensions.
    entiers :
    -1 Case libre
    0-4 Case noire avec un chiffre
    5 Case noire
    méthodes : randomize, coherent, regle_noire, regle_lumiere, regle_conflit
    """

    cases = [-1, 4, 3, 2, 1, 0, 5]
    casesRdm = [4, 4, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]

    def __init__(self, p, n, m=0):
        if m < 1:
            m = n
        self.dim = (n, m)
        self.prob = p
        self.tab = [[-1 for _ in range(m)] for _ in range(n)]

    def __getitem__(self, item):
        return self.tab[item]

    def __repr__(self):
        s = "[\n"
        for i in range(self.dim[0]):
            s += str(self[i])
            s += "\n"
        return s[:-1] + "\n]"

    def dico_cases(self): # renvoie deux dictionnaires qui associent coordonnées des cases libres à leur numéro et vice-versa
        dico_coord = {}
        dico_num = {}
        n = 0
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                if self.tab[i][j] == -1:
                    n += 1
                    coord = (i, j)
                    dico_coord[str(coord)] = n
                    dico_num[str(n)] = coord
        return dico_coord, dico_num

    def clear(self):    # remet toutes les cases du plateau à -1 (libre)
        n, m = self.dim
        for i in range(n):
            for j in range(m):
                self[i][j] = -1

    def randomize(self):
        self.clear()
        # nombre de cases non libres à placer
        n = round(int(self.dim[0] * self.dim[1] * self.prob))
        while n != 0:
            i = int(random() * self.dim[0])
            j = int(random() * self.dim[1])
            if self[i][j] == -1:
                n -= 1
                # on place une case non libre :
                if (i, j) in [(0, 0), (self.dim[0] - 1, self.dim[1] - 1), (0, self.dim[1] - 1), (self.dim[0] - 1, 0)]:
                    # 2 1 0 ou 5
                    self[i][j] = choice(Plateau.casesRdm[4:])
                elif i in [0, self.dim[0] - 1] or j in [0, self.dim[1] - 1]:
                        # 3 2 1 0 ou 5
                    self[i][j] = choice(Plateau.casesRdm[2:])
                else:
                        # 4 3 2 1 0 5
                    self[i][j] = choice(Plateau.casesRdm)

    def voisins(self, i, j):    # retourne les voisins libres immédiats d'une case de coordonées i,j
        v = []
        # ajout des cases voisines
        if i - 1 >= 0 and self.tab[i-1][j] == -1:  # voisin haut
            v.append((i - 1, j))
        if i + 1 < self.dim[0] and self.tab[i+1][j] == -1:     # voisin bas
            v.append((i + 1, j))
        if j - 1 >= 0 and self.tab[i][j-1] == -1:  # voisin gauche
            v.append((i, j - 1))
        if j + 1 < self.dim[1] and self.tab[i][j+1] == -1:     # voisin droit
            v.append((i, j + 1))
        return v

    def entourage(self, i, j):  #retourne toutes les cases dans la sous-ligne et sous-colonne qui passent par la case i,j
        e = []
        c = 0   # compteur (chaque case fait partie d'une sous-ligne et d'une sous-colonne du plateau uniquement, donc max 2)
        coord = (i, j)
        subparts = self.sous_parties()
        k = 0
        while k < len(subparts) and c < 2:
            if coord in subparts[k]:
                c = c + 1
                for elem in subparts[k]:
                    e.append(elem)
            k += 1
        liste = list(set(e))    # enlève les doublons
        return liste

    def coherent(self):
        # vérifie les conditions entre cases mur numéroté et nb de voisins
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                nb = self.tab[i][j]
                # case noire numéroté :
                if (nb in [1, 2, 3, 4] and nb > len(self.voisins(i, j))):
                    return False
        return True

    def sous_parties(self):
        subparts = []
        # traitement des sous-lignes
        subline = []
        for l in range(self.dim[0]):
            for c in range(self.dim[1]):
                if self.tab[l][c] == -1:
                    subline.append((l, c))
                if (self.tab[l][c] in (0,1,2,3,4,5) or c == self.dim[1] - 1):
                    if len(subline) > 1:
                        # on ajoute la sous-ligne si elle a au moins 2 éléments et
                        # si on tombe sur une case mur, ou si on arrive à la fin de la ligne
                        subparts.append(subline)
                    subline = []
        # traitement des sous-colonnes
        subcolumn = []
        for c in range(self.dim[1]):
            for l in range(self.dim[0]):
                if self.tab[l][c] == -1:
                    subcolumn.append((l, c))
                if (self.tab[l][c] in (0,1,2,3,4,5) or l == self.dim[0] - 1):
                    if len(subcolumn) > 1:
                        # on ajoute la sous-colonne si elle n'est pas vide et
                        # si on tombe sur une case non vide, ou si on arrive à la fin de la colonne
                        subparts.append(subcolumn)
                    subcolumn = []
        return subparts

    def case0(self, case, fnc):
        i, j = case
        for a, b in self.voisins(i, j):
            n = (Litteral(a, b, True))
            fnc.append([n])

    def case1(self, case, fnc):
        v = []
        i, j = case
        for a, b in self.voisins(i, j):
            v.append(Litteral(a, b))
        fnc.append(v)
        if len(v) in [2, 3, 4]:
            for l1 in range(0, len(v) - 1):
                for l2 in range(l1+1, len(v)):
                    n = list(map(Litteral.neg, [v[l1], v[l2]]))
                    fnc.append(n)

    def case2(self, case, fnc):
        v = []
        i, j = case
        for a, b in self.voisins(i, j):
            v.append(Litteral(a, b))
        if len(v) == 2:
            for l in v:
                fnc.append([l])
        elif len(v) == 3:
            for l1 in range(0, len(v) - 1):
                for l2 in range(l1 + 1, len(v)):
                    fnc.append([v[l1], v[l2]])
            n = map(Litteral.neg, v)
            fnc.append(n)
        elif len(v) == 4:
            for l1 in range(0, len(v) - 2):
                for l2 in range(l1 + 1, len(v) - 1):
                    for l3 in range(l1 + 2, len(v)):
                        clause = [v[l1], v[l2], v[l3]]
                        fnc.append(clause)
                        n = map(Litteral.neg, clause)
                        fnc.append(n)

    def case3(self, case, fnc):
        v = []
        i, j = case
        for a, b in self.voisins(i, j):
            v.append(Litteral(a, b))
        if len(v) == 3:
            for l in v:
                fnc.append([l])
        elif len(v) == 4:
            for l1 in range(0, len(v) - 1):
                for l2 in range(l1 + 1, len(v)):
                    fnc.append([v[l1], v[l2]])
            n = map(Litteral.neg, v)
            fnc.append(n)

    def case4(self, case, fnc):
        i, j = case
        for a, b in self.voisins(i, j):
            fnc.append([Litteral(a, b)])

    def regle_noire(self, fnc):
        """
        parcours le plateau et ajoute dans la fnc f des clauses pour chaques case noire numérotée

        une idée :
        récupérer L les coord des cases voisines et c le chiffre sur la case
        passer L et c dans une fct annexe regle1(L, c) qui renvoie les clauses
        ou directement regle1(L, c, f) qui ajoute les clauses à la fnc
        """
        n, m = self.dim
        for i in range(n):
            for j in range(m):
                if self[i][j] == 0:
                    self.case0((i, j), fnc)
                elif self[i][j] == 1:
                    self.case1((i, j), fnc)
                elif self[i][j] == 2:
                    self.case2((i, j), fnc)
                elif self[i][j] == 3:
                    self.case3((i, j), fnc)
                elif self[i][j] == 4:
                    self.case4((i, j), fnc)

    def regle_lumiere(self, fnc):
        """
        parcours les cases libre du plateau et ajoute dans fnc les regles qui assurent que chaque case soit éclairée
        idée : utiliser une fct annexe qui ...
        """
        for l in range(self.dim[0]):
            for c in range(self.dim[1]):
                if self.tab[l][c] == -1:
                    if len(self.voisins(l, c)) == 0:
                        litt = Litteral(l, c)
                        fnc.append([litt])
                    else:
                        e = self.entourage(l, c)
                        clause = []
                        for couple in e:
                            lit = Litteral(couple[0], couple[1])
                            clause.append(lit)
                        if len(clause) > 0:
                            fnc.append(clause)

    def regle_conflit(self, fnc):
        """
        pour chaque sous-ligne et chaque sous-colones ajoute la clause pour ne pas avoir plus d'une lampe dans la fnc
        """
        subparts = self.sous_parties()
        for s in subparts:
            for l1 in range(0, len(s) - 1):
                for l2 in range(l1+1, len(s)):
                    a = Litteral(s[l1][0], s[l1][1], True)
                    b = Litteral(s[l2][0], s[l2][1], True)
                    couple = (a, b)
                    fnc.append(couple)

    def case_isolee(self, fnc):
        for l in range(self.dim[0]):
            for c in range(self.dim[1]):
                if self.tab[l][c] == -1 and len(self.voisins(l, c)) == 0:
                    litt = Litteral(l, c)
                    fnc.append([litt])

    def placement_lampes(self, liste_cases, dico_num_coord):
        for c in liste_cases:
            num = int(c)
            if num > 0:
                i, j = dico_num_coord[str(num)]
                ent = self.entourage(i, j)
                self.tab[i][j] = 6
                for case in ent:
                    if self.tab[case[0]][case[1]] == -1:
                        self.tab[case[0]][case[1]] = 7
