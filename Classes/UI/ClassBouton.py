import pygame

class BoutonMenu():
    def __init__(self, Pos : tuple, Size : tuple, Image : str, Utility : str, AddLvl : int):
        #width = image.get_width()
        #height = image.get_height()
        self.Name = "Bouton"
        self.Utility = Utility
        self.AddLvl = AddLvl
        self.Image = pygame.transform.scale(Image, Size) #pygame.transform.scale(Image,((width*scale), (height*scale))) #Transforme la taille de l'Image
        self.Position = Pos
        self.HasHitBox = True                                              #Savoir si l'Objet a une HitBox ou Non
        self.HitBox = self.Image.get_rect() #Créer une HitBox
        self.HitBox.topleft = Pos
        self.CanBeClicked = True
        self.clicked = False
    
    def Clicked(self):
        self.clicked = True
    
    def ResetClick(self):
        self.clicked = False