#Game Of Life - 4 Juin 2020
#Code par Matthieu Gourdon et Lucas Wybrecht

##  -----Règles du jeu-----

#   *Dans ce Game of Life, les limites de la grille sont des murs

#   *grille de 15x15

#   *The universe of the Game of Life is an inendite two-dimensional orthogonal grid of square cells,
#    each of which is inone of two possible states, alive or dead.

#   *Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonallyadjacent.
#
#   *At each step in time, the following transitions occur :
# -Any live cell with fewer than two live neighbours dies, as if caused by under-population.
# -Any live cell with two or three live neighbours lives on to the next generation.
# -Any live cell with more than three live neighbours dies, as if by overcrowding.
# -Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
#
#   *The initial pattern constitutes the seed of the system.

#   *The first generation is created by applying the above rules simultaneously to every cell in the seed-births and
#    deathsoccur simultaneously, and the discrete moment at which this happens is sometimes called a step
#    (in other words, each generation is a pure function of the preceding one).

#   *The rules continue to be applied repeatedly to create further generations.

## Code :
##Bibliotheques :

import multiprocessing as mp
from multiprocessing import Process
import time, sys
lock = mp.Lock()  #Pour le mutex


def clear_ecran():
    """Clear l'écran"""
    print("\x1B[2J\x1B[;H", end=' ')


def move_to(lig, col):
    """Bouge le curseur à la ligne et à la colonne indiquée"""
    print("\033[" + str(lig) + ";" + str(col) + "f", end='')


def check_etat_cell(info_cell):
    """Renvoie l'état d'une case -- info_cell = [ligne_cell, colonne_cell, etat_cell]"""
    return info_cell[2]


def une_case(case_Index, mutex, tab, tab2, end):
    while end.value == 0:
        mutex.acquire()
        if not check_environnement(case_Index, tab):
            tab2[case_Index] = 0
        else:
            tab2[case_Index] = 1
        mutex.release()
        time.sleep(1)
    sys.exit(0)


def choice_start():
    choice = 0
    while choice not in [1, 2, 3, 4, 5, 6, 7]:
        choice = int(
            input(
                'Patern de départ ?\n 1: triple cellules vivantes\n 2: quintuple cellules vivantes\n 3: Planeur \n 4: Lightweight Spaceship\n 5: Small Exploder\n 6: Tumbler\n 7: Tests\n Réponse : '
            ))
    return choice


def Grille(mutex, tab, tab2, end):
    time.sleep(0.5)
    step = 0
    while end.value == 0:
        clear_ecran()
        mutex.acquire()
        vie_case = 0
        evolution = 0
        for case_Index in range(len(tab)):
            ma_ligne = 1 + case_Index // 15
            ma_colonne = case_Index - 15 * (ma_ligne - 1) + 1
            move_to(ma_ligne, ma_colonne)
            if tab2[case_Index] == 0:
                print('-')
            elif tab2[case_Index] == 1:
                print('X')
                vie_case += 1
            if tab2[case_Index] != tab[case_Index]:
                evolution += 1
            tab[case_Index] = tab2[case_Index]
        move_to(17, 5)
        step += 1
        print('Étape : ', step)
        move_to(18, 5)
        print('Nombre de cellules vivantes:', vie_case)
        move_to(20, 10)
        print('Commande pour stoper la simulation : Ctrl+C')
        if vie_case == 0 or evolution == 0:
            end.value = 1
        mutex.release()
        time.sleep(1)
    move_to(18, 5)
    print("Fin de simulation, plus d'évolution possible.\n")
    sys.exit(0)


