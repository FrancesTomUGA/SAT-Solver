import sys
import tests
from fenetre import affichage_graphique
from classes import Litteral, Fnc, Plateau
from tkinter import *


# --------------TEST FNC REGLES----------------
"""
nb paramètres :
- 5 : nom_script, proba, nb lignes, nb colonnes, step-by-step (1 si on veut afficher tous les plateaux testés, 0 sinon)
- 4 : nom_script, proba, dimension (plateau carré), step-by-step (1 si on veut afficher tous les plateaux testés, 0 sinon)
- 3 : nom_script, entier (numéro du test préétabli), debugg (1 si on veut afficher la construction de la fnc pas à pas, 0 sinon)
"""

if len(sys.argv) == 3:
    n = int(sys.argv[1])
    if n == 1:
        P = tests.test1()
    elif n == 2:
        P = tests.test2()
    elif n == 3:
        P = tests.test3()
    elif n == 4:
        P = tests.test4()
    elif n == 5:
        P = tests.test5()
    elif n == 6:
        P = tests.test6()
    else:
        print("Test non répertorié\n")
        quit()
    debugg = int(sys.argv[2])
    if debugg:
        dico_coord, dico_num = P.dico_cases()
        print("Plateau :\n")
        print(P)
        fnc_conflit = Fnc()  # application règle conflit    (max 1 lampe par sous-partie de plateau)
        fnc_lumiere = Fnc()  # application règle lumière     (toutes les cases sont éclairées)
        fnc_noire = Fnc()  # application règle noire   (mur numérotés)
        fnc_isolee = Fnc()  # cases isolées (doivent contenir une lampe)
        fnc = Fnc()

        P.regle_noire(fnc_noire)
        P.regle_noire(fnc)
        P.regle_conflit(fnc_conflit)
        P.regle_conflit(fnc)
        P.regle_lumiere(fnc_lumiere)
        P.regle_lumiere(fnc)

        print("\nFNC_noire coordonées : \n", fnc_noire)
        print("\nFNC_conflit coordonées : \n", fnc_conflit)
        print("\nFNC_lumière coordonées : \n", fnc_lumiere)

        liste_cases = fnc.execution_minisat(dico_coord)
        if len(liste_cases) != 0:
            affichage_graphique(P, "plateau_vide.ps")
            P.placement_lampes(liste_cases, dico_num)
            affichage_graphique(P, "plateau_lampe.ps")
    else:
        fnc = Fnc()  # initialise la fnc vide
        print("Plateau :\n")
        print(P)
        dico_coord, dico_num = P.dico_cases()
        P.regle_noire(fnc)
        P.regle_conflit(fnc)
        P.regle_lumiere(fnc)
        P.case_isolee(fnc)

        liste_cases = fnc.execution_minisat(dico_coord)
        if len(liste_cases) != 0:
            affichage_graphique(P, "plateau_vide.ps")
            P.placement_lampes(liste_cases, dico_num)
            affichage_graphique(P, "plateau_lampe.ps")

elif len(sys.argv) in [4, 5]:
    if len(sys.argv) == 4:
        prob = float(sys.argv[1])
        dim = int(sys.argv[2])
        sbs = int(sys.argv[3])
        P = Plateau(prob, dim)
    else:
        prob = float(sys.argv[1])
        l = int(sys.argv[2])
        c = int(sys.argv[3])
        sbs = int(sys.argv[4])
        P = Plateau(prob, l, c)
    a = 1
    nb_test = 1
    while a and nb_test <= 100:
        print("\n\n TEST ", nb_test, " :\n\n")
        fnc = Fnc()     # initialise la fnc vide
        P.randomize()
        while not P.coherent():
            P.randomize()  # change les cases jusqu'à avoir une cohérent
        print("Plateau :\n")
        print(P)
        if sbs:
            affichage_graphique(P, "plateau_vide.ps")
        dico_coord, dico_num = P.dico_cases()

        P.regle_noire(fnc)
        P.regle_conflit(fnc)
        P.regle_lumiere(fnc)
        P.case_isolee(fnc)

        liste_cases = fnc.execution_minisat(dico_coord)
        if len(liste_cases) != 0:
            if not sbs:
                affichage_graphique(P, "plateau_vide.ps")
            P.placement_lampes(liste_cases, dico_num)
            affichage_graphique(P, "plateau_lampe.ps")
            print("Plateau trouvé en ", nb_test, " tests.\n")
            a = 0
            input("\nAppuyez sur Entrée pour continuer\n")
        if sbs:
            input("\nAppuyez sur Entrée pour continuer\n")
        nb_test += 1
else:
    print("\nMauvais nombre d'arguments\n")
    print("nb parametres :\n"
          "     - 5 : nom_script, proba, nb lignes, nb colonnes, step-by-step (1 si on veut afficher tous les plateaux testes, 0 sinon)\n"
          "     - 4 : nom_script, proba, dimension (plateau carre), step-by-step (1 si on veut afficher tous les plateaux testes, 0 sinon)\n"
          "     - 3 : nom_script, entier (numéro du test preetabli), debugg (1 si on veut afficher la construction de la fnc pas à pas, 0 sinon)\n\n")
