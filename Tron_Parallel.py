import tkinter as tk
import random
import time
import copy
import numpy as np


Data = [   [1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,1,0,0,0,0,0,0,0,0,0,0,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1]  ]

GInit  = np.array(Data,dtype=np.int32)
GInit  = np.flip(GInit,0).transpose()

class Game:
    def __init__(self, Grille, PlayerX, PlayerY, Score=0):
        self.PlayerX = PlayerX
        self.PlayerY = PlayerY
        self.Score   = Score
        self.Grille  = Grille

    def copy(self):
        return copy.deepcopy(self)


GameInit = Game(GInit,3,5)

#############################################################
#
#  affichage en mode texte


def AffGrilles(G,X,Y):
    nbG, larg , haut = G.shape
    for y in range(haut-1,-1,-1) :
        for i in range(nbG) :
            for x in range(larg) :
               g = G[i]
               c = ' '
               if G[i,x,y] == 1 : c = 'M'  # mur
               if G[i,x,y] == 2 : c = 'O'  # trace
               if (X[i],Y[i]) == (x,y) : c ='X'  # joueur
               print(c,sep='', end = '')
            print(" ",sep='', end = '') # espace entre les grilles
        print("") # retour à la ligne


###########################################################
#
# simulation en parallèle des parties


# Liste des directions :
# 0 : sur place   1: à gauche  2 : en haut   3: à droite    4: en bas

dx = np.array([0, -1, 0,  1,  0],dtype=np.int32)
dy = np.array([0,  0, 1,  0, -1],dtype=np.int32)

# scores associés à chaque déplacement
ds = np.array([0,  1,  1,  1,  1],dtype=np.int32)

Debug = True
nb = 5 # nb de parties


def Simulate(Game):

    # on copie les datas de départ pour créer plusieurs parties en //
    G      = np.tile(Game.Grille,(nb,1,1))
    X      = np.tile(Game.PlayerX,nb)
    Y      = np.tile(Game.PlayerY,nb)
    S      = np.tile(Game.Score,nb)
    I      = np.arange(nb)  # 0,1,2,3,4,5...

    VGauche = np.tile(Game.Score,nb)
    VDroite = np.tile(Game.Score,nb)
    VHaut = np.tile(Game.Score,nb)
    VBas = np.tile(Game.Score,nb)
    
    

    boucle = True
    if Debug : AffGrilles(G,X,Y)

    # VOTRE CODE ICI

    n=0
    while(boucle) :
        if Debug :print("X : ",X)
        if Debug :print("Y : ",Y)
        if Debug :print("S : ",S)

        # marque le passage de la moto
        G[I, X, Y] = 2
        VGauche = G[I,X-1,Y]
        VGauche = (VGauche == 0) * 1

        VDroite = G[I,X+1,Y]
        VDroite = (VDroite == 0) * 1

        VHaut = G[I,X,Y+1]
        VHaut = (VHaut == 0) * 1
    
        VBas = G[I,X,Y-1]
        VBas = (VBas == 0) * 1

        LPossibles = np.zeros((nb,4),dtype=np.int32)
        Tailles = np.zeros(nb,dtype=np.int32)
        
        LPossibles[I,Tailles] = VGauche * 1
        Tailles += VGauche

        LPossibles[I,Tailles] = VHaut * 2
        Tailles += VHaut

        LPossibles[I,Tailles] = VDroite * 3
        Tailles += VDroite

        LPossibles[I,Tailles] = VBas * 4
        Tailles += VBas

        Tailles[Tailles==0] = 1
 
        R = np.random.randint(Tailles)
        Choix = LPossibles[I,R]
        DX = dx[Choix]
        DY = dy[Choix]

        if Debug : print("DX : ", DX)
        if Debug : print("DY : ", DY)

        X += DX
        Y += DY

        S += ds[Choix]

        n+=1
        if np.all(LPossibles) == 0 : print ("run {}".format(n))

        #debug
        if Debug : AffGrilles(G,X,Y)
        if Debug : time.sleep(2)

    print("Scores : ",np.mean(S))



Simulate(GameInit)