def check_environnement(case, tab):
    case_Vivante_Voisine = 0
    if case == 0:
        if tab[case + 1] == 1:
            case_Vivante_Voisine += 1
        if tab[case + 15] == 1:
            case_Vivante_Voisine += 1
        if tab[case + 16] == 1:
            case_Vivante_Voisine += 1
        if tab[case] == 1:
            if case_Vivante_Voisine in [2, 3]:
                return True
            else:
                return False
        else:
            if case_Vivante_Voisine == 3:
                return True
            else:
                return False
    elif case == 14:
        if tab[case - 1] == 1:
            case_Vivante_Voisine += 1
        if tab[case + 15] == 1:
            case_Vivante_Voisine += 1
        if tab[case + 14] == 1:
            case_Vivante_Voisine += 1
        if tab[case] == 1:
            if case_Vivante_Voisine in [2, 3]:
                return True
            else:
                return False
        else:
            if case_Vivante_Voisine == 3:
                return True
            else:
                return False
    elif case == 210:
        if tab[case + 1] == 1:
            case_Vivante_Voisine += 1
        if tab[case - 15] == 1:
            case_Vivante_Voisine += 1
        if tab[case - 14] == 1:
            case_Vivante_Voisine += 1
        if tab[case] == 1:
            if case_Vivante_Voisine in [2, 3]:
                return True
            else:
                return False
        else:
            if case_Vivante_Voisine == 3:
                return True
            else:
                return False
    elif case == 224:
        if tab[case - 1] == 1:
            case_Vivante_Voisine += 1
        if tab[case - 15] == 1:
            case_Vivante_Voisine += 1
        if tab[case - 16] == 1:
            case_Vivante_Voisine += 1
        if tab[case] == 1:
            if case_Vivante_Voisine in [2, 3]:
                return True
            else:
                return False
        else:
            if case_Vivante_Voisine == 3:
                return True
            else:
                return False

    elif case < 15:
        for i in [case, case + 15]:
            for j in [i - 1, i, i + 1]:
                if tab[j] == 1 and j != case:
                    case_Vivante_Voisine += 1
        if tab[case] == 1:
            if case_Vivante_Voisine == 2 or case_Vivante_Voisine == 3:
                return True
            else:
                return False
        else:
            if case_Vivante_Voisine == 3:
                return True
            else:
                return False

    elif case % 15 == 0:
        for i in [case - 15, case, case + 15]:
            for j in [i, i + 1]:
                if tab[j] == 1 and j != case:
                    case_Vivante_Voisine += 1
        if tab[case] == 1:
            if case_Vivante_Voisine == 2 or case_Vivante_Voisine == 3:
                return True
            else:
                return False
        else:
            if case_Vivante_Voisine == 3:
                return True
            else:
                return False
    elif case >= 210:
        for i in [case, case - 15]:
            for j in [i - 1, i, i + 1]:
                if tab[j] == 1 and j != case:
                    case_Vivante_Voisine += 1
        if tab[case] == 1:
            if case_Vivante_Voisine == 2 or case_Vivante_Voisine == 3:
                return True
            else:
                return False
        else:
            if case_Vivante_Voisine == 3:
                return True
            else:
                return False
    elif (case + 1) % 15 == 0:
        for i in [case - 15, case, case + 15]:
            for j in [i - 1, i]:
                if tab[j] == 1 and j != case:
                    case_Vivante_Voisine += 1
        if tab[case] == 1:
            if case_Vivante_Voisine == 2 or case_Vivante_Voisine == 3:
                return True
            else:
                return False
        else:
            if case_Vivante_Voisine == 3:
                return True
            else:
                return False

    else:
        for i in [case - 15, case, case + 15]:
            for j in [i - 1, i, i + 1]:
                if tab[j] == 1 and j != case:
                    case_Vivante_Voisine += 1
        if tab[case] == 1:
            if case_Vivante_Voisine == 2 or case_Vivante_Voisine == 3:
                return True
            else:
                return False
        else:
            if case_Vivante_Voisine == 3:
                return True
            else:
                return False


def GameOfLife():
    clear_ecran()
    choice = choice_start()
    clear_ecran()
    end = mp.Value('i', 0)
    Nb_process = 225
    mes_process = [0 for i in range(Nb_process)]
    tab = mp.Array('i', range(Nb_process))
    tab2 = mp.Array('i', range(Nb_process))
    for i in range(Nb_process):
        tab[i] = 0
        tab2[i] = 0
        if choice == 1:
            if i in [19, 34, 49]:
                tab[i] = 1
        elif choice == 2:
            if i in [80, 81, 82, 83, 84]:
                tab[i] = 1
        elif choice == 3:
            if i in [2, 18, 31, 32, 33]:
                tab[i] = 1
        elif choice == 4:
            if i in [61, 62, 63, 64, 75, 79, 94, 105, 108]:
                tab[i] = 1
        elif choice == 5:
            if i in [112, 126, 127, 128, 141, 143, 157]:
                tab[i] = 1
        elif choice == 6:
            if i in [
                    65, 66, 68, 69, 80, 81, 83, 84, 96, 98, 109, 111, 113, 115,
                    124, 126, 128, 130, 139, 140, 144, 145
            ]:
                tab[i] = 1
        elif choice == 7:
            if i in [30, 29, 44, 45, 222, 221, 223, 217, 218, 203, 202]:
                tab[i] = 1
        ma_ligne = 1 + i // 15
        ma_colonne = i - 15 * (ma_ligne - 1) + 1
        move_to(ma_ligne, ma_colonne)
        if tab[i] == 1:
            print('X')
        else:
            print('-')
        mes_process[i] = Process(
            target=une_case, args=(i, lock, tab, tab2, end))
    move_to(18, 5)
    print("X:Vivant, -:Mort | Début de la partie dans 3 secondes.")
    time.sleep(3)
    for case_Index in range(len(tab)):
        tab2[case_Index] = tab[case_Index]
    grille = mp.Process(target=Grille, args=(lock, tab, tab2, end))
    grille.start()

    for i in range(Nb_process):
        mes_process[i].start()

    for i in range(Nb_process):
        mes_process[i].join()
    grille.join()


#---------------------------------------------------------------
##Main :

if __name__ == "__main__":
    GameOfLife()