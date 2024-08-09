from Classes import MainGame
from time import sleep

ValeursP = {"Pion" : 1, "PionPEP" : 1, "Cavalier" : 3, "Fou" : 3, "Tour" : 5, "Dame" : 9, "Roi" : float("inf")}
GameInfos = MainGame.GameInfos

"""{'Empty': [((200, 320), None, None)],
'Allie': [],
'Ennemy': [((120, 320), <Classes.ClassPion.Pion object at 0x00000151F2A7DC60>, None)],
'Special': [((280, 320), ('Ennemy', <Classes.ClassPionPEP.PionPEP object at 0x00000151F2A7C130>), 'PriseEnPassant')],
'CanCaptureKing': False,
'MoveNbr': 3}"""

"""
Mon IA = {Coups : {Coups : {Coups : {}}, Coups : {Coups : {}}}, Coups, Coups, Coups, Coups, Coups, Coups}

ArbreBinaire = [[[Coups1, Noeud, [[Coups1, Noeud, Coups2], Noeud, Coups2]], Noeud, Coups2], Noeud, [[Coups1, Noeud, Coups2], Noeud, Coups2]]
"""

class ArbreNoeud:
    def __init__(self, Parent : object, Poids : int, S, Spec, P, Pos, Depth : int):
        self.Parent = Parent
        self.Depth = Depth
        self.Poids = Poids
        self.Situation = S
        self.CoupSpecial = Spec
        self.Piece = P
        self.Position = Pos
        self.Childrens = []
    
    def AddChilds(self, NewChild : object):
        self.Childrens.append(NewChild)
        NewChild.Parent = self


"""def GetMoves():
    Piece"""


def CreateTree(Positions : dict, ObjetPieces : list, CouleurPieces : dict, Couleur1 : str, Couleur2 : str, MaxDepth : int, Depth = 0):
    Profondeurs = []
    for Piece in CouleurPieces[Couleur1]:
        Moves = Piece.Movements
        #print(Piece, Moves)
        if Moves["MoveNbr"] == 0:
            continue

        """MovesList = Moves['Empty'] + Moves['Ennemy'] + Moves['Special']
        for Move in MovesList:
            Poids = evaluate(Move)
            N = ArbreNoeud(None, Poids, Move, Piece, Depth)
            Profondeurs.append(N)
            #print(N.Poids)"""
        
        MovesList = Moves['Empty'] + Moves['Ennemy'] + Moves['Special']
        for Key in Moves.keys():
            if Key == "Allie" or Key == "CanCaptureKing" or Key == "MoveNbr":
                continue
            for Move in Moves[Key]:
                Poids = evaluate(Move)
                N = ArbreNoeud(None, Poids, (Key, Move[1]), Move[2], Piece, Move[0], Depth)
                Profondeurs.append(N)

    return Profondeurs

def evaluate(Move : dict):
    if Move[1] == None:
        return 0
    
    if type(Move[1]) == tuple:
        if Move[1][0] != "Ennemy":
            return 0
        else:
            return ValeursP[Move[1][1].Name]
    else:
        return ValeursP[Move[1].Name]

def minimax(ArbreList : list):
    Max = ArbreList[0]
    for Noeud in ArbreList:
        if Noeud.Poids > Max.Poids:
            Max = Noeud

    if Max.Poids == 0:
        import random
        return random.choice(ArbreList)
    else: 
        return Max

def FindBestMove(Positions : dict, ObjetPieces : list, CouleurPieces : dict, Couleur1 : str, Couleur2 : str, Depth : int):
    ArbreDesPossibles = CreateTree(Positions, ObjetPieces, CouleurPieces, Couleur1, Couleur2, Depth)
    #print(ArbreDesPossibles)
    Noeud = minimax(ArbreDesPossibles)
    #time.sleep(1)
    return Noeud.Piece, Noeud.Position, Noeud.Situation, Noeud.CoupSpecial


class IA:
    def __init__(self, Name : str, Color : str, EnnemyColor : str, Depth : int, Help : bool):
        self.Name = Name                #Nom de l'Ia
        self.Couleur = Color            #Couleur des Pièces de l'Ia
        self.PlrCouleur = EnnemyColor   #Couleur des Pièces Ennemies

        self.Profondeur = Depth         #Profondeur de l'Arbre des Possibles utilisé pour l'Ia
        self.Assiste = Help             #Utilisé pour le Mode Assist
    
    def PlayMove(self):

        if GameInfos.GamePaused == False and self.Couleur == GameInfos.Tour["Couleur"]:
            print("Calculating Next Move...")
            Piece, Pos, Situation, CP = self.FindBestMove(GameInfos.Positions, MainGame.ObjetPieces, MainGame.CouleurPieces, GameInfos.Tour["Couleur"], GameInfos.NextColor(GameInfos.Tour["Couleur"]), 3)
            print("Le meilleur mouvement est :", Pos, " -->", GameInfos.Translate(Pos))
            print("La situation est :", Situation)
            print("La pièce qui effectue le meilleur mouvement est :", Piece)
            #sleep(3)
            Piece.NewPosition(Pos, Situation, CP) #Change la Position de la Pièce


    def FindBestMove(self, Positions : dict, ObjetPieces : list, CouleurPieces : dict, Couleur1 : str, Couleur2 : str, Depth : int):
        ArbreDesPossibles = CreateTree(Positions, ObjetPieces, CouleurPieces, Couleur1, Couleur2, Depth)
        print(ArbreDesPossibles)
        Noeud = minimax(ArbreDesPossibles)
        return Noeud.Piece, Noeud.Position, Noeud.Situation, Noeud.CoupSpecial