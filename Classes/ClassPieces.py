import pygame, random
from copy import deepcopy

SonCapture = "Sounds/capture.mp3"                 #Charge le Son de Capture
SonBouger = "Sounds/bouge.mp3"                    #Charge le Son de Déplacement
SonRoque = "Sounds/roque.mp3"                     #Charge le Son du Roque


class Pieces:
    def __init__(self, Piece : str, Couleur : str, Image : str, Position : tuple):
        from Classes import MainGame
        self.Name = Piece                                                   #Permet d'identifier l'Objet (au lieu d'utiliser la méthode 'isinstance' et donc de devoir import toutes les pièces à chaques fois)
        self.Couleur = Couleur                                              #La Couleur de la Pièce (= sa Team) donc Noir ou Blanc
        self.Position = Position                                            #La Position de la Pièce

        if Image == "": return                                              #Si c'est un Pion pour la PEP, alors ne pas continuer
        self.Image = pygame.image.load("Images/Pieces/" + str(Image)).convert_alpha()#L'image de la Pièce affiché à l'écran (convert_alpha() permet de ne pas bouffer de la RAM donc plus pratique)
        self.HasHitBox = True                                               #Savoir si l'Objet a une HitBox ou Non
        self.HitBox = self.Image.get_rect()                                 #Création d'une Zone cliquable autour de l'image (HitBox)
        self.HitBox.midbottom = Position                                    #Position de la HitBox de l'Image
        self.Movements = {}                                                 #Mouvements Possibles de la Pièce
        self.clicked = False                                                #Savoir si la pièce a été cliqué ou non
        self.Alive = True                                                   #Si la pièce est encore en vie ou non
        self.Disabled = False                                               #L'Objet est Activé ou Non
        self.Clickable = True                                               #Peut être cliqué
        self.SeDeplace = False                                              #Est entrain de se déplacer

        """Afficher la Pièce"""
        #Menu.screen.blit(self.Image, self.rect)
        MainGame.ObjetPieces.append(self)
        MainGame.CouleurPieces[self.Couleur].append(self)
        MainGame.GameInfos.PieceAjout(self.Couleur)
        MainGame.GameInfos.Positions[self.Position][1] = self

    def Clicked(self):
        from Classes import MainGame
        if MainGame.GameInfos.GamePaused == True:
            return
        if MainGame.GameInfos.PSelected != self:
            MainGame.GameInfos.ClearCases()
            MainGame.GameInfos.PSelected = self
            #Si le roi n'est pas en échec
            #print(self.Position)
            #self.AvailableMovements(self.Position)
            MainGame.GameInfos.AfficheCases(self, self.Movements)
            #print(self.Movements)
            #self.Deplacements()

    def Captured(self):                                                         #Quand une Pièce est mangé (=Capturé dans le jargon)
        from Classes import MainGame

        """Supprime la Pièce et la Désactive"""
        self.Alive = False
        self.Disabled = True
        self.HitBox.size = (0, 0)
        MainGame.GameInfos.DeletePiece(self)
        if MainGame.GameInfos.Positions[self.Position][1] == self:
            MainGame.GameInfos.Positions[self.Position][1] = None
        #for i, v in enumerate(MainGame.ObjetPieces):
        #    if v == self:
        #        MainGame.ObjetPieces.pop(i)

        #for i, v in enumerate(MainGame.ListAfficheObj):
        #    if v == self:
        #        MainGame.ListAfficheObj.pop(i)
        
        #if self.Name == "Pion":                                                #Vérifie le Joueur a joué le Coup de la Prise en Passant
        #    if self.PriseEnPassant == True:
        #        for i in MainGame.GameInfos.Positions:
        #            if MainGame.GameInfos.Positions[i][1] == self:
        #                MainGame.GameInfos.Positions[i][1] = None
        
        if self.Name == "Roi":                                                 #Fin de la Partie (le Roi a été Capturé --> Echec et Math)
            MainGame.GameInfos.EchecetMath(self.Couleur)

    def NewPosition(self, Position : tuple, Situation : tuple, SpecialMove : str):              #Change la Position de la Pièce
        print(Position, Situation, SpecialMove)
        #print(Situation)
        from Classes import MainGame
        PlaySound = SonBouger
        #self.SeDeplace = True                                                #La Pièce se déplace
        MainGame.GameInfos.ClearCases()                                      #Efface les Cases

        Piece = Situation[1]
        if Piece != None and type(Piece) == tuple:
            Piece = Situation[1][1]

        if Situation[0] == "Ennemy" or SpecialMove == "Promotion" and Situation[1][0] == "Ennemy":                                     #Si il y a un ennemi, alors la Pièce ennemi a été capturé
            #Objet = MainGame.GameInfos.Positions[Position][1]
            PlaySound = SonCapture
            Piece.Captured()
        elif Situation[0] == "Allie" and Situation[1].Name == "Tour" and self.Name == "Roi":
            PlaySound = SonRoque

        MainGame.GameInfos.Positions[self.Position][1] = None   #Rend l'Ancienne Position de la Pièce Vide
        MainGame.GameInfos.Positions[Position][1] = self        #Ajoute l'Objet a sa Position correspondant dans le Dict des Positions
        self.Position = Position                                                              #Change la Position de la Pièce
        self.HitBox.midbottom = self.Position                                                 #Met la HitBox de la Pièce à sa nouvelle position

        if SpecialMove == "PriseEnPassant":     #Prise En Passant
            Piece.PriseEnPassant()
            PlaySound = SonCapture

        elif SpecialMove == "Promotion":          #Promotion
            self.Promotion()
        
        elif SpecialMove == "Roque":
            self.LeRoque()
            PlaySound = SonRoque

        if self.Name == "Roi":
            MainGame.GameInfos.IsChess[self.Couleur][1] = self.Position
        self.Disabled = True                    #Réactive la Pièce
        
        #self.SeDeplace = False
        pygame.mixer.Sound(PlaySound).play()    #Joue le Son de la Pièce
        MainGame.GameInfos.UpdateScreen()       #Actualisation de la Position des Pièces
        MainGame.GameInfos.ChangeTour()         #Change le Tour
    
    def SimulateMove(self, Plateau, Position : tuple) -> None | tuple:
        Board = deepcopy(Plateau)  #On copie le Plateau actuel
        
        PieceCapture = None                         #La Piece capturée
        PosInf = list(Board[Position])              #Les infos de la Position
        PieceOnPos = PosInf[1]                      #Récupère la Pièce sur la position
        if PieceOnPos:                              #Si il y a une Pièce sur la position
            if PieceOnPos.Couleur == self.Couleur:  #Si c'est un allié
                return None                         #Ne fais rien
            else:
                PieceCapture = PieceOnPos           #Récupère la Pièce qui sera capturée
        
        PosInf[1] = self                            #Place la Pièce à la position
        Board[Position] = PosInf
        return Board                                #Retourne le nouveau Plateau et la Pièce capturée

    def IsEnnemy(self, AutrePiece : object):
        return self.Couleur != AutrePiece.Couleur

    
    def AddMovement(self, Key : str, Value : tuple, KingVerif : bool):
        from Classes import MainGame
        self.Movements[Key].append(Value)                   #Rajoute le Déplacement Possible dans la List des Déplacements de la Pièce
        #Pos = MainGame.GameInfos.Translate(Value[0])
        Piece = MainGame.GameInfos.Positions[Value[0]][1]
        if Piece is None:
            self.Movements['MoveNbr'] += 1                      #Rajoute 1 au Nombre de Déplacement Possible pour la Pièce
            return
        elif Piece.Couleur != self.Couleur or Key == 'Special':
            self.Movements['MoveNbr'] += 1                      #Rajoute 1 au Nombre de Déplacement Possible pour la Pièce

            if KingVerif == True:                               #Si une Vérification de l'Echec peut avoir lieu
                if Piece.Name == "Roi":                         #Vérifie que le Roi adverse n'est pas en échec
                    self.Movements['CanCaptureKing'] = True     #Si le Roi Adverse est en échec alors le noter dans la List
                    MainGame.GameInfos.IsChess[Piece.Couleur][0] = True
                    print("LE ROI ", Piece.Couleur, " EST ATTAQUE !!!")

    def InfosCase(self, Pos : tuple):
        """Fonction qui permet de connaitre les informations d'une Case. Renvoie un tuple (Team, Piece)"""
        from Classes import MainGame
        Team = "Empty"                                  #Réponse
        Piece = MainGame.GameInfos.Positions[Pos][1]    #Objet sur la Case
        if Piece != None:                               #Si il y a un Objet
            if Piece.Couleur == self.Couleur:           #Si l'Objet est allié
                Team = "Allie"                          #Réponse : Allié  
            else:                                       #Si l'Objet est ennemi
                Team = "Ennemy"                         #Réponse : Ennemi

        return (Team, Piece)                            #Renvoie la Réponse et l'Objet sur la Case
    
    def DetectSpecialMove(self, Pos : str):
        from Classes import MainGame
        
        try:
            Piece = MainGame.GameInfos.Positions[Pos][1]
        except KeyError:
            return None
        
        if self.Name == "Pion":
                if Piece is not None and self.Couleur == Piece.Couleur:
                    return None
                StrPos = MainGame.GameInfos.Positions[Pos][0]
                if StrPos[1] == "1" and self.Sens == "Haut" or StrPos[1] == "8" and self.Sens == "Bas":         #Promotion
                    return "Promotion"
        
        if MainGame.GameInfos.GameMode == "Tradition":
            return None

        if Piece is not None and self.Couleur != Piece.Couleur:
            if Piece.Name == "PionPEP" and Piece.Couleur != self.Couleur:                                #Prise en Passant
                return "PriseEnPassant"
        
        if self.Name == "Roi" and self.Roque == False:                                                                          #Roque
            if Piece is not None and Piece.Name == "Tour":
                if Piece.Roque == False:
                    return "Roque"

        return None
    
    #def IsEnnemyKing(self, Pos : str):
    #    from Classes import MainGame
    #    if type(Pos) == tuple:
    #        Pos = MainGame.GameInfos.Translate(Pos)
    #    return MainGame.GameInfos.Positions[Pos][1].Name == 'Roi'

    def Promotion(self):                            #Promotion d'un Pion
        from Classes import MainGame
        from Classes.Pieces import ClassCavalier, ClassFou, ClassTour, ClassDame
        Nbr = random.randint(1, 4)                  #Le Random choisi une des 4 Pièces au hasard
        if Nbr == 1:
            MainGame.ListAfficheObj.append(ClassCavalier.Cavalier("Cavalier", self.Couleur, MainGame.ImgPieces[self.Couleur]["Cavalier"], self.Position))
        elif Nbr == 2:
            MainGame.ListAfficheObj.append(ClassFou.Fou("Fou", self.Couleur, MainGame.ImgPieces[self.Couleur]["Fou"], self.Position))
        elif Nbr == 3:
            MainGame.ListAfficheObj.append(ClassTour.Tour("Tour", self.Couleur, MainGame.ImgPieces[self.Couleur]["Tour"], self.Position))
        elif Nbr == 4:
            MainGame.ListAfficheObj.append(ClassDame.Dame("Dame", self.Couleur, MainGame.ImgPieces[self.Couleur]["Dame"], self.Position))
        self.Captured()                             #Supprime le Pion actuel pour le remplacement par la nouvelle Pièce

    def PriseEnPassant(self):
        self.Creator.Captured()
    
    def LeRoque(self):
        from Classes import MainGame
        Tour = None
        TourPos = ()

        for X in range(-1, 2, 2):
            Pos = MainGame.GameInfos.FindCase(self.Position, (X, 0))

            Piece = MainGame.GameInfos.Positions[Pos][1]
            if Piece is None:
                TourPos = Pos
            else:
                Tour = Piece

        MainGame.GameInfos.Positions[Tour.Position][1] = None   #Rend l'Ancienne Position de la Pièce Vide
        MainGame.GameInfos.Positions[TourPos][1] = Tour        #Ajoute l'Objet a sa Position correspondant dans le Dict des Positions
        Tour.Position = TourPos                                                              #Change la Position de la Pièce
        Tour.HitBox.midbottom = Tour.Position                                                 #Met la HitBox de la Pièce à sa nouvelle position
        Tour.Roque = True