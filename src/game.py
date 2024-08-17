# Logique du jeu (gestion des tours, règles, victoires)

from . import abstract
from .ui import Guis, Console

class Game(abstract.abstract_Game):
    def __init__(self, Interfaces: Guis | Console) -> None:
        self.Players = {}
        self.Interfaces = Interfaces
        self.GameMode = Interfaces.chooseGamemode()
    
    def startGame(self):
        print("Starting a new Game !")
        print("Players :", self.Players)
        print("GameMode :", self.GameMode)