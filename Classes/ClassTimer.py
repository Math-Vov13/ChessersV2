from transitions import Machine, MachineError  # Final State Machine Library

# class Timer:
#     def __init__(self):
#         self.ResetTimer()
    
#     def ResetTimer(self):
#         """Remets les paramètres du Timer à 0"""
#         self.Player1 = {}                       #Infos du Joueur 1
#         self.Player2 = {}                       #Infos du Joueur 2

#         self.Active = False                     #Timer activé
#         self.Paused = False                     #Timer en pause

#         self.Start = pygame.time.get_ticks()    #Temps du démarrage du Timer
#         self.Time = 0                           #Temps actuel
#         self.StartPause = 0                     #Temps du début de la Pause
#         self.Pause = 0                          #Durée de la Pause
    
#     def Init(self, CouleurJ1 : str, CouleurJ2 : str):
#         """Initialise les Paramètres du Timer"""
#         self.Player1 = {"Couleur" : CouleurJ1, "Time" : 150}
#         self.Player2 = {"Couleur" : CouleurJ2, "Time" : 150}
    
#     def GetPlrTime(self, Couleur : str):
#         """Récupère le Temps du Joueur"""
#         if Couleur == self.Player1["Couleur"]:
#             return self.Player1["Time"]
#         else:
#             return self.Player2["Time"]
    
#     def StartTime(self):
#         """Démarre le Timer"""
#         self.Active = True
    
#     def UpdateTimer(self, Timer, PlrCouleur):
#         """Actualise le Timer"""
#         self.Time = Timer
#         if (self.Time - self.Start) // 1000:
#             self.Start = self.Time
#             return self.RemoveTime(PlrCouleur)
    
#     def RemoveTime(self, Couleur):
#         """Enlève 1 Seconde au Temps du Joueur"""
#         if Couleur == self.Player1["Couleur"]:
#             self.Player1["Time"] -= 1
#             if self.Player1["Time"] == 0:
#                 return self.Player1["Couleur"]
#         else:
#             self.Player2["Time"] -= 1
#             if self.Player2["Time"] == 0:
#                 return self.Player2["Couleur"]
        
#         return None

    
#     def PauseTimer(self):
#         """Arrête le Timer"""
#         self.Paused = True
#         self.StartPause = self.Time

#     def ContinueTimer(self):
#         """Relance le Timer"""
#         self.Paused = False
#         self.Start =  self.Time
#         self.Pause = self.Time - self.StartPause


class Timer:
    # States (PROTECTED)
    _RUNNING = "running"
    _PAUSED = "paused"
    _STOPPED = "stopped"

    def __init__(self, Chrono: bool= False) -> None:
        # Private properties
        self.__Time = 0
        self.__LastTick = 0
        self.__isChrono = Chrono

        transitions = [
            {"trigger": "run", "source": self._STOPPED, "dest": self._RUNNING, "after": "on_run"},
            {"trigger": "resume", "source": self._PAUSED, "dest": self._RUNNING, "after": "on_run"},
            {"trigger": "pause", "source": self._RUNNING, "dest": self._PAUSED},
            {"trigger": "stop", "source": self._RUNNING, "dest": self._STOPPED, "after": "on_stop"},
            {"trigger": "stop", "source": self._PAUSED, "dest": self._STOPPED, "after": "on_stop"},
        ]

        self.machine = Machine(
            model=self,
            states=[self._RUNNING, self._PAUSED, self._STOPPED],
            transitions=transitions,
            initial=self._STOPPED,
        )
    
    def on_run(self, tick: int = 0):
        self.__LastTick = tick

    def on_stop(self):
        self.__Time = 0
        self.__LastTick = 0
    
    def setAsChrono(self):
        self.__isChrono = not self.__isChrono

    def getTime(self):
        return self.__Time

    def updateTimer(self, tick: int):
        if self.state != self._RUNNING: return
        elapsed = (tick - self.__LastTick) / 1000 # add elapsed time
        self.__LastTick = tick       # update Tick
        if self.__isChrono:
            self.__Time -= elapsed
            print("Chrono:", self.__Time)
        else:
            self.__Time += elapsed
        
        if self.__Time <= 0:
            return False


if __name__ == "__main__":
    testTimer = Timer() # Create Timer Object

    try: # Test States
        testTimer.run() # -> runnig
        testTimer.pause() # -> paused
        testTimer.resume() # -> running
        testTimer.stop() # -> stopped
        testTimer.stop() #  ERROR !
    except MachineError as e: # track error
        print(f"Error with FSM : {e}")