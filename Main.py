## LICENSE
### Mathéo Vovard first implement
### Open Source :)

# This is the main file of the game.

import sys
from time import sleep as wait

from src.game import Game as GameClass
from src.abstract import abstract_Main
from src.ui import Guis, Console, create_UI_Object

# Classes
class Main(abstract_Main):
    def __init__(self, activateGuis: bool = False) -> None:
        self.InterfacesObject : Guis | Console = create_UI_Object(activateGuis)

        self.GameObject : GameClass = None
        
        self.GameLoop()
    
    def GameLoop(self):
        while True:
            if self.createNewGame() == 0:
                break

    def createNewGame(self):
        self.GameObject = GameClass(Interfaces=self.InterfacesObject)

        if self.GameObject.GameMode == 0:
            return 0 # Exit the loop
        return self.GameObject.startGame()


def getResponse()-> bool:
    response : bool | None = None
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ["y", "yes", "true"]:
            response = True
        elif sys.argv[1].lower() in ["n", "n", "false"]:
            response = False

    if response == None:
        response = str(input("Do you want to play with interfaces ? (y/n) ")) == "y"

    print("Bool :", response)
    return response

#### Game

print("Chessers V2")
print("Starting game...")

wait(1)
Main(getResponse())
wait(1)

print("Game ended !")
print("I'm working on the game. Please Wait...")
wait(1)