# Interface en ligne de commande

from time import sleep as wait

from .abstract_ui import abstract_uis
from .enums import GameMode

class Console(abstract_uis):
    def __init__(self) -> None:
        print("No interfaces has been set")

    def chooseGamemode(self) -> GameMode:
        print("Choix du Mode de jeu :")
        # allEnums = [i for i in GameMode]
        # print(allEnums)
        # for e in allEnums:
        #     print("%s. %s" % e[1], e[0])

        print("1. Normal")
        print("2. Competitif")
        print("3. Timer")
        print("4. Entrainement")
        wait(1)
        print("\n0. Exit\n\n")
        wait(1)
        UserInp : str = str(input("Which GameMode do you wante to play ? "))
        return UserInp == "1" or 0