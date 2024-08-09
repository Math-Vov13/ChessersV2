from Classes import MainGame
from time import time as Time
#Importer sleep aussi ?

ValeursP = {"Pion" : 1, "Cavalier" : 3, "Fou" : 3, "Tour" : 5, "Dame" : 9, "Roi" : float("inf")}
GameInfos = MainGame.GameInfos
#GameInfos = ""

class Arbre:
    def __init__(self, infos : dict):
        self.Racine : int = None  #La racine
        self.Valeur : int   #La valeur du Coup
        self.Piece : object #La Pièce
        self.Coup : dict    #Les informations du Coup
        self.Plateau : dict #Après simulation
        self.Enfants : list = [] #Les coups enfants
        self.Profondeur : int
    
    def AddChildren(self, Child : object):
        global L
        if Child and type(Child) == Arbre:
            self.Enfants.append(Child)
            #L+=1
    
    def getTree(self):
        pass


def GetMoves(Pieces : list, Plateau : dict):
    Nouveau = {}
    for Piece in Pieces:
        if not Piece in Nouveau:
            Nouveau[Piece] = []
        print(Nouveau)
        Nouveau[Piece].append(Piece.Movements)
        print(Nouveau)
    
    return Nouveau

def evaluate(Piece : object, Coup : tuple):
    Position = Coup[0]
    PieceatPos = Coup[1]
    
    if PieceatPos and PieceatPos.IsEnnemy(Piece):
        ValeursP[PieceatPos.Name]
    
    #Fonction d'auto évaluation pour savoir si le milieu est pris ou pas

    return 0

L = 0
C = {0 : [], 1 : [], 2 : [], 3 : []}
def CreateTree(Piece : object, Plateau : dict,  CouleurPieces : dict, Couleurs : dict, MaxDepth : int, ActuDepth : int = 1):
    # Si on a atteint la limite de profondeur !
    global L
    global C
    #print("CALLED !")
    #L+=1
    if ActuDepth >= MaxDepth:
        return 0
    
    GetMoves([Piece], Plateau)
    Moves = Piece.Movements

    # Si la Pièce n'a aucun mouv
    if Moves["MoveNbr"] == 0:
        return 0

    # Sinon
    MovesList = Moves['Empty'] + Moves['Ennemy'] + Moves['Special']
    for Key in Moves.keys():
        if Key == "Allie" or Key == "CanCaptureKing" or Key == "MoveNbr":
            continue
        for Move in Moves[Key]:
            Noeud = Arbre(Move)                         #Créer une feuille dans l'arbre
            SimulateBoard = Piece.SimulateMove(Plateau, Move[0]) #Simule le mouvement de la Pièce sur le plateau
                    
            #Récupérer les infos
            Noeud.Racine = None
            Noeud.Piece = Piece
            Noeud.Coup = Move
            Noeud.Plateau = SimulateBoard           #Récupère le plateau après le coup
            Noeud.Valeur = evaluate(Piece, Move)    #Récupère le poids du Coup
            Noeud.Profondeur = ActuDepth

            if Noeud.Coup[1] and Noeud.Coup[1].IsEnnemy(Piece):
                CouleurPieces[Couleurs["Ennemy"]].remove(Noeud.Coup[1]) #Retire la pièce capturée de la partie

            """
            print("Obj :", Noeud)
            print("Racine :", Noeud.Racine)
            print("Piece :", Noeud.Piece)
            print("Poids :", Noeud.Valeur)
            print("Coup :", Noeud.Coup)
            print("Plateau :", Noeud.Plateau)
            print("Enfants :", Noeud.Enfants)
            print("Profondeur :", Noeud.Profondeur)
            """

            i = 0
            for p in CouleurPieces[Couleurs["Ennemy"]]:
                L+=1
                i+=1
                C[ActuDepth].append(L)
                Noeud.AddChildren(CreateTree(p, dict(Noeud.Plateau), dict(CouleurPieces), {"Allie": Couleurs["Ennemy"], "Ennemy": Couleurs["Allie"]}, MaxDepth, ActuDepth+1))
                #Faire l'histoire de min-max et récupérer le meilleur coup (en fontion de la valeur) - / +

                #print(f"Salut : {C[ActuDepth]}")
            return Noeud

    # for i in range(Depth):

    #     #Récupère la couleur
    #     Color = CouleurIA
    #     if i == 1 or i == 2:
    #         print("Les Coups possible du Joueur :")
    #         Color = CouleurJr
    #     else:
    #         print("Les Coups possible de l'IA :")

    #     for Piece in CouleurPieces[Color]:
    #         Moves = Piece.Movements

    #         # Si la Pièce n'a aucun mouv
    #         if Moves["MoveNbr"] == 0:
    #             continue

    #         MovesList = Moves['Empty'] + Moves['Ennemy'] + Moves['Special']
    #         for Key in Moves.keys():
    #             if Key == "Allie" or Key == "CanCaptureKing" or Key == "MoveNbr":
    #                 continue
    #             for Move in Moves[Key]:
    #                 Noeud = Arbre(Move)                         #Créer une feuille dans l'arbre
    #                 SimulateBoard = Piece.SimulateMove(Move[0]) #Simule le mouvement de la Pièce sur le plateau
                    
    #                 #Récupérer les infos
    #                 Noeud.Racine = None
    #                 Noeud.Piece = Piece
    #                 Noeud.Coup = Move
    #                 Noeud.Plateau = SimulateBoard           #Récupère le plateau après le coup
    #                 Noeud.Valeur = evaluate(Piece, Move)    #Récupère le poids du Coup
    #                 Noeud.Profondeur = i

    #                 Tree.append(Noeud)

    #                 print("Obj :", Noeud)
    #                 print("Racine :", Noeud.Racine)
    #                 print("Piece :", Noeud.Piece)
    #                 print("Poids :", Noeud.Valeur)
    #                 print("Coup :", Noeud.Coup)
    #                 print("Plateau :", Noeud.Plateau)
    #                 print("Enfants :", Noeud.Enfants)
    #                 print("Profondeur :", Noeud.Profondeur)

