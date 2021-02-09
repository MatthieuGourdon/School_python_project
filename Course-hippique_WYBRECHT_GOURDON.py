
# Juin 2019
# Cours hippique
# Version tr�s basique, sans mutex sur l'�cran, sans arbitre, sans annoncer le gagant, ... ...
# coding latin - 1
# Quelques codes d'�chappement (tous ne sont pas utilis�s)
CLEARSCR="\x1B[2J\x1B[;H"          #  Clear SCReen
CLEAREOS = "\x1B[J"                #  Clear End Of Screen
CLEARELN = "\x1B[2K"               #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"               #  Clear Curseur UP
GOTOYX   = "\x1B[%.2d;%.2dH"       #  ('H' ou 'f') : Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"             #  effacer apr�s la position du curseur
CRLF  = "\r\n"                     #  Retour � la ligne

# VT100 : Actions sur le curseur
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

# VT100 : Actions sur les caract�res affichables
NORMAL = "\x1B[0m"                  #  Normal
BOLD = "\x1B[1m"                    #  Gras
UNDERLINE = "\x1B[4m"               #  Soulign�


# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m"                  #  Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m"                    #  Rouge
CL_GREEN="\033[22;32m"                  #  Vert
CL_BROWN = "\033[22;33m"                #  Brun
CL_BLUE="\033[22;34m"                   #  Bleu
CL_MAGENTA="\033[22;35m"                #  Magenta
CL_CYAN="\033[22;36m"                   #  Cyan
CL_GRAY="\033[22;37m"                   #  Gris

# "01" pour quoi ? (bold ?)
CL_DARKGRAY="\033[01;30m"               #  Gris fonc�
CL_LIGHTRED="\033[01;31m"               #  Rouge clair
CL_LIGHTGREEN="\033[01;32m"             #  Vert clair
CL_YELLOW="\033[01;33m"                 #  Jaune
CL_LIGHTBLU= "\033[01;34m"              #  Bleu clair
CL_LIGHTMAGENTA="\033[01;35m"           #  Magenta clair
CL_LIGHTCYAN="\033[01;36m"              #  Cyan clair
CL_WHITE="\033[01;37m"                  #  Blanc

#-------------------------------------------------------
# Juin 2019
# Cours hippique
# Version tr�s basique, sans mutex sur l'�cran, sans arbitre, sans annoncer le gagant, ... ...

# Quelques codes d'�chappement (tous ne sont pas utilis�s)
CLEARSCR="\x1B[2J\x1B[;H"          #  Clear SCReen
CLEAREOS = "\x1B[J"                #  Clear End Of Screen
CLEARELN = "\x1B[2K"               #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"               #  Clear Curseur UP
GOTOYX   = "\x1B[%.2d;%.2dH"       #  ('H' ou 'f') : Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"             #  effacer apr�s la position du curseur
CRLF  = "\r\n"                     #  Retour � la ligne

# VT100 : Actions sur le curseur
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

# VT100 : Actions sur les caract�res affichables
NORMAL = "\x1B[0m"                  #  Normal
BOLD = "\x1B[1m"                    #  Gras
UNDERLINE = "\x1B[4m"               #  Soulign�


# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m"                  #  Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m"                    #  Rouge
CL_GREEN="\033[22;32m"                  #  Vert
CL_BROWN = "\033[22;33m"                #  Brun
CL_BLUE="\033[22;34m"                   #  Bleu
CL_MAGENTA="\033[22;35m"                #  Magenta
CL_CYAN="\033[22;36m"                   #  Cyan
CL_GRAY="\033[22;37m"                   #  Gris

# "01" pour quoi ? (bold ?)
CL_DARKGRAY="\033[01;30m"               #  Gris fonc�
CL_LIGHTRED="\033[01;31m"               #  Rouge clair
CL_LIGHTGREEN="\033[01;32m"             #  Vert clair
CL_YELLOW="\033[01;33m"                 #  Jaune
CL_LIGHTBLU= "\033[01;34m"              #  Bleu clair
CL_LIGHTMAGENTA="\033[01;35m"           #  Magenta clair
CL_LIGHTCYAN="\033[01;36m"              #  Cyan clair
CL_WHITE="\033[01;37m"                  #  Blanc

