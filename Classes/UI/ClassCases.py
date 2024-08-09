import pygame
from Classes import MainGame

class CasesCouleur:
    def __init__(self, Piece : object, Position : str, Situation : tuple, CanBeClicked : bool, Special : str): #Position(X, Y)

        Img = Situation[0]
        Allie = False

        if MainGame.GameInfos.PlrMode == "PvE":
            if MainGame.GameInfos.Tour["Couleur"] == Piece.Couleur and MainGame.GameInfos.Player1["Couleur"] == Piece.Couleur:
                Allie = True
        else:
            if MainGame.GameInfos.Tour["Couleur"] == Piece.Couleur:
                Allie = True

        if Allie == True:                        #Donne la Couleur de la Situation en fonction de l'Objet sur la Case
            if Special != None:
                Img = 'SpecialMove'
            Img = MainGame.ImgCases["TourduJr"][Img]
        else:
            if Special != None:
                Img = 'Empty'
            CanBeClicked = False
            Img = MainGame.ImgCases["TourAdverse"][Img]

        self.Name = "Case"                                                  #Permet d'identifier l'Objet
        self.SpecialMove  = Special                                         #Coup Spécial Possible sur la Case
        self.Situation = Situation                                          #Situation de la Case, c'est-à-dire Ennemi, Allié ou Rien
        self.Image = pygame.image.load("Images/Cases/" + str(Img)).convert_alpha()                 #Image de la Case
        self.Position = Position                                            #Position de la Case
        self.HasHitBox = CanBeClicked                                       #Savoir si l'Objet a une HitBox ou Non
        if CanBeClicked == True:                                            #Si la Case doit avoir une HitBox, alors en créer une (cela permet de ne pas créer d'HitBox inutile)
            self.HitBox = self.Image.get_rect()                             #Créer la HitBox de la Case
            self.HitBox.midbottom = Position                                #Met la HitBox à la Position de la Case
        else:
            self.HitBox = (Position[0] - 40, Position[1] - 80)              #Position de l'Image pour l'afficher avec le 'blit()'
        self.Piece = Piece                                                  #Pièce qui a créé la Case (Objet)
        self.clicked = False                                                #Savoir si la Case a été cliqué ou non
        self.Disabled = False                                               #Savoir si la Case est active ou non

        #Menu.screen.blit(self.Image, self.rect)

        #self.Draw(Menu.screen)

        MainGame.ListAfficheObj.insert(0, self)                             #Affiche la Case
        MainGame.ObjetCases.append(self)                                    #Ajoute la Case dans le Liste des Cases

    def Clicked(self):
        if self.clicked == True or self.Disabled == True: return                        #Vérifie si la Case a déjà été cliqué ou non
        if MainGame.GameInfos.GamePaused == True: return                                #Si le Jeu est en Pause
        self.clicked = True                                                             #La Case a été cliqué
        if MainGame.GameInfos.Tour["Couleur"] == self.Piece.Couleur:                    #Vérifie si c'est bien au Tour du Joueur
            self.Piece.NewPosition(self.Position, self.Situation, self.SpecialMove)     #Déplace la Pièce a l'emplacement de la Case
            """Désactivation de l'Objet et Arrêt de son Affichage !"""
            self.Disabled = True
            self.HitBox.size = (0, 0)