def getTreeLen(Tree):
    #print("parcourt")
    
    TotalLen = 0
    if type(Tree) == list:
        for T in Tree:
            TotalLen += getTreeLen(T) + 1
            #print(TotalLen)
    
    elif type(Tree) == Arbre:
        for Child in Tree.Enfants:
            TotalLen += getTreeLen(Child) + 1
            #print(TotalLen)
    
    return TotalLen

def CreateAllTrees(Plateau : dict, ObjetPieces : list, CouleurPieces : dict, CouleurIA : str, CouleurJr : str, Depth : int = 2):
    global L
    Trees = []
    L=0
    StartT = Time()
    for Piece in CouleurPieces[CouleurIA]:
        Tree = CreateTree(Piece, dict(Plateau), dict(CouleurPieces), {"Allie": CouleurIA, "Ennemy": CouleurJr}, Depth)
        print(type(Tree))
        if type(Tree) == Arbre:
            Trees.append(Tree)

    DeltaT = Time()
    print("Taille :", len(Trees))
    print("Trees :", Trees)
    print("Tous les coups calculés :", getTreeLen(Trees))
    print("Called :", L)
    print("Test :", C)
    print("Temps pris :", DeltaT - StartT)

    return Trees

def minimax(Arbre):
    print("Taille de l'arbre :", len(Arbre))
    SystemError()
    return None


class IA:
    def __init__(self, Name : str, Color : str, EnnemyColor : str, Depth : int = 5, Help : bool = False):
        self.Name = Name                #Nom de l'Ia
        self.Couleur = Color            #Couleur des Pièces de l'Ia
        self.PlrCouleur = EnnemyColor   #Couleur des Pièces Ennemies

        self.Profondeur = Depth         #Profondeur de l'Arbre des Possibles utilisé pour l'Ia
        self.Assiste = Help             #Utilisé pour le Mode Assist
    
    def PlayMove(self):
        """Cherche le meilleur coup et le joue ensuite"""

        if GameInfos.GamePaused == False and self.Couleur == GameInfos.Tour["Couleur"]:
            print("Calculating Next Move...")
            Piece, Pos, Situation, CP = self.FindBestMove(GameInfos.Positions, MainGame.ObjetPieces, MainGame.CouleurPieces, GameInfos.Tour["Couleur"], GameInfos.NextColor(GameInfos.Tour["Couleur"]), 3)
            print("Le meilleur mouvement est :", Pos, " -->", GameInfos.Translate(Pos))
            print("La situation est :", Situation)
            print("La pièce qui effectue le meilleur mouvement est :", Piece)
            #sleep(3)
            Piece.NewPosition(Pos, Situation, CP) #Change la Position de la Pièce


    def FindBestMove(self, Positions : dict, ObjetPieces : list, CouleurPieces : dict, Couleur1 : str, Couleur2 : str, Depth : int):
        """Trouve le meilleur mouvement à faire"""

        # Créer un abre des possibles
        ArbreDesPossibles = CreateAllTrees(Positions, ObjetPieces, CouleurPieces, Couleur1, Couleur2, Depth)
        print("Arbre des Possibles :", ArbreDesPossibles)

        # Trouver le meilleur coup à jouer
        Noeud = minimax(ArbreDesPossibles)
        return Noeud.Piece, Noeud.Position, Noeud.Situation, Noeud.CoupSpecial

# Racine1 = {"value" : "Racine", "left" : None, "right" : None}
# def AddMapple(Racine, Nm=0):
#     if Nm >= 3:
#         return
    
#     Nm += 1
#     RacineL = Racine["left"] = {"value" : "Left", "left" : None, "right" : None}
#     AddMapple(RacineL, Nm)
#     RacineR = Racine["right"] = {"value" : "Right", "left" : None, "right" : None}
#     AddMapple(RacineR, Nm)

# AddMapple(Racine1)
# print(Racine1)

# TT = {(10):["a", "Obj"], (12):["a", "Obj1"]}
# def test():
#     Board = dict(TT)  #On copie le Plateau actuel
        
#     PieceCapture = None                         #La Piece capturée
#     PosInf = list(Board[10])                    #Les infos de la Position
#     PieceOnPos = PosInf[1]                      #Récupère la Pièce sur la position
#     if PieceOnPos:                              #Si il y a une Pièce sur la position
#         if PieceOnPos == "Obj1":  #Si c'est un allié
#             return None                         #Ne fais rien
#         else:
#             PieceCapture = PieceOnPos           #Récupère la Pièce qui sera capturée
        
#     PosInf[1] = "Moi meme"                           #Place la Pièce à la position
#     Board[10] = PosInf
#     return Board, PieceCapture      #Retourne le nouveau Plateau et la Pièce capturée
# print(TT)
# print(test())
# print(TT)