#-------------------------------------------------------

import multiprocessing as mp
from multiprocessing import Process 
import os, time,math, random, sys, ctypes

lock = mp.Lock() #Le mutex

LONGEUR_COURSE = 100 # Tout le monde aura la m�me copie (donc no need to have a 'value')
keep_running=mp.Value(ctypes.c_bool, True)



# Une liste de couleurs � affecter al�atoirement aux chevaux
lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY,
             CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN,  CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]

def effacer_ecran() : print(CLEARSCR,end='')
def erase_line_from_beg_to_curs() : print("\033[1K",end='')
def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')
def move_to(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def en_couleur(Coul) : print(Coul,end='')
def en_rouge() : print(CL_RED,end='') # Un exemple !


# La tache d'un cheval
def un_cheval(ma_ligne : int,mutex,tab) : # ma_ligne commence � 0
    col=1
    while col < LONGEUR_COURSE and keep_running.value :
        mutex.acquire()
        move_to(ma_ligne+1,col)      # pour effacer toute ma ligne
        mutex.release()
        mutex.acquire()
        erase_line_from_beg_to_curs()
        mutex.release()
        mutex.acquire()
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        mutex.release()
        mutex.acquire()
        print('('+chr(ord('A')+ma_ligne)+'>')
        mutex.release()
        col+=1
        mutex.acquire()
        tab[ma_ligne]=col
        mutex.release()
        time.sleep(0.1 * random.randint(1,5))
        
def un_arbitre(tab,stop_arb,gagnants,ChevPar):
    while keep_running.value:
        valeur=tab[0]
        indice=0
        inc=0
        if 100 in tab and stop_arb.value==0:
            for i in range(len(tab)):
                if tab[i]==100:
                    gagnants[stop_arb.value]=i
                    stop_arb.value+=1
            for i in range(len(gagnants)):
                if gagnants[i]!=-1:
                    move_to(22+i,10)
                    print("le cheval gagnant est :"+chr(ord('A')+gagnants[i]))
                    en_couleur(CL_GREEN)
                move_to(22,45)
                if chr(ord('A')+gagnants[0])==ChevPar or chr(ord('A')+gagnants[1])==ChevPar:
                    print("Pari gagné !")
                else:
                    print("Pari perdu !")
            break
        if stop_arb.value==0:
            for val in tab:
                inc+=1
                if val>valeur:
                    valeur=val
                    indice=inc
            move_to(22,10)
            print("le cheval gagnant est :"+chr(ord('A')+indice-1))
            en_couleur(CL_GREEN)

def pari():
    Pari=str(input("Vous pariez sur quel cheval ?"))
    if Pari in "ABCDEFGHIJKLMNOPQRST": 
        return(pari)
    else:
        pari()

#------------------------------------------------
# La partie principale :
def course_hippique() :
    ChevPar=pari()
    Nb_process=20
    mes_process = [0 for i in range(Nb_process)]
    effacer_ecran()
    tab=mp.Array('i',range(Nb_process))
    gagnants=mp.Array('i',[0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
    stop_arb=mp.Value('i',0)
    curseur_invisible()
    for i in range(Nb_process):  # Lancer     Nb_process  processus
        mes_process[i] = Process(target=un_cheval, args= (i,lock,tab,))
        mes_process[i].start()
    move_to(Nb_process+10, 1)
    arbitre=mp.Process(target=un_arbitre, args=(tab,stop_arb,gagnants,ChevPar))
    arbitre.start()    
    print("tous lances")
    for i in range(Nb_process): mes_process[i].join()
    arbitre.join()
    move_to(24, 1)
    curseur_visible()
    print("Fini")
    

    
# La partie principale :
if __name__ == "__main__" :
    course_hippique()
    
