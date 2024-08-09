import pygame

class Box:
    def __init__(self, Pos : tuple, Size : tuple):
        self.Name = "InputBox"
        self.HasHitBox = True
        self.HitBox = pygame.Rect(Pos, Size)
        self.font = pygame.font.SysFont("Verdana", (18, 0), True, False)
        self.Value = ""
        self.Active = False
    
    def Clicked(self):
        pass