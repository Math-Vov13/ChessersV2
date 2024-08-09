"""Import de toutes les Classes des Pièces pour la partie"""
import pygame
import threading
from Classes.UI import ClassEchiquier as Echiquier
from Classes.Pieces import ClassPion, ClassCavalier, ClassFou, ClassTour, ClassDame, ClassRoi

"""Variables"""
Lettres = ["A", "B", "C", "D", "E", "F", "G", "H", "I"] #List utilisé pour la création de l'échiquier
ImgCases = {"TourduJr" : {"Empty" : "vert_claire.png", "Allie" : "vert_foncer.png", "Ennemy" : "rouge.png", "SpecialMove" : "coup_special.png"}, "TourAdverse" : {"Empty" : "gris_claire.png", "Allie" : "gris_foncer.png", "Ennemy" : "gris_foncer.png"}} #Dict utilisé pour avoir le nom de l'image correspondant à chaques couleur des cases select
ImgPieces = {"Blanc" : {"Pion" : "pion_beige.png", "Cavalier" : "cavalier_beige.png", "Fou" : "fou_beige.png", "Tour" : "tour_beige.png", "Dame" : "reine_beige.png", "Roi" : "roi_beige.png"}, "Noir" : {"Pion" : "pion_noir.png", "Cavalier" : "cavalier_noir.png", "Fou" : "fou_noir.png", "Tour" : "tour_noir.png", "Dame" : "reine_noir.png", "Roi" : "roi_noir.png"}} #Dict utilisé pour avoir le nom de l'image correspondant à la Pièce du Jeu
PionPEPList = {"Blanc" : None, "Noir" : None}
Placements = ["Tour", "Cavalier", "Fou", "Dame", "Roi", "Fou", "Cavalier", "Tour", "Pion"]
ObjetPieces = []                        #List qui contient toutes les Pièces pour les afficher
CouleurPieces = {"Blanc": [], "Noir" : []}
ObjetCases = []                         #List qui contient toutes les Cases pour les afficher
ListAfficheObj = []                     #Liste qui affiche les Objets
ActualScreen = None                     #Ecran qui sera défini par le Menu

ColorBordure, ColorCaseNoire, ColorCaseBlanche = (191,127,69), (102,51,0), (245,245,220)          #Couleurs de l'échiquier


