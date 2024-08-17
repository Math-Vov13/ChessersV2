# All abstract classes
from abc import ABC, abstractmethod

class abstract_Main(ABC):
    def __init__(self) -> None: pass

    @abstractmethod
    def GameLoop(self): """Game loop"""
    @abstractmethod
    def createNewGame(self): """Create a new game instance"""

class abstract_Game(ABC):
    def __init__(self, Gamemode: str = "Normal") -> None: pass
    @abstractmethod
    def startGame(self): """Start the game"""