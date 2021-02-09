# Juin 2019
# Cours hippique
# Version tr�s basique, sans mutex sur l'�cran, sans arbitre, sans annoncer le gagant, ... ...
# coding latin - 1
# Quelques codes d'�chappement (tous ne sont pas utilis�s)
CLEARSCR = "\x1B[2J\x1B[;H"  #  Clear SCReen
CLEAREOS = "\x1B[J"  #  Clear End Of Screen
CLEARELN = "\x1B[2K"  #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"  #  Clear Curseur UP
GOTOYX = "\x1B[%.2d;%.2dH"  #  ('H' ou 'f') : Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"  #  effacer apr�s la position du curseur
CRLF = "\r\n"  #  Retour � la ligne

# VT100 : Actions sur le curseur
CURSON = "\x1B[?25h"  #  Curseur visible
CURSOFF = "\x1B[?25l"  #  Curseur invisible

# VT100 : Actions sur les caract�res affichables
NORMAL = "\x1B[0m"  #  Normal
BOLD = "\x1B[1m"  #  Gras
UNDERLINE = "\x1B[4m"  #  Soulign�

import multiprocessing as mp
from multiprocessing import Process
import time, random, ctypes

lock = mp.Lock()  #Le mutex
timer = mp.Value(ctypes.c_bool, True)


def effacer_ecran():
    print(CLEARSCR, end='')


def erase_line_from_beg_to_curs():
    print("\033[1K", end='')


def curseur_invisible():
    print(CURSOFF, end='')


def curseur_visible():
    print(CURSON, end='')


def move_to(lig, col):
    print("\033[" + str(lig) + ";" + str(col) + "f", end='')


def en_couleur(Coul):
    print(Coul, end='')


def client(Pile): #processus client
    L = []
    while timer.value:  #boucle jusqu'à la fin de la durée de service
        p = -1
        for i in range(len(Pile) // 2):
            if Pile[2 * i + 1] == -1:  #Regarde les clients qui n'ont pas encore commandé
                L.append(i)
                p = i
                break
        if p != -1:  #génère une commande pour un client
            time.sleep(0.5)
            com = ord('A') + int(random.uniform(10, 15))
            Pile[2 * p + 1] = com


def serveur(num_serv, Pile, liste_serveur, com_en_traitmnt, liste_client,
            liste_commande, stop):  #processus serveurs
    client_com = 0
    while stop.value > 0 or timer.value:  #boucle jusqu'à ce qu'il n'y ai plus de commande
        st = False
        for i in range(len(Pile) // 2):
            if i in liste_client:  #teste si des clients sont dans la pile
                None
            else:
                if Pile[2 * i + 1] != -1:  #regarde s'il y a des commandes
                    liste_client[i] = i
                    for j in range(len(liste_serveur)):

                        if j == num_serv and liste_serveur[j] == -1:  #regarde s'il y a un serveur dispo pour la commande

                            liste_serveur[j] = 2 * i
                            client_com = 2 * i
                            liste_commande[num_serv] = (Pile[client_com + 1])
                            st = True  #Autorise le serveur a prendre en charge la commande
                            break
                    break
        if st == True: #prise en charge de la commande
            com_en_traitmnt[num_serv] = 1
            time.sleep(random.randint(3, 6))
            Pile[client_com + 1] = -1
            liste_serveur[num_serv] = -1
            com_en_traitmnt[num_serv] = 0
            liste_client[client_com // 2] = -1
            liste_commande[num_serv] = -1


def major_dHomme(Pile, com_en_traitmnt, liste_serveur, liste_commande,
                 liste_client, stop): #processus affichage
    while timer.value or stop.value > 0:
        L = []
        for i in range(len(Pile) // 2):
            if Pile[2 * i + 1] != -1:  #récupère les infos pile pour l'affichage des commandes en attentes
                L.append((Pile[2 * i], chr(Pile[2 * i + 1])))
        move_to(1, 150)
        erase_line_from_beg_to_curs()
        move_to(1, 1)
        print('Commande(s) en attente : ', L)
        move_to(2, 100)
        erase_line_from_beg_to_curs()
        move_to(2, 1)
        print('Nombre de commande(s) en attente : ', (len(L)))
        for i in range(5):
            move_to(3 + i, 100)
            erase_line_from_beg_to_curs()
            move_to(3 + i, 1)
            if com_en_traitmnt[i] == 1 and Pile[liste_serveur[i]] != -1:
                print('Statut serveur ' + str(i) + ' : ' +
                      "traite la commande : " + str(chr(liste_commande[i])) +
                      " du client : " + str(Pile[liste_serveur[i]]))
            else:
                print("Statut serveur " + str(i) + " : " + "en attente")
        stop.value -= stop.value
        stop.value += len(L)


def duree_du_service():  #teste securisé de durée de simu
    try:
        a = int(input("Choisissez un durée de service : "))
    except:
        print("ce n'est pas un entier")
        resto()
    return (a)


def resto():  #main
    duree = duree_du_service()
    effacer_ecran()
    curseur_invisible()
    stop = mp.Value('i', 1)
    mes_serv = [0, 1, 2, 3, 4]
    Pile = mp.Array(
        'i',
        [0, -1, 1, -1, 2, -1, 3, -1, 4, -1, 5, -1, 6, -1, 7, -1, 8, -1, 9, -1])
    liste_serveur = mp.Array('i', [-1, -1, -1, -1, -1])
    com_en_traitmnt = mp.Array('i', [0, 0, 0, 0, 0])
    liste_client = mp.Array('i', [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1])
    liste_commande = mp.Array('i', [-1, -1, -1, -1, -1])
    for i in range(5):
        mes_serv[i] = Process(
            target=serveur,
            args=(
                i,
                Pile,
                liste_serveur,
                com_en_traitmnt,
                liste_client,
                liste_commande,
                stop,
            ))
        mes_serv[i].start()

    maj_dhomme = Process(
        target=major_dHomme,
        args=(
            Pile,
            com_en_traitmnt,
            liste_serveur,
            liste_commande,
            liste_client,
            stop,
        ))
    maj_dhomme.start()
    clients = Process(target=client, args=(Pile, ))
    clients.start()

    time.sleep(duree)
    timer.value = False


if __name__ == "__main__":
    resto()