class Game:
    def __init__(self):
        """Statut de la Partie"""
        self.Tour = {'Nbr' : 0, 'Couleur' : ''}                             #Tour de la Partie
        self.Player1 = {'Pseudo' : "", 'Couleur' : "", 'Bot' : False}       #Player1
        self.Player2 = {'Pseudo' : "", 'Couleur' : "", 'Bot' : False}       #Player2
        self.GameMode = ""                                                  #Mode de Jeu
        self.PlrMode = ""                                                   #Mode de Joueur
        self.InMenu = True                                                  #Joueur dans le Menu
        self.GameStarted = False                                            #Partie Démarrée
        self.GamePaused = False                                             #Jeu en Pause
        self.GameEnded = False                                              #Partie Terminée
        self.Winner = ""                                                    #Gagnant
        self.SoundPlaying = ""                                              #Son Joué actuellement
        self.GameChecking = False                                           #Vérifie les Infos de la Partie

        """Timer"""
        self.TimerObj = None                                                #Le Timer du Jeu
        self.StartTime = 0                                                  #Temps à laquelle la Partie a démarré (pour savoir combien de temps elle a durée à la fin)
        self.Timer = 30                                                     #Temps avant élimination

        """Pièces"""
        self.PSelected = ""                                                 #Pièce sélectionné
        self.Clicking = False                                               #Savoir si un Objet est entrain d'être Cliqué ou non
        self.Pion2C = ""                                                    #Pion qui a fait sauté 2 Cases
        self.PiecesR = {"Blanc" : 0, "Noir" : 0}                            #Pièces restantes en Jeu
        self.IsChess = {"Blanc" : [False, None], "Noir" : [False, None]}    #Couleur qui est en Echec

        """Echiquier"""
        self.Echiquier = Echiquier.Echiquier(8, 80, 30)                     #Echiquier
        self.Echiquier.Create(ColorCaseNoire,ColorCaseBlanche,ColorBordure) #Créer l'Echiquier
        self.StartPositions = self.Echiquier.Get_Positions()
        self.Positions = self.StartPositions                                #Positions des Pièces
        self.AttackPos = {"Blanc" : [], "Noir" : []}                        #Positions des Attaques possibles

        """IA"""
        self.GameAI = None                                                  #IA de la Partie
        self.IAActivated = False                                            #Savoir si l'IA est activé ou non
    
    def StartGame(self):
        pass

    def EndGame(self):
        pass

    def ResetGame(self, Visible : bool):                                    #Recommence la Partie à 0
        global CouleurPieces
        """Remet tous les paramètres du Jeu à 0"""
        ListAfficheObj.clear()                                              #Efface tous les Objets Visibles
        ObjetPieces.clear()                                                 #Efface toutes les Pièces
        CouleurPieces = {"Blanc": [], "Noir" : []}                          #Efface toutes les Pièces
        ObjetCases.clear()                                                  #Efface toutes les Cases

        self.PSelected = ""                                                 #Ne sélectionnes aucune Pièce
        self.PiecesR = {"Blanc" : 0, "Noir" : 0}                            #Remet à 0 le Nombre de Pièces sur le Plateau
        self.Tour["Nbr"] = 0
        self.Tour["Couleur"] = self.Player1["Couleur"]                      #Remet le Tour au Joueur 1
        self.IsChess = {"Blanc" : [False, None], "Noir" : [False, None]}    #Couleur qui est en Echec
        #print(self.Positions)
        #print(self.StartPositions.copy())
        #print(self.Echiquier.CasesPositions)
        #self.Positions = self.StartPositions.copy()
        self.Echiquier.Create(ColorCaseNoire, ColorCaseBlanche, ColorBordure)                                        #Recréer l'échiquier avec de nouvelles positions
        self.Positions = self.Echiquier.Get_Positions()
        if Visible == True:                                                 #Si le Joueur a juste mis le jeu en Pause et continue sa partie
            self.PlacerPieces(self.Player1, self.Player2, self.GameMode)    #Créer de nouvelles Pièces
            self.GameStarted = True                                         #Commence la Partie
            self.StartTime = 0                                              #Démarre le temps de la Partie
        self.AttackPos = {"Blanc" : [], "Noir" : []} 
        self.UpdateScreen()                                                 #Met à Jour la fenêtre
        self.NewTour()                                                      #Commence un Nouveau Tour
        #self.SetAttackCase()
        self.InMenu = False
        self.GamePaused = False                                             #Jeu plus en Pause
        self.GameEnded = False                                              #Jeu Recommencé
        self.Winner = ""                                                    #Aucun Gagnant
        if self.GameMode == "Timer":
            self.TimerObj.Init(self.Player1["Couleur"], self.Player2["Couleur"])#Timer remis au départ
            self.TimerObj.StartTime()                                           #Démarre le Timer
        
        if self.PlrMode == "PvE":
            from Classes.AI import AI_Chess as AIClass  #--->AI_Chess
            self.GameAI = AIClass.IA("Ordi", self.Player2["Couleur"], self.Player1["Couleur"], 3, False)

    def UpdateScreen(self):                 #Actualiser le Plateau du Jeu, pour actualiser la Position des Pièces
        """Actualise la fenêtre de Jeu"""
        self.Echiquier.UpdateBoard()
        self.CreationCase(ActualScreen)
        self.CreationPieces(ActualScreen)

    def CreationBoard(self):            #Création du Plateau de Jeu, (Pos --> Si on a besoin de la Position des Pièces ou non)
        """Test = [] #Réglage des positions des cases
        Test2 = []
        for i in self.Positions:
            if not i[0] in Test:
                Test.insert(0, i[0])
            if not i[1] in Test2:
                Test2.append(i[1])
            
        print(Test)
        print(Test2)"""

    def CreationCase(self, screen):                 #Mise en place des Cases
        for Object in ObjetCases:
            screen.blit(Object.Image, Object.HitBox)

    def CreationPieces(self, screen):               #Mise en place des pièces
        for Object in ObjetPieces:
            screen.blit(Object.Image, Object.HitBox)
    
    def AfficheCases(self, Piece : object, CasesList : dict):
        from Classes.UI import ClassCases
        for Key in CasesList:
            if type(CasesList[Key]) != list:
                continue

            for Value in CasesList[Key]: #('F5', Pièce, 'PriseEnPassant')
                HitBox = True
                if Key == "Allie":
                    HitBox = False
                ClassCases.CasesCouleur(Piece, Value[0], (Key, Value[1]), HitBox, Value[2])
    
    def ClearCases(self):
        for Case in ObjetCases:
            #if Case in ListAfficheObj:
            ListAfficheObj.remove(Case)
        ObjetCases.clear()
        self.PSelected = ""
        #self.CreationCase(ActualScreen)
    
    def DeletePiece(self, Piece : object):
        self.PieceDied(Piece.Couleur)
        ObjetPieces.remove(Piece)
        CouleurPieces[Piece.Couleur].remove(Piece)
        ListAfficheObj.remove(Piece)


    def ChangeTour(self):                           #Change le Tour actuel
        #from Classes import ChessAI
        if self.GamePaused == False:
            self.GameChecking = True
            self.GamePaused = True
            print(self.Positions)
            if self.Tour["Couleur"] == self.Player1["Couleur"]:
                self.Tour["Couleur"] = self.Player2["Couleur"]
                self.CreateMoves() #J'aimerai l'éviter :/
            else:
                self.NewTour()
            self.DeletePEP(self.Tour["Couleur"])
            #Menu.ResetTimer()
            """if self.Player1["Couleur"] == self.Tour["Couleur"]:
                if self.Player1["Bot"] == True:
                    ChessAI.Play_Move(self.Positions, CouleurPieces[self.Tour["Couleur"]])
            else:
                if self.Player2["Bot"] == True:
                    ChessAI.Play_Move(self.Positions, CouleurPieces[self.Tour["Couleur"]])"""
            self.GamePaused = False
            self.GameChecking = False
            if self.PlrMode != "PvE":
                return

            if self.PlrMode == "PvE":
                TH = threading.Thread(target = self.AIPlaying)
                TH.start()
            """if self.GameMode == "Assist" and self.Tour["Couleur"] != self.Player2["Couleur"] or self.Tour["Couleur"] == self.Player2["Couleur"]:
                Piece, Pos, Situation, CP = IA.FindBestMove(self.Positions, ObjetPieces, CouleurPieces, self.Tour["Couleur"], self.NextColor(self.Tour["Couleur"]), 3)
                print("Le meilleur mouvement est :", Pos)
                print("La situation est :", Situation)
                print("La pièce qui effectue le meilleur mouvement est :", Piece)
                Piece.NewPosition(Pos, Situation, CP)"""
    
    def AIPlaying(self):
        self.GameAI.PlayMove()
    
    def NextColor(self, Couleur : str):
        if Couleur == self.Player1["Couleur"]:
            return self.Player2["Couleur"]
        else:
            return self.Player1["Couleur"]

    def NewTour(self):
        #print(self.Positions)
        self.Tour['Nbr'] += 1
        self.Tour["Couleur"] = self.Player1["Couleur"] #Remet le Tour au Joueur 1
        self.CreateMoves()
        #PRINT LE RESULTAT SUR UN FICHIER .Txt
    
    def DeletePEP(self, Tour : str):
        """Efface les Prises en Passant qui ne sont plus"""
        Couleur = self.NextColor(Tour)
        if PionPEPList[Couleur] is not None:
            self.Positions[PionPEPList[Couleur].Position][1] = None
        PionPEPList[Couleur] = None

    def PlacerPieces(self, Couleur1 : str, Couleur2 : str, GameMode : str): #Place les Pièces
        """Place les Nouvelles Pièces sur le Plateau"""

        Places = Placements
        if Couleur1["Couleur"] == "Noir": #Définit la Position de la Dame en fonction de la Couleur de la Case (Dame Blanche sur Case Blanche et Dame Noire sur Case Noire)
            Places[3] = "Dame"
            Places[4] = "Roi"
        elif Couleur1["Couleur"] == "Blanc":
            Places[3] = "Roi"
            Places[4] = "Dame"
        
        Couleurs = (Couleur2["Couleur"], Couleur1["Couleur"])
        Sens = ("Haut", "Bas")
        PosX = [680, 600, 520, 440, 360, 280, 200, 120] #1, 2, 7, 8
        PosY = [160, 240, 720, 640] #A, B, H, G
        YIndex = -1
        for z in range(2): #S'occuper d'abord de la rangée du haut, puis du bas
            Couleur = Couleurs[z]
            Sens2 = Sens[z]
            YIndex += 1
            XIndex = -1
            for v in Places: #Place chaque Pièces une par une
                XIndex += 1
                ImgPiece = v + '_' + Couleur + '.png'
                if v == "Cavalier":
                    ListAfficheObj.append(ClassCavalier.Cavalier(v, Couleur, ImgPieces[Couleur][v], (PosX[XIndex], PosY[YIndex])))

                elif v == "Fou":
                    ListAfficheObj.append(ClassFou.Fou(v, Couleur, ImgPieces[Couleur][v], (PosX[XIndex], PosY[YIndex])))
                    
                elif v == "Tour":
                    if GameMode == "USA/UK" and z != 1:
                        continue
                    ListAfficheObj.append(ClassTour.Tour(v, Couleur, ImgPieces[Couleur][v], (PosX[XIndex], PosY[YIndex])))
                    
                elif v == "Dame":
                    if GameMode == "USA/UK" and z != 0:
                        continue
                    ListAfficheObj.append(ClassDame.Dame(v, Couleur, ImgPieces[Couleur][v], (PosX[XIndex], PosY[YIndex])))
                    
                elif v == "Roi":
                    ListAfficheObj.append(ClassRoi.Roi(v, Couleur, ImgPieces[Couleur][v], (PosX[XIndex], PosY[YIndex])))
                    self.IsChess[Couleur][1] = (PosX[XIndex], PosY[YIndex])
                    
                elif v == "Pion":
                    YIndex += 1
                    XIndex = -1
                    for _ in range(1, 9):
                        XIndex += 1
                        ListAfficheObj.append(ClassPion.Pion(v, Couleur, ImgPieces[Couleur][v], (PosX[XIndex], PosY[YIndex]), Sens2))

    def PieceAjout(self, Couleur):      #Ajoute une Pièce sur le Plateau
        self.PiecesR[Couleur] += 1

    def PieceDied(self, Couleur):       #Enlève une Pièce sur le Plateau
        self.PiecesR[Couleur] -= 1
    
    def EchecetMath(self, CouleurP : str):    #Echec et Math (Couleur du Perdant)
        """Fin de la Partie"""
        print("ECHEC ET MATHS !!!")
        self.GamePaused = True
        self.GameEnded = True
        self.GameStarted = False
        if CouleurP == self.Player1["Couleur"]:
            self.Winner = self.Player2["Pseudo"]
        else:
            self.Winner = self.Player1["Pseudo"]

    def Translate(self, trad):          #Permet de passer du Str au Tuple / Tuple au Str
        """Traduit le nom d'une Case en sa coordonnée et inversion."""
        Result = None
        if type(trad) == str:           #Si Nom d'une Case, alors renvoyer sa Position
            Result = self.Positions[trad][0]
        elif type(trad) == tuple:       #Si Position, alors renvoyer le Nom de la Case correspondante
            for i in self.Positions:
                if self.Positions[i][0] == trad:
                    Result = i
                    break
        else:                           #Si trad n'est pas du Str ou Tuple (dans ce cas j'ai dû faire une erreur dans mon code...)
            pass
            #print("Traduction Impossible !")

        return Result

    def FindCase(self, PosDepart : tuple, PosArriv : tuple): #PosArriv --> (x, y)
        """Renvoie le Nom de la Case recherchée"""
        TailleC = self.Echiquier.taille_case
        Result = PosDepart
        Rx, Ry = PosDepart[0], PosDepart[1]
        x = PosArriv[0]
        y = PosArriv[1]
        if x != 0:                                          #X
            Nbr = TailleC * x
            Rx += Nbr
            Result = (Rx, Result[1])
            if not Result in self.Positions.keys():         #Case non existante
                return None

        if y != 0:                                          #Y
            Nbr = TailleC * y
            Ry += Nbr
            Result = (Result[0], Ry)
            if not Result in self.Positions.keys():         #Case non existante
                return None

        return Result
    
    def CreateMoves(self):
        #NbrMoves = {'Player1' : 0, 'Player2' : 0}
        for Piece in ObjetPieces:
            #print(Piece, Piece.Position, self.Translate(Piece.Position))
            print(Piece.AvailableMovements(Piece.Position))
        #print()
        
        #print(self.Positions)
    
    def FindAttackedCase(self, List : list):
        if len(List) == 0:
            return
        else:
            Piece = List.pop(0)
            for i in Piece.Movements:
                if (i == "Ennemy" or i == "Empty") and len(Piece.Movements[i]) > 0:
                    for v in Piece.Movements[i]:
                        self.AttackPos[Piece.Couleur][v[0]] = Piece
            self.FindAttackedCase(List)
    
    def SetAttackCase(self):
        Positions = {}
        for Key in self.Positions:
            Positions[Key] = None
        
        self.AttackPos["Blanc"] = Positions
        self.AttackPos["Noir"] = Positions
        print(self.AttackPos)
        self.FindAttackedCase(ObjetPieces)
        
        print(self.AttackPos)

            


    def IsChessVerification(self):
        """Vérifie si un des Roi est en Echec"""
        self.Checking = True
        for Object in ObjetPieces:
            print("test")
        self.Checking = False
        return


"""Création de la Fenêtre de Jeu"""
pygame.init()
pygame.display.init()

GameInfos = Game()      #Création des Données du Jeu