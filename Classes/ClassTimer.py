import pygame

class Timer:
    def __init__(self):
        self.ResetTimer()
    
    def ResetTimer(self):
        """Remets les paramètres du Timer à 0"""
        self.Player1 = {}                       #Infos du Joueur 1
        self.Player2 = {}                       #Infos du Joueur 2

        self.Active = False                     #Timer activé
        self.Paused = False                     #Timer en pause

        self.Start = pygame.time.get_ticks()    #Temps du démarrage du Timer
        self.Time = 0                           #Temps actuel
        self.StartPause = 0                     #Temps du début de la Pause
        self.Pause = 0                          #Durée de la Pause
    
    def Init(self, CouleurJ1 : str, CouleurJ2 : str):
        """Initialise les Paramètres du Timer"""
        self.Player1 = {"Couleur" : CouleurJ1, "Time" : 150}
        self.Player2 = {"Couleur" : CouleurJ2, "Time" : 150}
    
    def GetPlrTime(self, Couleur : str):
        """Récupère le Temps du Joueur"""
        if Couleur == self.Player1["Couleur"]:
            return self.Player1["Time"]
        else:
            return self.Player2["Time"]
    
    def StartTime(self):
        """Démarre le Timer"""
        self.Active = True
    
    def UpdateTimer(self, Timer, PlrCouleur):
        """Actualise le Timer"""
        self.Time = Timer
        if (self.Time - self.Start) // 1000:
            self.Start = self.Time
            return self.RemoveTime(PlrCouleur)
    
    def RemoveTime(self, Couleur):
        """Enlève 1 Seconde au Temps du Joueur"""
        if Couleur == self.Player1["Couleur"]:
            self.Player1["Time"] -= 1
            if self.Player1["Time"] == 0:
                return self.Player1["Couleur"]
        else:
            self.Player2["Time"] -= 1
            if self.Player2["Time"] == 0:
                return self.Player2["Couleur"]
        
        return None

    
    def PauseTimer(self):
        """Arrête le Timer"""
        self.Paused = True
        self.StartPause = self.Time

    def ContinueTimer(self):
        """Relance le Timer"""
        self.Paused = False
        self.Start =  self.Time
        self.Pause = self.Time - self.StartPause